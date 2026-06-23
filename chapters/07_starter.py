"""
Chapter 7 — PID Control

This is YOUR workspace. Read the matching lesson first:
    chapters/07-pid-control.md

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/07_starter.py

Stuck? Try for real first, THEN peek at:
    solutions/07_solution.py
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

print("Chapter 07 - delete this line and start coding your exercises!\n")


# ===========================================================================
# Exercise 1
# P-only controller. Write p_control(error, kp) returning kp*error. Simulate
# a lift: position starts at 0, target 1000; each step position +=
# p_control(target-pos, 0.001) * 50. Loop 100 times, print position every 20
# steps. Does it reach 1000? Does it overshoot?
# ===========================================================================
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 2
# Feel the gain. Repeat exercise 1 with kp = 0.0005, 0.001, 0.005. Describe
# (comment) what too-low and too-high P feel like (slow vs. oscillating).
# ===========================================================================
def exercise_2():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 3
# Add D. Extend to pd_control(error, last_error, kp, kd, dt). Add D and
# re-run. Show that a good D reduces overshoot compared to P-only.
# ===========================================================================
def exercise_3():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 4
# Build the class. Write a MyPIDF class with __init__(kp, ki, kd, kf) and
# update(current, target) that tracks last_error, error_sum, and last_time —
# mirroring PIDFController.java. Return P+I+D+F.
# ===========================================================================
def exercise_4():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 5
# Integral windup reset. Add the "reset error_sum when error changes sign"
# rule to MyPIDF. Demonstrate with a target that the controller overshoots:
# show the integral getting reset.
# ===========================================================================
def exercise_5():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 6
# Drive to a heading with YOUR PID. Replace the hand-tuned error*gain turn
# from Chapter 4 with MyPIDF. Turn to 90°. Tune kp/kd until it settles
# within 1° without wild oscillation. Print the final heading.
# ===========================================================================
def exercise_6():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 7
# Lift to a height. Model a lift: ticks moves toward a target by your PID's
# output each loop. Use MyPIDF to drive it from 0 to 960 ticks (Juice's
# HIGH_RUNG value!). Print ticks every 10 loops; show it settles near 960.
# ===========================================================================
def exercise_7():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 8
# Feedforward vs gravity. Add a constant "gravity" that subtracts 5 ticks
# every loop (the lift sags). Show that without kf the lift settles *below*
# target, and adding kf (a constant up-push) fixes it. This is exactly why
# Lift.java adds ff = f.
# ===========================================================================
def exercise_8():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 9
# Compare to the real port. Run the sim's built-in PIDFController (the
# faithful Java port) and your MyPIDF on the same problem with the same
# gains. They should behave almost identically. Print both final values.
# ===========================================================================
def exercise_9():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 10
# Tune Juice's real lift gains. Lift.java uses p=0.02, i=0.0, d=0.00045,
# f=0.125. Plug those into your controller for the 0→960 lift and see how it
# behaves. Then try to beat it (faster settle, less overshoot) by adjusting
# d. Report your best gains and why they're better. (This is the actual job
# of a Juice software member.)
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
