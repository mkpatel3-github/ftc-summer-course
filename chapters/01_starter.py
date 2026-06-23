"""
Chapter 1 — Hello, Robot

This is YOUR workspace. Read the matching lesson first:
    chapters/01-hello-robot.md

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/01_starter.py

Stuck? Try for real first, THEN peek at:
    solutions/01_solution.py
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
                    DeadWheelLocalizer, OTOSLocalizer)

print("Chapter 01 - delete this line and start coding your exercises!\n")


# ===========================================================================
# Exercise 1
# Hello Juice. Print one telemetry line that says Team: Juice 16236. Run it.
# ===========================================================================
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 2
# Three types. Make three variables: an int for your favorite robot's wheel
# count (4), a double for a motor power (0.75), and a String for the team
# name. Print all three with telemetry, each on its own line.
# ===========================================================================
def exercise_2():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 3
# Java costume. Take your three variables from #2 and write — in a comment —
# what each line would look like in Java (with the type and semicolon).
# Don't run the Java; just write it correctly.
# ===========================================================================
def exercise_3():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 4
# Math like Python. A robot drives at 0.6 power for 3.0 seconds. Compute and
# print distance = power * 3.0 (just the number, units don't matter yet).
# ===========================================================================
def exercise_4():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 5
# Booleans. Make a boolean-style variable is_red_alliance = True. Print a
# telemetry line Alliance: RED if it's true and Alliance: BLUE if false.
# (Use an if/else.)
# ===========================================================================
def exercise_5():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 6
# The update() trap. Add three telemetry lines but call update() only once
# at the end. Then write a second version that calls update() after each
# line. Run both. In a comment, explain what update() actually does (hint:
# it's like pressing "send").
# ===========================================================================
def exercise_6():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 7
# Average. A motor's encoder reads 1800 ticks; another reads 1810. Print the
# average. Then in a comment, note: in Java (1800 + 1810) / 2 using int
# gives a *surprising* answer — what is it and why? (This is the famous
# integer-division gotcha.)
# ===========================================================================
def exercise_7():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 8
# Rounding telemetry. Real telemetry of a double is ugly (6.000000001).
# Print a power value of 2/3 rounded to 2 decimals. (Python: round(x, 2).)
# ===========================================================================
def exercise_8():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 9
# A status line like Juice. Recreate the *style* of TeleOpMainRed's
# telemetry: print four lines — MODE, COLOR, CLIMB, state — with any
# sensible made-up values. Make it look like a real driver station screen.
# ===========================================================================
def exercise_9():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 10
# Mini design. In plain English (a comment block), list every piece of
# information *you* would want on your driver station during a match, and
# why. No code — this is the "think like a programmer" muscle. Compare your
# list to the four lines Juice actually shows.
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
