"""
Chapter 11 — Crossing to Java

This is YOUR workspace. Read the matching lesson first:
    chapters/11-crossing-to-java.md

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/11_starter.py

Stuck? Try for real first, THEN peek at:
    solutions/11_solution.py
"""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
# Everything from the simulator you might need:
from ftcsim import (Robot, Field, Gamepad, IMU, Motor, StepperServo,
                    PIDFController, run_for, Pose2d, AprilTag, Odometry, Camera,
                    Command, InstantCommand, SequentialCommand, ParallelCommand,
                    SleepCommand, CommandScheduler, DriveToPoseAction,
                    SequentialAction, run_action)

print("Chapter 11 - delete this line and start coding your exercises!\n")


# ===========================================================================
# Exercise 1
# Type tags. Convert these three Python lines to Java, with the right type
# and a semicolon each: wheels = 4, power = 0.6, name = "Juice".
# ===========================================================================
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 2
# An if/else. Convert this to Java (braces and parentheses): if speed > 1.0:
# / speed = 1.0 / else: / speed = speed. (This is clamping.)
# ===========================================================================
def exercise_2():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 3
# A for loop. Python for i in range(4): printing i. Write the Java for (int
# i = 0; i < 4; i++) { ... } version that does the same.
# ===========================================================================
def exercise_3():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 4
# A method signature. Convert def clamp(power): that returns a clamped value
# into a Java method header: double clamp(double power) { ... }. Write the
# whole method.
# ===========================================================================
def exercise_4():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 5
# The drive formula. Take wheel_powers(x, y, rx) from Chapter 6 and write it
# in Java: four double variables using Juice's exact formula, ending in
# semicolons.
# ===========================================================================
def exercise_5():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 6
# snake → camel. Rename each to Java style: set_drive_power,
# get_encoder_value, reset_heading, left_stick_y, is_red_alliance. (One of
# these stays the same in FTC — which, and why? Hint: gamepad fields.)
# ===========================================================================
def exercise_6():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 7
# A telemetry block. Convert a 3-line Python telemetry print (MODE, pose,
# loop) into Java telemetry.addData(...) calls followed by
# telemetry.update();.
# ===========================================================================
def exercise_7():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 8
# Wrap a loop in an OpMode. Take your Chapter 6 mini-TeleOp loop body and
# write the full runOpMode() skeleton around it (class header,
# waitForStart(), the while (opModeIsActive()) loop). The loop body can stay
# as a // ... comment.
# ===========================================================================
def exercise_8():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 9
# A whole subsystem. Convert your Chapter 8 Lift class (constructor +
# set_target + update) into a Java class sketch: public class Lift { ... }
# with typed fields and methods. Logic in comments is fine; get the *shape*
# right.
# ===========================================================================
def exercise_9():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 10
# Spot the bugs. Here is Java with four beginner mistakes. In a comment,
# list each bug and the fix: java public void drive(double x double y) {
# double power = x + y if power > 1 { power = 1; }
# telemetry.addData("power", power) }
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
