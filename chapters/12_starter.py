"""
Chapter 12 — Field-Centric Driving

This is YOUR workspace. Read the matching lesson first:
    chapters/12-field-centric-driving.md

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/12_starter.py

Stuck? Try for real first, THEN peek at:
    solutions/12_solution.py
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

print("Chapter 12 - delete this line and start coding your exercises!\n")


# ===========================================================================
# Exercise 1
# Same when facing forward. With the robot at heading 0, drive (x=0, y=1)
# field-centric for 1s, then reset and drive the same robot-centric. Show
# the final pose is (about) the same — at heading 0 the two are identical.
# ===========================================================================
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 2
# The spin test. Turn the robot to heading 90 first (use run_for with rx).
# Then drive (0, 1) *robot-centric* for 1s and print the pose. Notice it
# strafed sideways in field terms — not what the driver wanted.
# ===========================================================================
def exercise_2():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 3
# Field-centric fixes it. Same setup: turn to heading 90, then drive (0, 1)
# *field-centric* for 1s. Show it moves in +y (downfield) like the driver
# intended, even though the robot's nose points sideways.
# ===========================================================================
def exercise_3():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 4
# Write the rotation yourself. Don't call the built-in. Write
# rotate_stick(x, y, heading_deg) that returns (x_robot, y_robot) using the
# formula above. Test it: at heading 90, (0, 1) should come out close to (1,
# 0) or (-1, 0) (figure out the sign and explain it).
# ===========================================================================
def exercise_4():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 5
# Drive a square, field-centric. Without ever turning the robot, drive a
# square: +y 1s, +x 1s, −y 1s, −x 1s, all field-centric. The robot's heading
# should stay ~0 the whole time while it traces a box. (Mecanum +
# field-centric = strafing a square.)
# ===========================================================================
def exercise_5():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 6
# Heading reset button. Simulate the driver pressing a "reset heading"
# button: turn the robot to 90, then call robot.imu.reset_heading(), then
# drive (0,1) field-centric. After reset, "forward" should follow the
# robot's *current* nose. Explain in a comment when a driver would press
# this.
# ===========================================================================
def exercise_6():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 7
# Compare distance. For both modes, turn the robot 45° first, then drive
# (0,1) for 1s. Print both final poses side by side and describe the
# difference in plain English.
# ===========================================================================
def exercise_7():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 8
# Slow + field-centric. Combine Chapter 6's slow mode (×0.3 on a bumper)
# with field-centric driving. Show one second of normal vs slow covers
# different distance, both field-centric.
# ===========================================================================
def exercise_8():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 9
# A full field-centric TeleOp. Write a run_for loop with a scripted gamepad
# that: reads sticks, drives field-centric, and resets heading when a button
# is pressed once (edge-detected, Chapter 6). Print telemetry every 25
# loops: heading + pose.
# ===========================================================================
def exercise_9():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 10
# Why not always field-centric? In a comment, list two situations where a
# driver might *prefer* robot-centric (hint: lining up to a wall/board, or
# if the IMU drifts), and describe how a team lets the driver toggle between
# the two modes with one button.
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
