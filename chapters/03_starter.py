"""
Chapter 3 — Encoders & Distance

This is YOUR workspace. Read the matching lesson first:
    chapters/03-encoders-and-distance.md

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/03_starter.py

Stuck? Try for real first, THEN peek at:
    solutions/03_solution.py
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

print("Chapter 03 - delete this line and start coding your exercises!\n")


# ===========================================================================
# Exercise 1
# Read ticks. Reset front_left, drive forward 1s, print the encoder value.
# How many inches is that (divide by 45)?
# ===========================================================================
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 2
# Two conversion functions. Write inches_to_ticks(inches) and
# ticks_to_inches(ticks). Test that converting 24 inches → ticks → inches
# gives back 24.
# ===========================================================================
def exercise_2():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 3
# Drive exactly 24 inches. Use the while-loop pattern to drive forward until
# the encoder shows 24 inches, then stop. Print the final pose — x should be
# near 24.
# ===========================================================================
def exercise_3():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 4
# A reusable drive_inches. Wrap exercise 3 into a function
# drive_inches(robot, inches, power=0.5). Drive 12, then 36 inches with it.
# ===========================================================================
def exercise_4():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 5
# Backward by encoder. Make drive_inches handle negative distances: if
# inches is negative, drive at negative power and loop until the encoder
# drops below the target. Test with -12.
# ===========================================================================
def exercise_5():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 6
# Why time is worse (experiment). Drive 24 inches by *time* (guess the
# seconds at 0.5 power), then by *encoder*. Run each from the same start.
# Then imagine the battery is weak: in the sim, lower the power to 0.3 and
# repeat both. Which method still ends at 24 inches? Explain in a comment.
# ===========================================================================
def exercise_6():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 7
# Square dance. Make the robot trace a square: drive 24 inches, turn 90°
# (set_drive_power(0,0,0.5) until imu.get_heading() reaches the next
# corner), repeat 4 times. (Reuse Chapter 4's turn idea early — or just turn
# by time for now.) Print the pose after each side.
# ===========================================================================
def exercise_7():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 8
# Average the encoders. A real robot reads *all four* wheel encoders and
# averages them for a better distance estimate (one wheel can slip). Write
# average_distance_inches(robot) that averages the four encoders and
# converts to inches. Drive forward and print it.
# ===========================================================================
def exercise_8():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 9
# Slow down near the target (taste of PID). Modify drive_inches so that when
# the robot is within the last 6 inches, it uses lower power (e.g. 0.2)
# instead of full. Does it overshoot less? This is the *intuition* behind
# the "P" in PID you'll build later.
# ===========================================================================
def exercise_9():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 10
# Mission math. A game element is 30 inches forward and the robot must stop
# 4 inches short to avoid knocking it. Using only drive_inches, write code
# that ends with the robot 26 inches forward. Then write (comment) what
# could still make it inaccurate on a real field (wheel slip, bumps,
# battery) — and which sensor from later chapters fixes heading drift.
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
