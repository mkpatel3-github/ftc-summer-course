"""
Chapter 19 — Motion Profiling: Smooth, Fast, Repeatable

This is YOUR workspace. Read the matching lesson first:
    chapters/19-motion-profiling.md

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/19_starter.py

Stuck? Try for real first, THEN peek at:
    solutions/19_solution.py
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

print("Chapter 19 - delete this line and start coding your exercises!\n")


# ===========================================================================
# Exercise 1
# Make a profile. Create AsymmetricMotionProfile(distance=1000, max_v=500,
# accel=1000, decel=1000). Print total_time, calculate(0), and
# calculate(total_time). Confirm it starts at 0 and ends at 1000.
# ===========================================================================
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 2
# Sample the curve. Print calculate(t) for t = 0, 0.25, 0.5, 0.75, and
# total_time of that profile. Confirm the position increases smoothly and
# lands on 1000.
# ===========================================================================
def exercise_2():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 3
# Velocity shape. Print velocity(t) across the same times. Confirm it ramps
# up, holds near max_v, then ramps down to 0 — the trapezoid.
# ===========================================================================
def exercise_3():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 4
# Triangle case. Make a *short* move that never reaches cruise:
# AsymmetricMotionProfile(distance=50, max_v=500, accel=1000, decel=1000).
# Print total_time and the peak velocity (prof.peak_v). Show peak_v is less
# than max_v — explain why in a comment.
# ===========================================================================
def exercise_4():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 5
# Asymmetric. Build two profiles for the same distance: one with accel ==
# decel, one that decelerates *twice* as hard as it accelerates. Print both
# total_times and describe, in a comment, when you'd want to brake harder
# than you launch.
# ===========================================================================
def exercise_5():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 6
# Plot it (ASCII). For a profile, print one line per time step where the
# number of # characters is proportional to calculate(t). You should *see*
# the S-shaped position curve rise and level off. (No libraries — just "#" *
# int(pos / scale).)
# ===========================================================================
def exercise_6():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 7
# Track it with a PID. Simulate a lift: a position variable starting at 0.
# Each step dt=0.02, compute the profile target calculate(t), run a
# PIDFController to get power, and move the position by power * step_size.
# Show the lift follows the profile and ends near the target. (Tune kp until
# it tracks.)
# ===========================================================================
def exercise_7():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 8
# Profile vs slam. Compare two strategies to reach 1000: (a) "slam" = full
# power until past target then stop, (b) profile + PID. Print the position
# trace of each near the end and describe the overshoot difference in a
# comment.
# ===========================================================================
def exercise_8():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 9
# Add feedforward. Extend exercise 7: add kV * profile.velocity(t) to the
# PID output. Show the tracking error (target − actual) is smaller with
# feedforward than without. Explain what kV is doing.
# ===========================================================================
def exercise_9():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 10
# Lift presets, profiled. Combine with Chapter 17: write a Lift that, given
# a Globals preset height, builds a profile from its current position to the
# target and tracks it. Command it GROUND → HIGH → LOW and print where it
# lands each time. This is a real, competition-grade lift.
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
