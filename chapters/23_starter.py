"""
Chapter 23 — AprilTag Relocalization & Latency Compensation

This is YOUR workspace. Read the matching lesson first:
    chapters/23-apriltag-relocalization.md

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/23_starter.py

Stuck? Try for real first, THEN peek at:
    solutions/23_solution.py
"""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
# Everything from the simulator you might need:
from ftcsim import (Robot, Field, Gamepad, IMU, Motor, StepperServo,
                    PIDFController, run_for, Pose2d, AprilTag, Odometry, Camera,
                    Command, InstantCommand, SequentialCommand, ParallelCommand,
                    SleepCommand, CommandScheduler, DriveToPoseAction,
                    SequentialAction, run_action,
                    LynxModule, reset_hw_reads, hw_reads, KalmanFilter,
                    AsymmetricMotionProfile, Localizer, DriveEncoderLocalizer,
                    DeadWheelLocalizer, OTOSLocalizer,
                    PoseHistory, ConditionalCommand, Subsystem, Button,
                    RunningCommandScheduler, Path, PurePursuitFollower)

print("Chapter 23 - delete this line and start coding your exercises!\n")


# ===========================================================================
# Exercise 1
# See the lag. Make a robot with tags and camera.latency = 0.1. Drive
# forward, and each loop print robot.camera.localize_with_timestamp()'s
# capture_time next to robot.clock. Show the capture time is always ~0.1s
# behind now. (This is the whole problem in one number.)
# ===========================================================================
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 2
# Naive reset is wrong. Drive forward 1s at speed. Then take one camera fix
# and *naively* set your estimate to localize().x. Print it next to the true
# robot.x. Show the naive fix lands behind the true position by roughly
# speed × latency. Explain in a comment.
# ===========================================================================
def exercise_2():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 3
# Build a PoseHistory. Make a PoseHistory(timeout=1.0). In a loop driving
# forward, call hist.add(robot.clock, robot.odometry.get_pose()) each step.
# Afterward, print hist.pose_at(t) for a t in the middle of the drive and
# confirm it returns the pose from back then (not the latest).
# ===========================================================================
def exercise_3():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 4
# Patch one fix. Reproduce the lesson's diagram by hand with the sim: drive
# forward, record history, take a timestamped fix, and call
# hist.patch(measured, capture_time). Print the patched x vs the naive
# measured.x vs true robot.x. Show patched is closer to true.
# ===========================================================================
def exercise_4():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 5
# timeout drops old poses. Add poses at times 0.0, 0.5, 1.5 to a
# PoseHistory(timeout=1.0) (call remove_old(1.5)). Show pose_at(0.0) now
# returns None (too old) while pose_at(1.5) works. In a comment: why cap the
# history at all (memory / relevance)?
# ===========================================================================
def exercise_5():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 6
# Relocalize over a drive. Drive forward 2s with drift + latency. Each loop:
# add to history, and *if* a fix is available, patch it and snap your
# estimate to the patched pose; otherwise coast on odometry. Print final
# estimate vs true. Show drift was erased.
# ===========================================================================
def exercise_6():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 7
# Latency makes it worse — prove it. Run exercise 6 twice: once snapping to
# the naive localize() and once to the patched pose. Print both final
# errors. Show the patched version wins, and that the gap grows if you
# increase latency or speed.
# ===========================================================================
def exercise_7():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 8
# No tag in view. Place the robot so it drives out of camera range partway
# (or clear field.april_tags mid-drive). When localize_with_timestamp()
# returns None, skip the reset and coast on odometry. Show the estimate
# holds steady through the blackout and re-snaps when a tag returns. (Same
# coast-vs-correct logic as Ch 21, now with patching.)
# ===========================================================================
def exercise_8():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 9
# Reject a bad detection. A camera sometimes spits out a garbage fix. Before
# patching, reject any measured pose that is more than (say) 12 inches from
# your current estimate — it's probably a misread. Feed in one good fix and
# one absurd one; show your code accepts the good, ignores the bad. In a
# comment, relate this to why teams gate detections by distance/ambiguity.
# ===========================================================================
def exercise_9():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 10
# Full relocalizing drive base. Combine it all into a relocalize(robot,
# hist) helper and a drive loop that uses it every tick: add history, get a
# timestamped fix, reject outliers, patch, and reset the estimate. Drive a
# multi-leg path and print the final estimate vs true. In a comment, map
# each step to j5155's AprilTagDrive.updatePoseEstimate() line by line. This
# is a real relocalizing localizer — the top of the FTC localization stack.
# ===========================================================================
def exercise_10():
    # ---- YOUR CODE HERE ----
    pass


if __name__ == "__main__":
    # Uncomment each exercise as you finish it, then run this file.
    pass
    # exercise_1()
    # exercise_2()
    # exercise_3()
    # exercise_4()
    # exercise_5()
    # exercise_6()
    # exercise_7()
    # exercise_8()
    # exercise_9()
    # exercise_10()
