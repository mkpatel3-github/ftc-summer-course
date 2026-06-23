"""Chapter 23 solutions - AprilTag Relocalization & Latency Compensation."""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
from ftcsim import Robot, Field, PoseHistory, Pose2d, run_for


def fresh_robot(latency=0.1, drift=0.0):
    r = Robot(field=Field().add_standard_tags())
    r.camera.latency = latency
    r.odometry.drift_per_read = drift
    return r


def ex1():
    # See the lag: the capture time always trails the clock by ~latency.
    r = fresh_robot(latency=0.1)
    def loop(t):
        r.set_drive_power(0, 1, 0)
        fix = r.camera.localize_with_timestamp()
        if fix is not None:
            _, capture_time = fix
            print(f"clock={r.clock:.2f}  capture_time={capture_time:.2f}"
                  f"  lag={r.clock - capture_time:.2f}")
    run_for(r, 0.2, loop)
    # The lag column is always ~0.10s -- that's the whole problem in one number.


def ex2():
    # Naive reset lands BEHIND the true position by ~speed*latency.
    r = fresh_robot(latency=0.1)
    run_for(r, 1.0, lambda t: r.set_drive_power(0, 1, 0))
    fix = r.camera.localize_with_timestamp()
    naive_x = fix[0].x
    print(f"true x={r.x:.2f}  naive fix x={naive_x:.2f}  error={r.x - naive_x:.2f}")
    # At ~40 in/s * 0.1s the fix lags ~4in behind. The camera answer describes
    # where we WERE when the shutter opened, not where we are now.


def ex3():
    # Build a PoseHistory; pose_at(mid) returns the OLD pose, not the latest.
    r = fresh_robot(latency=0.0)
    hist = PoseHistory(timeout=10.0)
    mid_time, mid_true = None, None
    def loop(t):
        nonlocal mid_time, mid_true
        r.set_drive_power(0, 1, 0)
        hist.add(r.clock, r.odometry.get_pose())
        if mid_time is None and r.clock >= 0.5:
            mid_time, mid_true = r.clock, r.x
    run_for(r, 1.0, loop)
    back = hist.pose_at(mid_time)
    print(f"pose_at({mid_time:.2f}) x={back.x:.2f}  (true then ~{mid_true:.2f})"
          f"  latest x={hist.latest().x:.2f}")
    # pose_at returns the pose from back THEN, far behind the final pose.


def ex4():
    # Patch one fix: patched x is closer to true than the naive measured x.
    r = fresh_robot(latency=0.1)
    hist = PoseHistory(timeout=2.0)
    def loop(t):
        r.set_drive_power(0, 1, 0)
        hist.add(r.clock, r.odometry.get_pose())
    run_for(r, 1.0, loop)
    measured, capture_time = r.camera.localize_with_timestamp()
    patched = hist.patch(measured, capture_time)
    print(f"true x={r.x:.2f}  naive x={measured.x:.2f}  patched x={patched.x:.2f}")
    print(f"naive error={abs(r.x - measured.x):.2f}  "
          f"patched error={abs(r.x - patched.x):.2f}")
    # Patched rolls the late fix forward by the odometry driven since capture,
    # landing near the true CURRENT pose.


def ex5():
    # timeout drops old poses.
    hist = PoseHistory(timeout=1.0)
    hist._entries = []  # start clean
    hist.add(0.0, Pose2d(0, 0, 0))
    hist.add(0.5, Pose2d(5, 0, 0))
    hist.add(1.5, Pose2d(15, 0, 0))   # adding at 1.5 drops anything < 0.5
    print("pose_at(0.0):", hist.pose_at(0.0))   # too old -> None
    print("pose_at(1.5):", hist.pose_at(1.5))   # kept
    # Cap the history so it doesn't grow without bound (memory) and so stale,
    # irrelevant poses can't be matched to a fresh detection (relevance).


def ex6():
    # Relocalize over a drive with drift + latency: snap to the patched pose.
    r = fresh_robot(latency=0.1, drift=0.05)
    hist = PoseHistory(timeout=2.0)
    est = [Pose2d(0, 0, 0)]
    def loop(t):
        r.set_drive_power(0, 0.5, 0)        # half power: stay mid-field, still moving
        odo = r.odometry.get_pose()
        hist.add(r.clock, odo)
        est[0] = odo
        fix = r.camera.localize_with_timestamp()
        if fix is not None:
            patched = hist.patch(*fix)
            if patched is not None:
                est[0] = patched
    run_for(r, 2.0, loop)
    print(f"true x={r.x:.2f}  estimate x={est[0].x:.2f}  "
          f"drift erased, error={abs(r.x - est[0].x):.2f}")


