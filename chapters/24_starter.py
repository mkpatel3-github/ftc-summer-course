"""
Chapter 24 — Advanced Command-Based: Bindings, Requirements & Conditionals

This is YOUR workspace. Read the matching lesson first:
    chapters/24-advanced-command-based.md

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/24_starter.py

Stuck? Try for real first, THEN peek at:
    solutions/24_solution.py
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

print("Chapter 24 - delete this line and start coding your exercises!\n")


# ===========================================================================
# Exercise 1
# Bind a button. Make a RunningCommandScheduler and a Button reading a flag
# you control. Bind it (when_pressed) to an InstantCommand that prints
# "FIRE". Flip the flag True and call sched.run(); show it fires. Set it
# back False, run again; show it does not re-fire. (Edge detection, for
# free.)
# ===========================================================================
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 2
# Only on the rising edge. Keep the flag True for 5 consecutive run() calls.
# Count how many times the command fires. Show it's exactly once — held
# buttons don't repeat. In a comment, contrast with polling the flag
# directly in a loop.
# ===========================================================================
def exercise_2():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 3
# Two buttons, two commands. Bind button A to "open" and button B to "close"
# (each an InstantCommand printing its name). Press A, then B, then A. Show
# the prints follow your presses. No was_pressed variables in your loop.
# ===========================================================================
def exercise_3():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 4
# A subsystem requirement. Make a Subsystem claw. Build two commands that
# both .requires(claw) but take several loops to finish (subclass Command,
# finish after N updates). Schedule the first, tick once, then schedule the
# second. Show the first is no longer scheduled (sched.is_scheduled) — the
# second cancelled it.
# ===========================================================================
def exercise_4():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 5
# No shared requirement, no cancel. Repeat exercise 4 but give the two
# commands different subsystems (claw and lift). Schedule both. Show both
# stay scheduled and run at the same time. In a comment: this is why
# requirements are per-subsystem, not global.
# ===========================================================================
def exercise_5():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 6
# ConditionalCommand basics. Make a claw_closed flag. Build a
# ConditionalCommand that runs "OPEN" when closed and "CLOSE" when open. Run
# it with the flag True, then False; show it picks the right branch each
# time based on the condition at init.
# ===========================================================================
def exercise_6():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 7
# A real toggle. Wire exercise 6 to a button so one button alternates
# open/close. Have each branch also flip the claw_closed flag. Press the
# button three times; show it goes closed→open→closed→open. This is a
# one-button toggle, the command-based way.
# ===========================================================================
def exercise_7():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 8
# Nested conditional (3-state). Mimic KookyBotz's ClawToggleCommand: a state
# variable that is "CLOSED", "OPEN", or "INTERMEDIATE", and a nested
# ConditionalCommand so one button cycles closed→intermediate→open→… Print
# the state after each press. In a comment, match it to the Java bridge
# above.
# ===========================================================================
def exercise_8():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 9
# Requirement during a sequence. Schedule a SequentialCommand (several
# steps, requires lift) and let it run a couple loops. Mid-sequence,
# schedule a different command that also requires lift. Show the sequence is
# cancelled and the new command takes over. Explain why this is the
# *correct* behavior for a driver who changes their mind mid-action.
# ===========================================================================
def exercise_9():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 10
# A tiny TeleOp. Put it together: a scheduler, two subsystems (drive, claw),
# a couple of buttons bound to commands, and a 30-loop "match" where you
# script some button presses by flipping flags on certain loops. Print what
# runs each loop. In a comment, map your loop body to KookyBotz's
# CommandScheduler.getInstance().run() and explain what you'd no longer have
# to hand-write compared to a Chapter 6 polling loop.
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
