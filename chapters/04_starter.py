"""
Chapter 4 — The Gyro (IMU)

This is YOUR workspace. Read the matching lesson first:
    chapters/04-the-gyro-imu.md

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/04_starter.py

Stuck? Try for real first, THEN peek at:
    solutions/04_solution.py
"""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
# Everything from the simulator you might need:
from ftcsim import (Robot, Field, Gamepad, IMU, Motor, StepperServo,
                    PIDFController, run_for, Pose2d, AprilTag, Odometry, Camera,
                    Command, InstantCommand, SequentialCommand, ParallelCommand,
                    SleepCommand, CommandScheduler, DriveToPoseAction,
                    SequentialAction, run_action)

print("Chapter 04 - delete this line and start coding your exercises!\n")


# ===========================================================================
# Exercise 1
# Read heading. Reset heading, spin at rx=0.4 for 0.5s, print the heading.
# ===========================================================================
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 2
# Angle difference (naive). Write angle_error(target, current) = target -
# current. Test angle_error(90, 0) → 90. Then test angle_error(-170, 170) →
# −340. Note in a comment why −340 is "wrong" for a robot (it would spin
# almost all the way around).
# ===========================================================================
def exercise_2():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 3
# Angle difference (smart). Write angle_wrap(error) that maps any angle into
# −180..180 (hint: ((error + 180) % 360) - 180). Now
# angle_wrap(angle_error(-170, 170)) should give +20. Test several values.
# ===========================================================================
def exercise_3():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 4
# Turn to angle. Write turn_to(robot, target_deg) using the loop pattern:
# while the (wrapped) error is bigger than ~2°, turn in the sign of the
# error; then stop. Turn to +90, print heading. Turn to −45, print heading.
# ===========================================================================
def exercise_4():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 5
# Turn both directions. From heading 0, turn_to(+90), then turn_to(-90),
# printing after each. Confirm it goes left then right (not the long way
# around).
# ===========================================================================
def exercise_5():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 6
# Proportional turn (smoother). Improve turn_to so the turn power is error *
# gain (try gain = 0.02), clamped to ±0.5. It should slow down as it
# approaches the target instead of slamming on. Compare overshoot to
# exercise 4.
# ===========================================================================
def exercise_6():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 7
# Gyro-straight. Write drive_straight(robot, inches, power=0.5) that drives
# forward by *encoder distance* (Chapter 3) and corrects heading toward 0
# each loop using rx = angle_wrap(0 - heading) * 0.03. Drive 36 inches and
# print the final heading (should stay near 0).
# ===========================================================================
def exercise_7():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 8
# Push test. Our sim drives perfectly straight, so simulate a "push": inside
# the loop, every 25 steps add a small heading disturbance with
# robot.heading += 5. Run drive_straight with the correction ON, then with
# it OFF (rx=0). Compare final headings. This is exactly why gyro-straight
# matters.
# ===========================================================================
def exercise_8():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 9
# Drive straight on a heading. Generalize drive_straight to take a
# target_heading argument so the robot can drive straight while *facing*
# +30°. Drive 24 inches on heading +30 and confirm it holds +30.
# ===========================================================================
def exercise_9():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 10
# Combine: an L-path. Drive straight 24 inches on heading 0, turn_to(90),
# then drive straight 24 inches on heading 90. Print the pose. You just did
# encoder distance + gyro turn + gyro-straight together — the backbone of a
# real autonomous.
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
