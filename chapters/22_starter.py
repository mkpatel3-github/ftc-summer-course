"""
Chapter 22 — The Tuning Workflow: @Config, Dashboard, and a Method

This is YOUR workspace. Read the matching lesson first:
    chapters/22-tuning-workflow.md

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/22_starter.py

Stuck? Try for real first, THEN peek at:
    solutions/22_solution.py
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

print("Chapter 22 - delete this line and start coding your exercises!\n")


# ===========================================================================
# Exercise 1
# Build the bench. Write run_gains(kp, kv) from the lesson (profile
# distance=1000, max_v=500, accel=decel=1000). Call it once with kp=0.5,
# kv=0 and print the max tracking error. This is your "one dashboard run".
# ===========================================================================
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 2
# Sweep kP. Call run_gains for kp in [0.1, 0.5, 1, 2, 5, 10] (kv=0). Print
# each kp and its error. Identify the kp with the lowest error — that's what
# dragging the slider finds for you.
# ===========================================================================
def exercise_2():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 3
# Too much kP. Keep raising kp well past the best value from exercise 2 (try
# 100, 105, 110). Track the error's sign over time and count sign flips.
# Show that past a threshold the error stops shrinking and starts
# oscillating (the sign flips repeatedly, the value blows up). In a comment:
# this is why you stop *before* the buzz.
# ===========================================================================
def exercise_3():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 4
# Feedforward first. Set kp=0 and sweep kv in [0, 0.25, 0.5, 1.0, 1.5].
# Print the error for each. Show a good kv alone (no PID!) already tracks
# the profile well — the reason teams tune FF *before* PID. (For this plant
# the sweet spot is near kv=1.0.)
# ===========================================================================
def exercise_4():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 5
# FF + PID together. PID alone can only track well by cranking kp
# dangerously high (near the oscillation threshold from exercise 3). Show
# the better way: pick a gentle, safe kp (e.g. 5) and compare its error
# *without* feedforward vs *with* your best kv from exercise 4. Show FF
# makes the gentle kp track well — so you never have to live near
# instability. In a comment, restate the tuning order (FF, then P, then D,
# then I).
# ===========================================================================
def exercise_5():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 6
# One variable at a time. Demonstrate the cardinal rule: do a run where you
# change kp and kv at once and it gets better — then argue (in a comment)
# why you can't tell which one helped. Contrast with the single-variable
# sweeps above.
# ===========================================================================
def exercise_6():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 7
# Score, don't eyeball. Extend the bench to also return settling time (first
# time the error drops under 1% of distance and stays). Print both max-error
# and settling-time for three kp values. Show "better" can be two numbers
# that trade off.
# ===========================================================================
def exercise_7():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 8
# A coarse-to-fine search. Find the best kp in two passes: first a coarse
# sweep ([1, 10, 100]), then a fine sweep around the coarse winner — staying
# below the oscillation threshold (e.g. 40, 50, 60, 75). Print the refined
# best. This is how you tune fast without testing a thousand values (and
# without blowing past the stability edge).
# ===========================================================================
def exercise_8():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 9
# Simulate the slow way's cost. You have 6 candidate kp values. Print the
# wall-clock cost of tuning them on a real robot at 90 s per
# build-deploy-test vs. live on the dashboard at 5 s per slider try. (Just
# arithmetic.) Show why @Config exists.
# ===========================================================================
def exercise_9():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 10
# Write your tuning playbook. In a comment block, write the step-by-step
# procedure your team will follow to tune a new profiled mechanism from
# scratch: which constant first, what you watch, when you move on, when
# you're done. Reference the order from the lesson and the single-variable
# rule. This is the deliverable a top team actually keeps in their repo.
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
