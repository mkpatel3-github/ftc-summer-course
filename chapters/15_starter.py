"""
Chapter 15 — Command-Based Programming

This is YOUR workspace. Read the matching lesson first:
    chapters/15-command-based-programming.md

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/15_starter.py

Stuck? Try for real first, THEN peek at:
    solutions/15_solution.py
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

print("Chapter 15 - delete this line and start coding your exercises!\n")


# ===========================================================================
# Exercise 1
# Your first command. Write a DriveForward(Command) like the example. Run it
# with the scheduler for 1s and print the pose. Confirm the robot moved and
# then stopped (end()).
# ===========================================================================
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 2
# InstantCommand. Use InstantCommand(lambda: print("CLAW OPEN")) and run it.
# Confirm it prints once and finishes immediately.
# ===========================================================================
def exercise_2():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 3
# SleepCommand. Run a SequentialCommand(InstantCommand(print "start"),
# SleepCommand(0.5), InstantCommand(print "end")). Confirm "start" then a
# pause then "end".
# ===========================================================================
def exercise_3():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 4
# Sequential drive. Build a SequentialCommand that drives forward 1s, then
# strafes 1s (write a Strafe command). Print the pose after — it should show
# both legs.
# ===========================================================================
def exercise_4():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 5
# Parallel actions. Write a Spin command (sets rx) and run ParallelCommand(
# DriveForward(robot, 1.0), Spin(robot, 1.0)). Show the robot both moved
# *and* rotated — something a plain sequence can't do in the same second.
# ===========================================================================
def exercise_5():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 6
# "Done yet?" logic. Write a DriveToX(robot, target_x) command whose
# update() returns True only when robot.x >= target_x. Run it and confirm it
# stops near the target, not after a fixed time. (Commands end on a
# *condition*, not a clock.)
# ===========================================================================
def exercise_6():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 7
# Compose a mini-auto. Combine your commands into a SequentialCommand that:
# drives to x=30, then in parallel (drives a bit + prints "LIFT UP"), then
# an InstantCommand prints "SCORE". Read it out loud — does the code match
# the sentence?
# ===========================================================================
def exercise_7():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 8
# Reuse. Show off the payoff: build *two* different autos from the same
# command classes (e.g. a "left" routine and a "right" routine) without
# rewriting the commands. In a comment, note how this compares to
# copy-pasting loop code.
# ===========================================================================
def exercise_8():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 9
# A LoopCommand. Juice has LoopCommand.java. Write a LoopCommand(fn, times)
# that calls fn once per update() and finishes after times updates. Use it
# to print a countdown 3,2,1. (This is how you fold repeated behavior into
# the scheduler.)
# ===========================================================================
def exercise_9():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 10
# State machine vs commands. In a comment, compare Chapter 8's Levels state
# machine with command-based: when is a simple enum state machine *enough*,
# and when do commands earn their complexity? (Hint: number of subsystems
# acting at once.) Both are correct tools — explain how you'd choose.
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
