"""
Chapter 25 — Path Following: Pure Pursuit (and a Peek at GVF)

This is YOUR workspace. Read the matching lesson first:
    chapters/25-path-following.md

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/25_starter.py

Stuck? Try for real first, THEN peek at:
    solutions/25_solution.py
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

print("Chapter 25 - delete this line and start coding your exercises!\n")


# ===========================================================================
# Exercise 1
# Build a path, find the projection. Make a Path with 4–5 waypoints in a
# gentle curve. Put the robot at the start and print
# path.closest_point(robot.x, robot.y). Move the robot a few inches down the
# path by hand (robot.x = ...) and print it again. Show the projection index
# advances as you move along the path.
# ===========================================================================
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 2
# See the carrot move. With the robot at the start, print
# path.lookahead_point(robot.x, robot.y, 8.0). Nudge the robot forward a few
# times and print the lookahead each time. Show the carrot slides forward
# along the path as you advance. (This is pure pursuit's whole idea in one
# print.)
# ===========================================================================
def exercise_2():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 3
# Follow a straight line. Make a Path from (0,0) to (30,0). Run a
# PurePursuitFollower in a run_for loop until .run() returns False. Print
# the robot's final (x, y). Show it arrives near (30, 0).
# ===========================================================================
def exercise_3():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 4
# Follow a curve. Make an L-shaped path like [(0,0),(10,0),(20,10),(20,20)].
# Follow it and print the final pose. Show the robot ends near (20, 20) — it
# tracked the corner without stopping at the middle waypoint.
# ===========================================================================
def exercise_4():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 5
# Small lookahead tracks tight. Follow the curve from exercise 4 with
# lookahead=2.0. Every few loops, print the robot's distance from the
# *nearest* path point (path.closest_point(...)[1]). Show the distance stays
# small — the robot hugs the path closely. In a comment, explain why a small
# lookahead tracks tightly here, *and* why on a real robot (with momentum)
# too small a value would instead make it overshoot and wobble.
# ===========================================================================
def exercise_5():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 6
# Lookahead too big cuts corners. Follow the same curve with lookahead=20.0.
# Track the max distance the robot ever gets from the path. Show it drifts
# *inside* the corner (large max distance) compared to a medium lookahead.
# In a comment: big lookahead = smooth but sloppy.
# ===========================================================================
def exercise_6():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 7
# Tune the lookahead. Run the curve with lookahead = 2, 6, 10, 16. For each,
# record the total path-tracking error (sum of closest_point distance each
# loop). Print a little table. Show error grows as lookahead grows
# (corner-cutting). Pick the value that best trades accuracy against
# smoothness — that's your tuned lookahead, same idea as tuning kp.
# ===========================================================================
def exercise_7():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 8
# Detect arrival. Use the .run() return value as your loop condition: keep
# calling it until it returns False, counting loops. Print the loop count
# and confirm the final distance to path.end() is within tol. Show the
# follower stops itself — you don't hand-pick a timeout.
# ===========================================================================
def exercise_8():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 9
# A two-leg autonomous. Chain two paths: follow path A to its end, then
# follow path B from there (build a second PurePursuitFollower). Print the
# pose after each leg. This is how an auto routine strings path segments —
# like RoadRunner's .splineTo(...).splineTo(...).
# ===========================================================================
def exercise_9():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 10
# Pure pursuit vs. GVF, in your own words. Follow a path and, each loop,
# print both the tangent direction (angle from the current closest point to
# the *next* waypoint) and the error distance (closest_point distance).
# Watch how the follower's steering is really "go along the path (tangent) +
# pull back onto it (error)." In a comment, map your two numbers to the
# tangent and normal vectors in the KookyBotz GVF bridge above, and say in
# one sentence what GVF adds that pure pursuit doesn't (curvature-limited
# speed).
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
