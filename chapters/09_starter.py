"""
Chapter 9 — Autonomous

This is YOUR workspace. Read the matching lesson first:
    chapters/09-autonomous.md

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/09_starter.py

Stuck? Try for real first, THEN peek at:
    solutions/09_solution.py
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

print("Chapter 09 - delete this line and start coding your exercises!\n")


# ===========================================================================
# Exercise 1
# Start at a pose. Create a robot at Pose2d(-30, -60, 0) style start
# (Robot(start_x=-30, start_y=-60, start_heading=0)). Print its pose.
# ===========================================================================
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 2
# Go to a point (dead reckoning). Write go_to_x(robot, target_x) that uses
# drive_inches logic to move the robot's x to a target. Move from -30 to 0.
# ===========================================================================
def exercise_2():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 3
# Two-segment path. Drive forward 24", turn to 45°, drive forward 20". Print
# the pose after each segment. (You're hand-building what a spline does
# smoothly.)
# ===========================================================================
def exercise_3():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 4
# A step list. Represent an autonomous as a Python list of (name, function)
# tuples. Write run_sequence(robot, steps) that runs each function in order
# and prints "[1/4] preload ... done". This is your SequentialAction.
# ===========================================================================
def exercise_4():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 5
# Recreate BucketSide's shape. Build a step list named like Juice's:
# preload, spike1, depo1, spike2, depo2, spike3, depo3, park. Each step can
# just be a small move (drive/turn) — the point is the *structure*. Run it
# with run_sequence.
# ===========================================================================
def exercise_5():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 6
# Pose targeting. Write drive_to_pose(robot, x, y, heading) that: turns to
# face the target point, drives straight to it (using distance = hypot of
# dx,dy), then turns to the final heading. Drive from start to (-56, -56,
# 45) like Juice's preload. Print how close you got.
# ===========================================================================
def exercise_6():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 7
# Distance-to-pose helper. Write distance_to(robot, x, y) returning the
# straight- line distance (math.hypot). Use it to confirm exercise 6 ended
# within a few inches of the target.
# ===========================================================================
def exercise_7():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 8
# Auto + subsystem. Combine with Chapter 8: at the "depo" steps, also call a
# lift.run_to_preset(HIGH_BASKET) and print "scored". Your autonomous now
# drives AND operates a mechanism, like the real thing.
# ===========================================================================
def exercise_8():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 9
# Timed autonomous. Real auto is 30 seconds. Track elapsed sim time and make
# run_sequence stop early if a 30-second budget runs out, printing which
# steps didn't finish. (Robots that run out of time mid-path is a real
# problem teams plan for.)
# ===========================================================================
def exercise_9():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 10
# Design a full auto. Pick a simple scoring plan in plain English: e.g.
# "score preload in high basket, grab 2 floor samples, score each, park."
# Express it as a step list of drive_to_pose + subsystem calls, run it in
# the sim, and print the final pose + "points scored" tally. Then write
# (comment) one thing RoadRunner would do better than your dead-reckoning
# version and why Juice uses it.
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
