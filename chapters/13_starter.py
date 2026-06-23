"""
Chapter 13 — Odometry: Always Know Where You Are

This is YOUR workspace. Read the matching lesson first:
    chapters/13-odometry-and-pose.md

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/13_starter.py

Stuck? Try for real first, THEN peek at:
    solutions/13_solution.py
"""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
# Everything from the simulator you might need:
from ftcsim import (Robot, Field, Gamepad, IMU, Motor, StepperServo,
                    PIDFController, run_for, Pose2d, AprilTag, Odometry, Camera,
                    Command, InstantCommand, SequentialCommand, ParallelCommand,
                    SleepCommand, CommandScheduler, DriveToPoseAction,
                    SequentialAction, run_action)

print("Chapter 13 - delete this line and start coding your exercises!\n")


# ===========================================================================
# Exercise 1
# Read your pose. Make a robot, drive forward 1s, then print
# robot.odometry.get_pose(). Confirm x grew and y/heading stayed ~0.
# ===========================================================================
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 2
# Pose after a turn. Turn the robot to ~90° (drive with rx), then print the
# pose's heading. Confirm odometry tracked the rotation.
# ===========================================================================
def exercise_2():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 3
# Distance between poses. Drive somewhere, grab pose =
# robot.odometry.get_pose(), then use pose.distance_to(Pose2d(0, 0)) to
# print how far from the field center you are.
# ===========================================================================
def exercise_3():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 4
# Live pose telemetry. In a run_for loop driving forward, print the odometry
# pose every 25 loops. Watch x climb in real time — this is what a driver
# sees.
# ===========================================================================
def exercise_4():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 5
# Track a multi-leg path. Drive forward 1s, strafe 1s, forward 1s. After
# each leg, print the pose. You're logging a path like an autonomous would.
# ===========================================================================
def exercise_5():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 6
# "Am I there yet?" Pick a target Pose2d(40, 0, 0). In a loop, drive forward
# and stop as soon as robot.odometry.get_pose().distance_to(target) < 2.0.
# Print the final pose and how long it took. (This is the seed of "drive to
# pose" in Chapter 16.)
# ===========================================================================
def exercise_6():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 7
# Feel the drift. Set robot.odometry.noise = 0.5. Read the pose 5 times
# *without* moving and print each. Notice it jitters even though the robot
# is still — real sensors do this. In a comment, say why timing-based
# autonomous (FLL style) can't catch this.
# ===========================================================================
def exercise_7():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 8
# Offsets matter. Juice sets xOffset/yOffset for where the pods sit relative
# to robot center. In a comment, explain what would go wrong in the pose if
# you told the software the pods were at the center when they're really 6"
# forward (hint: rotation).
# ===========================================================================
def exercise_8():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 9
# Reset to a known pose. At the start of autonomous you *tell* odometry
# where you are. Simulate this: move the robot to (20, -30), then in a
# comment explain why you must "seed" the starting pose before autonomous
# and what happens if you forget.
# ===========================================================================
def exercise_9():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 10
# Pinpoint vs OTOS, in your words. Research note: in a comment, summarize
# the trade-off between a Pinpoint (two encoder pods) and an OTOS (optical
# mouse sensor) — cost, setup, and what each struggles with. (See
# gobilda.com and sparkfun's OTOS page in REFERENCES.) No code; this is the
# "choose your hardware" muscle.
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
