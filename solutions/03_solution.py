"""Chapter 3 solutions - Encoders & Distance."""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
from ftcsim import Robot, run_for, TICKS_PER_INCH


def ex1(robot):
    robot.front_left.reset_encoder()
    run_for(robot, 1.0, lambda t: robot.set_drive_power(0, 0.5, 0))
    ticks = robot.front_left.get_encoder_value()
    print("ticks:", round(ticks, 1), "= inches", round(ticks / 45, 2))


def inches_to_ticks(inches):
    return inches * TICKS_PER_INCH


def ticks_to_inches(ticks):
    return ticks / TICKS_PER_INCH


def ex2():
    print("round-trip 24in:", ticks_to_inches(inches_to_ticks(24)))


def drive_inches(robot, inches, power=0.5):
    robot.front_left.reset_encoder()
    target = inches_to_ticks(inches)
    if inches >= 0:
        while robot.front_left.get_encoder_value() < target:
            robot.set_drive_power(0, power, 0)
            robot.step(0.02)
    else:
        while robot.front_left.get_encoder_value() > target:
            robot.set_drive_power(0, -power, 0)
            robot.step(0.02)
    robot.set_drive_power(0, 0, 0)


def ex3(robot):
    drive_inches(robot, 24)
    print("after 24in:", robot.pose_str())


def ex4(robot):
    drive_inches(robot, 12)
    print("after 12:", robot.pose_str())
    drive_inches(robot, 36)
    print("after +36:", robot.pose_str())


def ex5(robot):
    drive_inches(robot, -12)
    print("after -12:", robot.pose_str())


def ex6():
    # Encoder method ends at 24 regardless of power; time method does not.
    for power in (0.5, 0.3):
        enc = Robot()
        drive_inches(enc, 24, power)
        print(f"encoder @power {power}:", enc.pose_str())
    # Same guessed time (1.2s) at different powers -> different distance:
    for power in (0.5, 0.3):
        tm = Robot()
        run_for(tm, 1.2, lambda t: tm.set_drive_power(0, power, 0))
        print(f"time @power {power}:   ", tm.pose_str())


def average_distance_inches(robot):
    motors = (robot.front_left, robot.front_right, robot.back_left, robot.back_right)
    avg_ticks = sum(abs(m.get_encoder_value()) for m in motors) / 4
    return ticks_to_inches(avg_ticks)


def ex8(robot):
    run_for(robot, 1.0, lambda t: robot.set_drive_power(0, 0.5, 0))
    print("avg distance in:", round(average_distance_inches(robot), 2))


def drive_inches_slowdown(robot, inches, power=0.5):
    robot.front_left.reset_encoder()
    target = inches_to_ticks(inches)
    while robot.front_left.get_encoder_value() < target:
        remaining = ticks_to_inches(target - robot.front_left.get_encoder_value())
        p = 0.2 if remaining < 6 else power
        robot.set_drive_power(0, p, 0)
        robot.step(0.02)
    robot.set_drive_power(0, 0, 0)


def ex9(robot):
    drive_inches_slowdown(robot, 24)
    print("slowdown 24in:", robot.pose_str())


def ex10(robot):
    drive_inches(robot, 26)  # stop 4in short of a 30in target
    print("stops at:", robot.pose_str())
    # Real-field error: wheel slip, field bumps, low battery, robot not perfectly
    # straight. Heading drift is fixed by the gyro/IMU (Chapter 4).


if __name__ == "__main__":
    for name, fn in [("ex1", ex1), ("ex3", ex3), ("ex4", ex4), ("ex5", ex5),
                     ("ex8", ex8), ("ex9", ex9), ("ex10", ex10)]:
        print(name); fn(Robot())
    print("ex2"); ex2()
    print("ex6"); ex6()
