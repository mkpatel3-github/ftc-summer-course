# Chapter 13 — Odometry: Always Know Where You Are

> Goal: stop *guessing* where the robot is from "drove 2 seconds at 0.6 power" and start
> *knowing* — a live `(x, y, heading)` pose, updated every loop. This is the leap from FLL
> dead-reckoning to real FTC, and Juice's `KalmanDrive.java` is built on it.

## What odometry is

**Odometry** = continuously tracking the robot's position on the field. In Chapter 3 you
turned encoder ticks into inches for *one straight move*. Odometry does that **every
loop**, for x, y, *and* heading at once, so at any instant you can ask "where am I?" and
get a `Pose2d(x, y, heading)`.

Modern teams (including Juice) do this with a dedicated sensor so they don't have to do
the math:

- **goBILDA Pinpoint** — a little computer with two odometry "pods" (unpowered wheels on
  encoders). Juice uses this in `KalmanDrive.java` (`goBILDA_4_BAR_POD` resolution,
  `xOffset`/`yOffset` for where the pods sit).
- **SparkFun OTOS** — an optical sensor that watches the floor like a gaming mouse and
  reports pose directly.

Either way, in code it's one object you ask for a pose:

```python
pose = robot.odometry.get_pose()      # -> Pose2d(x, y, heading)
print(pose.x, pose.y, pose.heading)
```

In Juice's real `KalmanDrive.java` this is the `Pinpoint` driver feeding the localizer.

## Why it's a superpower

Once you always know your pose, you can:

- Drive to an **exact spot** with a controller, instead of timing it (Chapter 16).
- **Correct** when a defender bumps you — re-read the pose and re-plan.
- Reuse the same autonomous on either alliance by reflecting coordinates.

## The catch: drift

Wheel/pod odometry slowly **drifts** — tiny errors add up over a match (wheel slip,
bumps). That's *why* Juice's drive is called **`KalmanDrive`**: it fuses odometry with a
camera (AprilTags) using a **Kalman filter** to cancel the drift. You'll meet vision in
Chapter 14 and fusion in Chapter 15. For now: odometry is great, but not perfect.

---

## Exercises

The sim's `robot.odometry.get_pose()` returns a `Pose2d` with `.x`, `.y`, `.heading`.
You can create targets with `Pose2d(x, y, heading)` (already imported for you). To feel
drift, you can make a noisy sensor: `robot.odometry.noise = 0.5`.

**1. Read your pose.** Make a robot, drive forward 1s, then print
`robot.odometry.get_pose()`. Confirm x grew and y/heading stayed ~0.

**2. Pose after a turn.** Turn the robot to ~90° (drive with rx), then print the pose's
heading. Confirm odometry tracked the rotation.

**3. Distance between poses.** Drive somewhere, grab `pose = robot.odometry.get_pose()`,
then use `pose.distance_to(Pose2d(0, 0))` to print how far from the field center you are.

**4. Live pose telemetry.** In a `run_for` loop driving forward, print the odometry pose
every 25 loops. Watch x climb in real time — this is what a driver sees.

**5. Track a multi-leg path.** Drive forward 1s, strafe 1s, forward 1s. After each leg,
print the pose. You're logging a path like an autonomous would.

**6. "Am I there yet?"** Pick a target `Pose2d(40, 0, 0)`. In a loop, drive forward and
stop as soon as `robot.odometry.get_pose().distance_to(target) < 2.0`. Print the final
pose and how long it took. (This is the seed of "drive to pose" in Chapter 16.)

**7. Feel the drift.** Set `robot.odometry.noise = 0.5`. Read the pose 5 times *without*
moving and print each. Notice it jitters even though the robot is still — real sensors do
this. In a comment, say why timing-based autonomous (FLL style) can't catch this.

**8. Offsets matter.** Juice sets `xOffset`/`yOffset` for where the pods sit relative to
robot center. In a comment, explain what would go wrong in the pose if you told the
software the pods were at the center when they're really 6" forward (hint: rotation).

**9. Reset to a known pose.** At the start of autonomous you *tell* odometry where you
are. Simulate this: move the robot to `(20, -30)`, then in a comment explain why you must
"seed" the starting pose before autonomous and what happens if you forget.

**10. Pinpoint vs OTOS, in your words.** Research note: in a comment, summarize the
trade-off between a Pinpoint (two encoder pods) and an OTOS (optical mouse sensor) — cost,
setup, and what each struggles with. (See gobilda.com and sparkfun's OTOS page in
REFERENCES.) No code; this is the "choose your hardware" muscle.

## Java bridge

```java
// goBILDA Pinpoint (the sensor Juice's KalmanDrive uses):
GoBildaPinpointDriver pinpoint = hardwareMap.get(GoBildaPinpointDriver.class, "pinpoint");
pinpoint.setOffsets(xOffsetMM, yOffsetMM);
pinpoint.setEncoderResolution(GoBildaPinpointDriver.GoBildaOdometryPods.goBILDA_4_BAR_POD);

// every loop:
pinpoint.update();
Pose2D pose = pinpoint.getPosition();
double x = pose.getX(DistanceUnit.INCH);
double y = pose.getY(DistanceUnit.INCH);
double h = pose.getHeading(AngleUnit.DEGREES);
```

➡️ Solutions: [`solutions/13_solution.py`](../solutions/13_solution.py)
