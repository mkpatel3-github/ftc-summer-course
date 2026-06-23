"""
Chapter 21 — Sensor Fusion & the Kalman Filter

This is YOUR workspace. Read the matching lesson first:
    chapters/21-sensor-fusion-kalman.md

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/21_starter.py

Stuck? Try for real first, THEN peek at:
    solutions/21_solution.py
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

print("Chapter 21 - delete this line and start coding your exercises!\n")


# ===========================================================================
# Exercise 1
# Build your own. Write the MyKalman class from the lesson. Run update(5, 4)
# once from a 0 start and print the result. Compare it to the sim's
# KalmanFilter(q,r) with the same Q/R — they should match.
# ===========================================================================
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 2
# Trust knobs. With your filter, fuse the same inputs (model_delta=10,
# measurement=0) twice: once with a large R (trust sensor little) and once
# with a small R (trust sensor a lot). Print both outputs and explain the
# difference in a comment.
# ===========================================================================
def exercise_2():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 3
# Smooth a noisy signal. Feed your filter a sequence of noisy measurements
# of a value that's really 50 (e.g. 48, 53, 49, 51, 47...) with
# model_delta=0 each step. Print the estimate converging toward 50 and
# staying steady — the filter is smoothing.
# ===========================================================================
def exercise_3():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 4
# See the drift. Drive forward 2s with robot.odometry.drift_per_read = 0.05.
# Print the odometry pose's x vs the true robot.x. Show odometry now reads
# too high — that's accumulated drift.
# ===========================================================================
def exercise_4():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 5
# See the noise. With robot.camera.noise = 1.0 and tags placed, read
# robot.camera.localize().x five times without moving. Show it jumps around
# the true value — absolute but jittery.
# ===========================================================================
def exercise_5():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 6
# Fuse x, one step. Each loop you have: model_delta = how far odometry
# *says* x moved this step, and measurement = the camera's x. Fuse them with
# a KalmanFilter for one step and print the fused x. (You're combining
# exercises 4 and 5.)
# ===========================================================================
def exercise_6():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 7
# Fuse over a whole drive. Drive forward 2s. Each loop, feed the Kalman
# filter the odometry delta (predict) and the camera x (correct). Print, at
# the end, the fused x, the raw odometry x, and the true x. Show fused is
# closer to true than drifting odometry.
# ===========================================================================
def exercise_7():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 8
# Tune Q and R. Repeat exercise 7 with three (Q, R) settings:
# trust-camera-heavy, trust-odometry-heavy, and balanced. Print the final
# error for each. Find the one that's smoothest *and* accurate. In a
# comment, relate Q/R tuning to PID gain tuning.
# ===========================================================================
def exercise_8():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 9
# Camera drops out. Realistic case: the camera only sees a tag for part of
# the drive. When localize() returns None, skip the correct step (predict
# only). Show the fused estimate coasts on odometry during the blackout and
# re-snaps when the tag reappears.
# ===========================================================================
def exercise_9():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 10
# Two-axis fusion. Run two Kalman filters — one for x, one for y — to fuse a
# full 2D position over a forward+strafe path. Print the fused (x, y) vs
# true (x, y). In a comment, note this is exactly how j5155's
# Vector2dKalmanFilter composes two 1-D filters, and how Juice's KalmanDrive
# keeps its pose honest all match.
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
