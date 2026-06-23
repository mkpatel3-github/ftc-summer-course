"""
Chapter 20 — Swappable Localizers

This is YOUR workspace. Read the matching lesson first:
    chapters/20-swappable-localizers.md

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/20_starter.py

Stuck? Try for real first, THEN peek at:
    solutions/20_solution.py
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

print("Chapter 20 - delete this line and start coding your exercises!\n")


# ===========================================================================
# Exercise 1
# Three localizers, one robot. Make a Robot, then create all three localizer
# types on it. Print each one's get_pose() right away. Confirm all three
# report (about) the starting pose.
# ===========================================================================
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 2
# Code against the interface. Write report(localizer) that just calls
# localizer.get_pose() and prints it — with no mention of which type it is.
# Call it with all three. This function is "interface-only" code.
# ===========================================================================
def exercise_2():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 3
# Drive and compare. Drive the robot forward 2s. Then read all three
# localizers and print their poses. They should be close, but not identical
# — note which drifts most.
# ===========================================================================
def exercise_3():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 4
# Feel the drift. Read each localizer 20 times *without moving the robot*
# and print the first and last reading. Rank the three by how much they
# wander. In a comment, match each to its real-world cause (wheel slip /
# clean pods / optical jitter).
# ===========================================================================
def exercise_4():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 5
# A swappable drive function. Write drive_until_x(robot, localizer,
# target_x) that drives forward until localizer.get_pose().x >= target_x.
# Run it with a DriveEncoderLocalizer and again with a DeadWheelLocalizer —
# same function, swapped strategy. Print where each stopped.
# ===========================================================================
def exercise_5():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 6
# Make your own localizer. Subclass Localizer to create PerfectLocalizer
# whose get_pose() returns the robot's true pose with zero drift/noise (use
# robot.get_pose()). Pass it to your report() from exercise 2 — it just
# works, because it honors the contract.
# ===========================================================================
def exercise_6():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 7
# The contract enforced. Create a broken "localizer" class that forgets to
# implement get_pose() (just pass the base). Call get_pose() on it inside a
# try/except and print the error. In a comment, explain how the interface
# tells you *at the point of use* that you broke the contract.
# ===========================================================================
def exercise_7():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 8
# Strategy at runtime. Put your three localizers in a dict keyed by name
# ("encoder", "deadwheel", "otos"). Write code that picks one by a string
# variable and uses it — simulating choosing your hardware from a config
# without changing logic.
# ===========================================================================
def exercise_8():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 9
# Best of both (preview). Drive forward 2s. The drive-encoder localizer has
# drifted; a (hypothetical) perfect one hasn't. Print the gap between them.
# In a comment, predict how you'd *combine* a drifting-but-smooth source
# with an absolute one — this is exactly Chapter 21 (sensor fusion).
# ===========================================================================
def exercise_9():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 10
# Why interfaces win. In a comment block, describe a concrete mid-season
# scenario: your team buys a Pinpoint to replace drive-encoder odometry.
# With the Localizer interface, how many files change? Without it (position
# code copy-pasted everywhere), what's the risk? This is the design lesson
# of the chapter.
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
