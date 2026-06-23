"""
Chapter 16 — Modern Autonomous: Driving to Poses

This is YOUR workspace. Read the matching lesson first:
    chapters/16-modern-autonomous-paths.md

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/16_starter.py

Stuck? Try for real first, THEN peek at:
    solutions/16_solution.py
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

print("Chapter 16 - delete this line and start coding your exercises!\n")


# ===========================================================================
# Exercise 1
# Drive to a point. Run a single DriveToPoseAction(robot, Pose2d(30, 0, 0))
# with run_action. Print the final pose — it should be near (30, 0, 0).
# ===========================================================================
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 2
# Drive and turn. Target Pose2d(0, 0, 90) — same spot, but rotate to face
# 90°. Confirm the heading ends near 90.
# ===========================================================================
def exercise_2():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 3
# Two legs. SequentialAction of (20, 0, 0) then (20, 20, 0). Print the pose
# after each? (Tip: run them as two separate run_action calls so you can
# print between.) The robot should trace an L.
# ===========================================================================
def exercise_3():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 4
# A box. Sequence four targets that drive a 24" square back to the start.
# Print the final pose; it should be near (0,0). Compare in a comment to
# Chapter 12's *timed* square — which is more reliable and why?
# ===========================================================================
def exercise_4():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 5
# Tolerance matters. Run the same target with tol=0.5 and again with
# tol=5.0. Print both final poses and the difference. In a comment: why
# might a team use a *looser* tolerance on early legs and a tight one on the
# scoring leg?
# ===========================================================================
def exercise_5():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 6
# Start somewhere else. Make Robot(start_x=-30, start_y=-60,
# start_heading=0) (like a real autonomous start corner) and drive to
# Pose2d(0, 0, 0). Pose-based autonomous doesn't care where you start, as
# long as odometry is seeded — show it arrives.
# ===========================================================================
def exercise_6():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 7
# Battery-proof. This is the headline. In a comment, explain why this
# pose-based action arrives at the same place whether the battery is full or
# low, while Chapter 9's "drive 1.5s at 0.6 power" would not. Tie it back to
# the controller closing the error.
# ===========================================================================
def exercise_7():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 8
# Mimic BucketSide. Juice's BucketSide.java drives to a scoring spot,
# scores, then to a sample, repeatedly. Build a SequentialAction that drives
# to a "basket" Pose2d(-50, -50, 45), prints "SCORE", drives to a "sample"
# Pose2d(-30, -30, 0), prints "PICKUP". Run it and print the final pose.
# ===========================================================================
def exercise_8():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 9
# Combine with a command. Bridge Chapters 15 and 16: after driving to a pose
# with an action, run an InstantCommand (or just call a function) that
# prints "LIFT + SCORE". In a comment, describe how a real auto interleaves
# *driving* (actions) with *mechanisms* (commands) — often in parallel.
# ===========================================================================
def exercise_9():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 10
# Design your own autonomous. Pick a made-up mission (e.g., "score 3 samples
# in the basket, then park"). In a comment block, write the full sequence of
# Pose2d targets and mechanism actions you'd run, in order. Then implement
# as much as you can with DriveToPoseAction + prints. This is a real
# autonomous plan — the capstone of the whole course.
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
