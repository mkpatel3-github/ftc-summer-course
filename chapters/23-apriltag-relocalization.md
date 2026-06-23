# Chapter 23 — AprilTag Relocalization & Latency Compensation

> Goal: use a camera fix to *reset* your pose mid-match — and do it **correctly**, accounting
> for the fact that the camera's answer arrives **late**. This is the last piece of the
> localization story (odometry → vision → fusion → **relocalization**) and the exact trick
> j5155 / Capital City Dynamics ship in `PosePatcher.java` + `AprilTagDrive.java`.

## The problem fusion alone doesn't solve

In Chapter 21 you fused drifting odometry with a noisy camera. But there's a subtle bug
hiding in every vision system: **the camera's answer is old.** A webcam frame takes time to
expose, transfer, and run AprilTag detection — easily **50–150 ms**. By the time your code
hears "you were at x=24," the robot has already driven somewhere else.

If you naively slam that stale reading onto your *current* pose, you teleport backward to
where you **were**, not where you **are**. At full speed (≈40 in/s) a 100 ms lag is **4
inches** of error — injected by the very system meant to fix error. Relocalization done wrong
is worse than no relocalization.

## The fix: timestamp everything, then back-date

j5155's insight: every detection comes with `frameAcquisitionNanoTime` — the instant the
shutter actually opened. So:

1. **Keep a history** of your odometry pose, each entry stamped with the time.
2. When a fix arrives, look up **where odometry thought you were at the capture time**.
3. The difference between the camera's answer and that old odometry pose is the **correction**.
4. **Re-apply** all the odometry motion you've driven *since* the capture, so the correction
   lands on your **current** pose, not the stale one.

That's latency compensation. The fix is applied as if you'd received it instantly.

```
time:     t0 (shutter) .......... t1 (answer arrives, "now")
odometry:  x=20  -->  -->  -->  -->  x=25     (drove +5 since the frame)
camera:    "you were at x=21 at t0"
           correction at t0 = 21 - 20 = +1
           apply to NOW:    25 + 1 = x=26     <- corrected current pose
```

## The sim's tools

The camera can report a capture timestamp, and `PoseHistory` does the back-dating:

```python
from ftcsim import Robot, Field, PoseHistory

robot = Robot(field=Field().add_standard_tags())
robot.camera.latency = 0.1                 # 100 ms lag
hist = PoseHistory(timeout=1.0)

# each loop:
hist.add(robot.clock, robot.odometry.get_pose())   # stamp the current pose
fix = robot.camera.localize_with_timestamp()        # (pose, capture_time) or None
if fix is not None:
    measured, capture_time = fix
    corrected = hist.patch(measured, capture_time)   # rolled forward to now
```

`patch` finds the odometry pose at `capture_time`, measures how far you've moved since, and
returns the camera fix shifted by that motion — your real current pose.

## Java bridge (j5155 PosePatcher + AprilTagDrive)

```java
// AprilTagDrive.updatePoseEstimate(), each loop:
PoseVelocity2d posVel = super.updatePoseEstimate();   // OTOS/odometry first
posePatcher.add(pose);                                // stamp current pose
posePatcher.removeOld();                               // drop >1s old
Vector2d aprilVector = getVectorBasedOnTags();         // averaged tag fix, or null
if (aprilVector != null) {
    long tagTime = detection.frameAcquisitionNanoTime; // when the shutter opened
    Pose2d corrected = posePatcher.patch(aprilVector, tagTime);
    pose = corrected;                                  // RESET to the tag-corrected pose
}
```

```java
// PosePatcher keeps a TreeMap<Long, Pose2d> of timestamp -> pose, and patch()
// finds the entry at-or-before the capture time, computes the delta, and rolls
// every later entry forward by that delta (re-applying odometry since the frame).
```

---

## Exercises

