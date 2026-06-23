"""
Chapter 18 — Loop Time & Bulk Reads

This is YOUR workspace. Read the matching lesson first:
    chapters/18-loop-time-and-bulk-reads.md

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/18_starter.py

Stuck? Try for real first, THEN peek at:
    solutions/18_solution.py
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

print("Chapter 18 - delete this line and start coding your exercises!\n")


# ===========================================================================
# Exercise 1
# Count a naive read. Reset the counter, read all 4 drive encoders
# separately (front_left, front_right, back_left, back_right), and print
# hw_reads(). (Expect 4.)
# ===========================================================================
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 2
# Count a naive loop. Reset, then in a for loop of 10 "loops" read all 4
# encoders each time. Print the total. (Expect 40 — this is what a slow
# robot does.)
# ===========================================================================
def exercise_2():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 3
# Turn on MANUAL caching. Set
# robot.hub.set_bulk_caching_mode(LynxModule.MANUAL). Reset the counter.
# Call robot.hub.clear_bulk_cache() once, then read all 4 encoders. Print
# hw_reads(). (Expect 1 — one bulk read served all four.)
# ===========================================================================
def exercise_3():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 4
# The big comparison. Redo exercise 2 but with MANUAL caching and a
# clear_bulk_cache() at the top of each of the 10 loops. Print the total and
# the speedup factor vs exercise 2. (Expect 10 reads → 4× fewer.)
# ===========================================================================
def exercise_4():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 5
# Forgot to clear. With MANUAL mode on, run 5 loops but *don't* call
# clear_bulk_cache() at all (only once before the loop). Read an encoder
# each loop and watch the value go stale (it never updates). In a comment:
# this is the #1 bulk-read bug — explain it.
# ===========================================================================
def exercise_5():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 6
# AUTO mode. Switch to LynxModule.AUTO, reset, and read the 4 encoders once.
# Compare the read count to MANUAL. In a comment, state the trade-off
# between AUTO and MANUAL.
# ===========================================================================
def exercise_6():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 7
# read → decide → write. Restructure a drive loop into three explicit phases
# per tick: a read() that snapshots all 4 encoders into a dict, a decide()
# that computes the average, and a write() that sets drive power. Run 25
# loops driving forward; print the final average tick count. Keep reads only
# in read().
# ===========================================================================
def exercise_7():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 8
# Consistent snapshot. Demonstrate the danger of reading mid-loop: in one
# version read front_left at the start *and* end of the loop body and show
# they can differ (because robot.step ran). Then show the read-phase version
# uses one consistent value. Explain why that matters for a PID.
# ===========================================================================
def exercise_8():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 9
# Loop-time budget. Pretend each real hardware read costs 2 ms. Compute and
# print the estimated loop time (ms) and loop frequency (Hz) for: (a) 6
# naive reads per loop, (b) 1 bulk read per loop. (Just arithmetic: time =
# reads × 2 ms; Hz = 1000 / time.) Show the frequency jump.
# ===========================================================================
def exercise_9():
    # ---- YOUR CODE HERE ----
    pass


# ===========================================================================
# Exercise 10
# Wire it into a real subsystem. Take your Chapter 17 RobotHardware
# singleton and add clear_bulk_cache(), read(), periodic(), write() methods.
# Write a run_loop() that calls them in order each tick. In a comment, map
# each method to what KookyBotz's Duo.java loop does (scheduler.run();
# robot.clearBulkCache(); robot.read(); robot.periodic(); robot.write();).
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
