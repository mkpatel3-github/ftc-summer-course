"""
Chapter 5 — Sensors & Line Following

This is YOUR workspace. Read the matching lesson first:
    chapters/05-sensors-and-line-following.md

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/05_starter.py

Stuck? Try for real first, THEN peek at:
    solutions/05_solution.py
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

print("Chapter 05 - delete this line and start coding your exercises!\n")


# ===========================================================================
# Exercise 1
# Read the sensor. Put a BLUE sample at (10, 0). Drive the robot to it
# (forward) and print red(), green(), blue() once it's on top. Note which
# channel is high.
# ===========================================================================
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 2
# detect_color v1. Write detect_color(robot) that returns "BLUE" if blue is
# the biggest channel, else None. Test on a blue sample and on empty floor.
# ===========================================================================
def exercise_2():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 3
# Fix Juice's bug. Extend detect_color to return "RED", "BLUE", or "YELLOW"
# correctly: yellow = red high AND green high AND blue low; otherwise
# whichever of red/blue is bigger. Test all three colors by changing
# f.sample_color.
# ===========================================================================
def exercise_3():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 4
# Alliance filter. Write should_keep(color, alliance) — Juice keeps a sample
# if it's YELLOW or matches the alliance color, else ejects it. Mirror the
# idea from Claw.smartStopDetect: return 1 (keep), -1 (eject), or 0
# (nothing). Test for a RED alliance seeing each color.
# ===========================================================================
def exercise_4():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 5
# Drive until you see it. Write a loop that drives forward until
# detect_color returns non-None, then stops. Print where it stopped.
# (Sensor-driven stopping — like intaking until a game piece is detected.)
# ===========================================================================
def exercise_5():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 6
# Distance stop. Using robot.distance.get_distance() (inches to the front
# wall), drive forward until you're 12 inches from the wall, then stop.
# Print the final distance.
# ===========================================================================
def exercise_6():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 7
# Wall follow / approach (proportional). Instead of a hard stop, slow down
# smoothly: drive with power = (distance - 12) * 0.05, clamped to 0..0.6,
# until distance is ~12. Compare the stopping smoothness to exercise 6.
# ===========================================================================
def exercise_7():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 8
# Line following — set up. Our Field has a black line at x = line_x. Write a
# helper on_line(robot) that returns True when the robot's x is within
# line_half_width of line_x. (Pretend this is a downward light sensor
# reading dark.)
# ===========================================================================
def exercise_8():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 9
# Line following — follow it. The line runs along x=0 up the field. Drive
# forward (+y) while steering to keep x near 0: rx-style correction using
# error = 0 - robot.x. Start the robot at x=4 and show it converges back
# toward x≈0 as it drives up the field. (This is the same
# proportional-control shape again!)
# ===========================================================================
def exercise_9():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 10
# Mission: sort a sample. Put a sample of a random color in front of the
# robot. Drive to it, detect its color, decide keep/eject for the BLUE
# alliance, and print a clear action line (KEEP blue or EJECT red). This
# mirrors exactly what Juice's intake does during a match.
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
