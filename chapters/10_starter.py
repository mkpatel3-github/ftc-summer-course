"""
Chapter 10 — Capstone: Solve a Mission

This is YOUR workspace. Read the matching lesson first:
    chapters/10-capstone-mission.md

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/10_starter.py

Stuck? Try for real first, THEN peek at:
    solutions/10_solution.py
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

print("Chapter 10 - delete this line and start coding your exercises!\n")


# ===========================================================================
# Exercise 1
# Restate the mission. In a comment, list every job the robot must do and
# which chapter's tool solves it. (No code — this is step 1–3 of the loop.)
# ===========================================================================
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 2
# Robot scaffold. Make a robot at start pose (-36, -60, 90) and a score = 0
# counter. Print the starting state.
# ===========================================================================
def exercise_2():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 3
# Visit one cell. Use drive_to_pose to drive to the first cell's pose.
# Confirm you arrived (distance < 4 in).
# ===========================================================================
def exercise_3():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 4
# Identify the cell. At the cell, read the color (the mission tells the sim
# what color is there). Decide keep/reject for the BLUE alliance using your
# Chapter 5 should_keep logic. Print the decision.
# ===========================================================================
def exercise_4():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 5
# Deliver or skip. If the cell should be kept, drive_to_pose to the Depot
# (48,48) and add +5 to score. If it's red, skip it (don't deliver) and
# print "rejected red". Do this for the first cell.
# ===========================================================================
def exercise_5():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 6
# Loop all three cells. Wrap exercises 3–5 in a loop over all three cells.
# Tally the score. Print a line per cell (cell 2 BLUE -> delivered +5).
# ===========================================================================
def exercise_6():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 7
# Park for points. After the cells, drive_to_pose to a parking spot on the
# center line (x≈0). Add +10. Print final score.
# ===========================================================================
def exercise_7():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 8
# Respect the clock. Add a 30-second budget (like Chapter 9). If delivering
# all three cells would blow the budget, skip the farthest one and still
# park. Print which cells were skipped and why. (Real strategic decision!)
# ===========================================================================
def exercise_8():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 9
# Full autonomous, as a sequence. Refactor your whole solution into a step
# list run by run_sequence (Chapter 9) + subsystem/state usage (Chapter 8) —
# so it reads like BucketSide.java: a clean ordered list of named actions.
# Run it end to end.
# ===========================================================================
def exercise_9():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 10
# Reflect + translate. (a) In a comment, write what you'd change to score
# more (faster paths? carry multiple cells?). (b) Pick ONE method from your
# solution and write its Java version in a comment, using Juice's patterns
# (setDrivePower, runToPreset, SequentialAction). This is the Python→Java
# bridge you'll cross for real when the season starts.
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
