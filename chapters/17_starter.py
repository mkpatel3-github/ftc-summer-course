"""
Chapter 17 — Robot Architecture: One Home for Hardware

This is YOUR workspace. Read the matching lesson first:
    chapters/17-robot-architecture.md

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/17_starter.py

Stuck? Try for real first, THEN peek at:
    solutions/17_solution.py
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

print("Chapter 17 - delete this line and start coding your exercises!\n")


# ===========================================================================
# Exercise 1
# A singleton. Write a RobotHardware class with a get_instance() classmethod
# that caches and returns one shared instance. Call it twice, store both,
# and prove they are the same object (a is b is True).
# ===========================================================================
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 2
# Own the hardware. Give RobotHardware an __init__ that creates a sim
# Robot() and stores it as self.robot. Add a drive(x, y, rx) method that
# forwards to self.robot.set_drive_power(...). Drive forward 1s through the
# singleton; print the pose.
# ===========================================================================
def exercise_2():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 3
# A Globals file. Make a Globals class with named constants: LIFT_GROUND=0,
# LIFT_LOW=800, LIFT_HIGH=1600, CLAW_OPEN=0.6, CLAW_CLOSED=0.2. Print all
# five.
# ===========================================================================
def exercise_3():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 4
# Use the names, not the numbers. Write a function lift_preset(name) that
# takes "GROUND", "LOW", or "HIGH" and returns the matching Globals
# constant. Show that changing Globals.LIFT_HIGH to a new value changes the
# result without touching lift_preset. (This is the payoff of the pattern.)
# ===========================================================================
def exercise_4():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 5
# Enums in Globals. Add an ALLIANCE constant and a helper scoring_x() that
# returns a +x target for RED and a −x target for BLUE. Flip
# Globals.ALLIANCE and show the target mirrors — one constant changes the
# whole robot's autonomous side.
# ===========================================================================
def exercise_5():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 6
# No more copy-paste. Write two "OpModes" as functions — teleop() and
# auton() — that both get the robot from RobotHardware.get_instance(). Show
# they share the same hardware object (drive in one, read the pose in the
# other).
# ===========================================================================
def exercise_6():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 7
# Reverse once. Add a reverse_left_side() method on RobotHardware that flips
# the left motors' reverse flag. In a comment, explain why doing this in the
# singleton (instead of in each OpMode) prevents the classic "works in
# TeleOp, broken in auto" bug.
# ===========================================================================
def exercise_7():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 8
# A subsystem reads from the singleton. Write a Lift class whose constructor
# takes the RobotHardware instance and uses Globals presets in a go_to(name)
# method. Notice the Lift never touches hardwareMap/Robot directly — it goes
# through the singleton.
# ===========================================================================
def exercise_8():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 9
# Telemetry data class. Solvers keep a TelemetryData holder. Make a small
# class that stores the robot's mode, alliance, and pose, with a
# show(telemetry) method that prints them. Use it from your teleop()
# function.
# ===========================================================================
def exercise_9():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 10
# Refactor a mess. Below (write it first) is a "bad" version: a function
# that calls Robot() itself and uses bare numbers 0.6, 1600. Refactor it to
# use RobotHardware.get_instance() and Globals. In a comment, list every
# benefit you gained.
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
