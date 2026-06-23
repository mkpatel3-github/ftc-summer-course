"""
Chapter 2 — Motors & Power

This is YOUR workspace. Read the matching lesson first:
    chapters/02-motors-and-power.md

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/02_starter.py

Stuck? Try for real first, THEN peek at:
    solutions/02_solution.py
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

print("Chapter 02 - delete this line and start coding your exercises!\n")


# ===========================================================================
# Exercise 1
# Spin one wheel. Set front_left to power 0.5, step the sim 50 times, and
# print the wheel's encoder value. (Just see a number grow.)
# ===========================================================================
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 2
# Clamp it. Set a wheel to power 2.0. Print robot.front_left.speed. What
# number did it actually store? Explain in a comment why it's not 2.0.
# ===========================================================================
def exercise_2():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 3
# Forward and back. Drive the robot forward at full power for 1 second,
# print the pose, then backward for 1 second, and print again. Did x (or y)
# return near start? (Use set_drive_power(0, 1.0, 0) then (0, -1.0, 0).)
# ===========================================================================
def exercise_3():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 4
# Half vs full. Drive forward at 0.5 for 2s and at 1.0 for 1s. Compare the
# distance traveled (print both poses). Should they be similar — why or why
# not?
# ===========================================================================
def exercise_4():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 5
# The reverse flag. Make two motors, one reverse=False and one reverse=True.
# Give both set_speed(0.5). Print both .speed values. Explain what reverse
# did.
# ===========================================================================
def exercise_5():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 6
# A drive_power helper. Write a Python function drive(robot, power, seconds)
# that drives straight at power for seconds using run_for. Use it to drive
# forward 1.5s. (You're packaging a behavior into a function — this is what
# Motor methods do.)
# ===========================================================================
def exercise_6():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 7
# Strafe. Mecanum wheels can slide sideways. Drive with set_drive_power(1.0,
# 0, 0) (that's the x/strafe input) for 1 second and print the pose. Which
# coordinate changed?
# ===========================================================================
def exercise_7():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 8
# Spin in place. Drive with set_drive_power(0, 0, 0.5) for 1 second. Print
# the heading. How many degrees did it turn? Now do rx = -0.5 and confirm it
# turns the other way.
# ===========================================================================
def exercise_8():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 9
# Clamp helper (write it yourself). Without using the sim's clamp, write
# your own Python function clamp(value, lo=-1.0, hi=1.0) that returns the
# value limited to the range. Test it on 2.0, -3.0, and 0.4. (This exact
# idea appears all over robot code.)
# ===========================================================================
def exercise_9():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 10
# Normalize four powers (Juice's real trick). In Robot.java, after computing
# four wheel powers, Juice finds the biggest absolute value; if it's over
# 1.0, it divides *all four* by that max so the ratios stay the same but
# nothing exceeds 1.0. Write a Python function normalize([fl, fr, bl, br])
# that does this and return the new list. Test it on [1.5, -0.5, 1.0, 0.2].
# Compare your code to lines 682–696 of Robot.java.
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
