"""
Chapter 14 — Vision & AprilTags

This is YOUR workspace. Read the matching lesson first:
    chapters/14-vision-and-apriltags.md

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/14_starter.py

Stuck? Try for real first, THEN peek at:
    solutions/14_solution.py
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
                    DeadWheelLocalizer, OTOSLocalizer)

print("Chapter 14 - delete this line and start coding your exercises!\n")


# ===========================================================================
# Exercise 1
# See a tag. Put the robot near the right wall (start_x=60, start_y=0) and
# print robot.camera.get_detections(). Confirm at least one tag is visible
# and print its id.
# ===========================================================================
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 2
# Localize. From the same spot, print robot.camera.localize(). Compare it to
# the robot's true pose (robot.get_pose()). They should match (perfect sim
# camera).
# ===========================================================================
def exercise_2():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 3
# Out of range. Put the robot at the center (0,0) with the camera's
# max_range small: robot.camera.max_range = 10. Show localize() returns
# None. Explain in a comment what your code should do when the camera sees
# nothing.
# ===========================================================================
def exercise_3():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 4
# Localize from the math yourself. Don't call localize(). Get one detection
# (tag, dx, dy) from get_detections() and compute robot_x = tag.x - dx,
# robot_y = tag.y - dy by hand. Confirm it matches the true pose.
# ===========================================================================
def exercise_4():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 5
# Nearest tag wins. Place the robot where two tags are in range (try
# start_x=50, start_y=50 with a large max_range). Print all detections and
# their distances, then show localize() picked the closest one. Why prefer
# the closest? (Comment.)
# ===========================================================================
def exercise_5():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 6
# Camera vs odometry. Drive forward 2s. Print both robot.odometry.get_pose()
# and robot.camera.localize(). With a perfect sim they agree — in a comment,
# say which one you trust more after a 30-second match, and why (drift!).
# ===========================================================================
def exercise_6():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 7
# Find the sample by color. Reuse Chapter 5: place a colored sample on the
# field (field.sample_x, field.sample_y, field.sample_color), drive over it,
# and use the color sensor to report its color. In a comment, note that
# CVMaster.java does this with a camera blob detector instead of a contact
# sensor — what's the advantage of seeing it from far away?
# ===========================================================================
def exercise_7():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 8
# Re-localize after a "bump." Drive forward 2s, then *teleport* the robot
# (simulate a defender shoving it: set robot.x += 8). Show odometry still
# reports the old-ish path but camera.localize() immediately reports the
# true, bumped position. This is the headline benefit of vision.
# ===========================================================================
def exercise_8():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 9
# A vision-corrected stop. Drive toward the right wall. Each loop, if a tag
# is visible, use camera.localize() to check distance to Pose2d(60, 0); stop
# within 2". Print the final pose. (Vision closing the loop on position.)
# ===========================================================================
def exercise_9():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 10
# Design a vision plan. In a comment block, write the plan Juice's CVMaster
# follows at a high level: when to run the AprilTag pipeline (localization)
# vs the color-blob pipeline (find sample), and why you wouldn't run heavy
# vision every single loop (hint: loop time — Chapter 15). No code; this is
# real strategy.
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