def _drive_and_estimate(use_patch):
    r = fresh_robot(latency=0.1, drift=0.05)
    hist = PoseHistory(timeout=2.0)
    est = [Pose2d(0, 0, 0)]
    def loop(t):
        r.set_drive_power(0, 0.5, 0)         # half power: still moving at the end
        hist.add(r.clock, r.odometry.get_pose())
        fix = r.camera.localize_with_timestamp()
        if fix is not None:
            if use_patch:
                est[0] = hist.patch(*fix)
            else:
                est[0] = fix[0]      # naive: snap to the stale fix
    run_for(r, 2.0, loop)
    return abs(r.x - est[0].x)


def ex7():
    # Latency makes naive worse -- prove it.
    naive_err = _drive_and_estimate(use_patch=False)
    patched_err = _drive_and_estimate(use_patch=True)
    print(f"naive final error={naive_err:.2f}  patched final error={patched_err:.2f}")
    # Patched wins; the gap grows with more latency or speed (more motion to
    # roll forward = more error the naive version ignores).


def ex8():
    # No tag in view: coast on odometry, re-snap when a tag returns.
    r = fresh_robot(latency=0.1)
    hist = PoseHistory(timeout=2.0)
    est = [Pose2d(0, 0, 0)]
    def loop(t):
        r.set_drive_power(0, 1, 0)
        hist.add(r.clock, r.odometry.get_pose())
        if abs(r.clock - 0.5) < 0.03:
            r.field.april_tags = []                 # blackout
        if abs(r.clock - 1.0) < 0.03:
            r.field.add_standard_tags()             # tag returns
        fix = r.camera.localize_with_timestamp()
        if fix is not None:
            patched = hist.patch(*fix)
            est[0] = patched if patched is not None else est[0]
        else:
            est[0] = r.odometry.get_pose()          # coast
        print(f"clock={r.clock:.2f}  tag={'yes' if fix else 'NO '}  "
              f"est x={est[0].x:.2f}")
    run_for(r, 1.2, loop)
    # Estimate holds through the blackout and re-snaps when the tag comes back.


def ex9():
    # Reject a bad detection more than 12in from the current estimate.
    r = fresh_robot(latency=0.0)
    run_for(r, 1.0, lambda t: r.set_drive_power(0, 1, 0))
    estimate = r.odometry.get_pose()
    def accept(measured):
        return measured.distance_to(estimate) <= 12.0
    good = Pose2d(estimate.x + 2, estimate.y, 0)     # plausible
    bad = Pose2d(estimate.x + 80, estimate.y, 0)     # absurd misread
    print("accept good?", accept(good), " accept bad?", accept(bad))
    # Teams gate detections by distance/ambiguity so one garbage frame can't
    # teleport the robot across the field.


def relocalize(robot, hist, estimate):
    """One tick of latency-correct relocalization (the Ch 23 helper)."""
    hist.add(robot.clock, robot.odometry.get_pose())
    fix = robot.camera.localize_with_timestamp()
    if fix is None:
        return robot.odometry.get_pose()             # coast
    measured, capture_time = fix
    if measured.distance_to(estimate) > 12.0:
        return estimate                               # reject outlier
    patched = hist.patch(measured, capture_time)
    return patched if patched is not None else estimate


def ex10():
    # Full relocalizing drive base over a multi-leg path.
    r = fresh_robot(latency=0.1, drift=0.05)
    hist = PoseHistory(timeout=2.0)
    est = [Pose2d(0, 0, 0)]
    def loop(t):
        r.set_drive_power(0, 1, 0) if t < 1.0 else r.set_drive_power(1, 0, 0)
        est[0] = relocalize(r, hist, est[0])
    run_for(r, 2.0, loop)
    print(f"true ({r.x:.1f},{r.y:.1f})  estimate ({est[0].x:.1f},{est[0].y:.1f})")
    # Maps to j5155 AprilTagDrive.updatePoseEstimate(): odometry first
    # (hist.add), get the averaged tag fix (localize_with_timestamp), reject
    # implausible ones, patch() to back-date + roll forward, reset the pose.


if __name__ == "__main__":
    for name in ["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10"]:
        print("\n===", name, "===")
        globals()[name]()
