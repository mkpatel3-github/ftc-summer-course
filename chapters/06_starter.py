"""
Chapter 6 — Mecanum TeleOp

This is YOUR workspace. Read the matching lesson first:
    chapters/06-mecanum-teleop.md

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/06_starter.py

Stuck? Try for real first, THEN peek at:
    solutions/06_solution.py
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

print("Chapter 06 - delete this line and start coding your exercises!\n")


# ===========================================================================
# Exercise 1
# Joystick to motion. Make a gamepad, set left_stick_y = -1.0 (sticks are
# inverted — up is negative!), and in a run_for loop call
# robot.set_drive_power(-gp.left_stick_x, -gp.left_stick_y,
# gp.right_stick_x) for 1s. Confirm the robot drove forward.
# ===========================================================================
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 2
# Strafe with the stick. Set left_stick_x = 1.0 (and y=0, rx=0). Drive 1s.
# Which field coordinate changed? (This is strafing.)
# ===========================================================================
def exercise_2():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 3
# Rotate with the stick. Set right_stick_x = 0.5, drive 1s, print heading.
# ===========================================================================
def exercise_3():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 4
# Diagonal. Set left_stick_x and left_stick_y both so the robot drives at a
# 45° diagonal. Predict, then check the pose.
# ===========================================================================
def exercise_4():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 5
# Wheel-power inspector. Write wheel_powers(x, y, rx) that returns the four
# powers using Juice's exact formula. Print the powers for pure forward
# (0,1,0), pure strafe (1,0,0), and pure spin (0,0,1). Notice which wheels
# flip sign.
# ===========================================================================
def exercise_5():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 6
# Edge detector. Write a class or function that, given the current and
# previous button state, returns True only on the rising edge. Simulate a
# button "held" for 5 loops and show your detector fires exactly once.
# ===========================================================================
def exercise_6():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 7
# Button does a thing. In a TeleOp loop, when gamepad.a goes from
# False→True, toggle a mode variable between "SAMPLE" and "SPECIMEN" (like
# Juice's toggleGamepiece). Script the gamepad so a is pressed on loops 10
# and 30, and print mode each time it changes. It should toggle twice, not
# 20 times.
# ===========================================================================
def exercise_7():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 8
# Full driver sim. Combine: drive forward for the first second (stick), then
# strafe right for the next second, then spin for the last second — all in
# one run_for. Use the elapsed time t that loop_fn receives to decide which
# phase you're in. Print the pose at the end.
# ===========================================================================
def exercise_8():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 9
# Slow mode. Real drivers hold a bumper for precision ("slow mode"). When
# gamepad.right_bumper is held, multiply all drive inputs by 0.3. Show the
# robot covers less distance in 1s with slow mode on vs off.
# ===========================================================================
def exercise_9():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 10
# Mini TeleOp like Juice. Write a loop that: reads the sticks for driving,
# uses edge detection so a toggles scoring mode and b "ejects" (just print
# "EJECT"), and every loop prints a 3-line telemetry (MODE, pose, loop
# count) in the style of TeleOpMainRed. Run it for 2 seconds with a scripted
# gamepad. This is a real TeleOp in miniature.
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