Use `from ftcsim import Robot, Field, PoseHistory, run_for`. Set `robot.camera.latency` to
simulate lag, `robot.odometry.drift_per_read` for drift, and tags via
`Field().add_standard_tags()`. `robot.clock` is the sim time; it advances on `robot.step`.

**1. See the lag.** Make a robot with tags and `camera.latency = 0.1`. Drive forward, and each
loop print `robot.camera.localize_with_timestamp()`'s capture_time next to `robot.clock`. Show
the capture time is always ~0.1s behind now. (This is the whole problem in one number.)

**2. Naive reset is wrong.** Drive forward 1s at speed. Then take one camera fix and *naively*
set your estimate to `localize().x`. Print it next to the true `robot.x`. Show the naive fix
lands **behind** the true position by roughly `speed × latency`. Explain in a comment.

**3. Build a PoseHistory.** Make a `PoseHistory(timeout=1.0)`. In a loop driving forward, call
`hist.add(robot.clock, robot.odometry.get_pose())` each step. Afterward, print
`hist.pose_at(t)` for a `t` in the middle of the drive and confirm it returns the pose from
back then (not the latest).

**4. Patch one fix.** Reproduce the lesson's diagram by hand with the sim: drive forward,
record history, take a timestamped fix, and call `hist.patch(measured, capture_time)`. Print
the patched x vs the naive `measured.x` vs true `robot.x`. Show patched is **closer to true**.

**5. timeout drops old poses.** Add poses at times 0.0, 0.5, 1.5 to a `PoseHistory(timeout=1.0)`
(call `remove_old(1.5)`). Show `pose_at(0.0)` now returns `None` (too old) while `pose_at(1.5)`
works. In a comment: why cap the history at all (memory / relevance)?

**6. Relocalize over a drive.** Drive forward 2s with drift + latency. Each loop: add to
history, and *if* a fix is available, patch it and snap your estimate to the patched pose;
otherwise coast on odometry. Print final estimate vs true. Show drift was erased.

**7. Latency makes it worse — prove it.** Run exercise 6 twice: once snapping to the **naive**
`localize()` and once to the **patched** pose. Print both final errors. Show the patched
version wins, and that the gap grows if you increase `latency` or speed.

**8. No tag in view.** Place the robot so it drives out of camera range partway (or clear
`field.april_tags` mid-drive). When `localize_with_timestamp()` returns `None`, skip the reset
and coast on odometry. Show the estimate holds steady through the blackout and re-snaps when a
tag returns. (Same coast-vs-correct logic as Ch 21, now with patching.)

**9. Reject a bad detection.** A camera sometimes spits out a garbage fix. Before patching,
reject any measured pose that is more than (say) 12 inches from your current estimate — it's
probably a misread. Feed in one good fix and one absurd one; show your code accepts the good,
ignores the bad. In a comment, relate this to why teams gate detections by distance/ambiguity.

**10. Full relocalizing drive base.** Combine it all into a `relocalize(robot, hist)` helper
and a drive loop that uses it every tick: add history, get a timestamped fix, reject outliers,
patch, and reset the estimate. Drive a multi-leg path and print the final estimate vs true.
In a comment, map each step to j5155's `AprilTagDrive.updatePoseEstimate()` line by line. This
is a real relocalizing localizer — the top of the FTC localization stack.

## Java bridge

```java
// The shape of a relocalizing loop, in spirit:
estimate = odometry.update();          // predict from wheels/OTOS
history.add(now(), estimate);
Detection d = camera.getLatest();
if (d != null && d.isPlausible(estimate)) {     // reject outliers
    estimate = history.patch(d.fieldPose, d.frameAcquisitionNanoTime);  // back-date + roll fwd
}
// estimate is now drift-free AND latency-correct.
```

You've now built the entire localization arc: dead reckoning, then vision, then fusion, then
latency-correct relocalization. This is what keeps a top robot's pose honest for a full match.

➡️ Solutions: [`solutions/23_solution.py`](../solutions/23_solution.py)
