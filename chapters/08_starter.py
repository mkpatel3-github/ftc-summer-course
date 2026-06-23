"""
Chapter 8 — Subsystems & State Machines

This is YOUR workspace. Read the matching lesson first:
    chapters/08-subsystems-and-state-machines.md

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/08_starter.py

Stuck? Try for real first, THEN peek at:
    solutions/08_solution.py
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

print("Chapter 08 - delete this line and start coding your exercises!\n")


# ===========================================================================
# Exercise 1
# A Claw class. Write a Claw class with is_open state and methods open(),
# close(), and status() (returns "OPEN"/"CLOSED"). This mirrors Claw.java's
# start/stop intake. Use it; print status before and after closing.
# ===========================================================================
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 2
# Encapsulate a Lift. Write a Lift class wrapping a MyPIDF (from Ch.7) and a
# ticks value. Methods: run_to_position(target), update() (one PID step),
# get_pos(). Drive it to 1000 and loop update() until it settles.
# ===========================================================================
def exercise_2():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 3
# The Levels enum. Use Python's enum to recreate a trimmed Levels: INIT,
# INTAKE, INTERMEDIATE, LOW_BASKET, HIGH_BASKET, LOW_RUNG, HIGH_RUNG. Print
# all of them.
# ===========================================================================
def exercise_3():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 4
# Lift presets. Give Lift a run_to_preset(level) method that maps each
# Levels value to a target tick count (use Juice's real numbers:
# HIGH_BASKET=2160, HIGH_RUNG=960, INTAKE=-15, others 0). Send it to
# HIGH_BASKET and settle.
# ===========================================================================
def exercise_4():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 5
# A Robot with a state. Write a small Robot wrapper class holding a lift and
# a state field (a Levels). Methods high_basket() and high_rung() that set
# BOTH the lift preset AND self.state. Verify state updates when you call
# them.
# ===========================================================================
def exercise_5():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 6
# smartOuttake. Add smart_outtake() that returns "DROP SAMPLE" if state is a
# basket, "RELEASE SPECIMEN" if state is a rung, else "NOTHING". Test it
# after calling high_basket() and after high_rung(). (This is the real
# smartOuttake logic.)
# ===========================================================================
def exercise_6():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 7
# toggleGamepiece. Add a mode ("SAMPLE"/"SPECIMEN") and a toggle_gamepiece()
# method that flips it (mirror Robot.toggleGamepiece). Also add
# tele_deposit_preset() that calls high_basket() if mode is SAMPLE else
# high_rung(). Test both modes.
# ===========================================================================
def exercise_7():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 8
# Legal transitions. Not every state can follow every other. Write a
# can_transition(from_state, to_state) using a dictionary of allowed
# next-states (e.g. from INTAKE you can go to INTERMEDIATE; from
# INTERMEDIATE to any scoring level; you can't jump straight
# INTAKE→HIGH_BASKET). Test a legal and an illegal transition.
# ===========================================================================
def exercise_8():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 9
# Full sequence. Drive the state machine through a realistic scoring cycle:
# INIT → INTAKE → INTERMEDIATE → HIGH_BASKET → (smart_outtake) →
# INTERMEDIATE. At each step print the state and, for scoring states, the
# lift target. Reject any illegal transition using exercise 8.
# ===========================================================================
def exercise_9():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 10
# Design your own subsystem. Pick a mechanism from a real FTC game (an
# intake, a shooter, a hanger). On paper/comment: list its states, its
# hardware (motors/servos/ sensors), and the public methods you'd expose.
# Then implement a minimal version as a Python class with at least 2 states
# and a update()/status(). This is exactly the first thing you'll do on
# Juice for a new season.
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
