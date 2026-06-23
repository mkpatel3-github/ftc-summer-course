"""Chapter 4 solutions - The Gyro (IMU)."""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
from ftcsim import Robot, run_for, TICKS_PER_INCH


def ex1(robot):
    robot.imu.reset_heading()
    run_for(robot, 0.5, lambda t: robot.set_drive_power(0, 0, 0.4))
    print("heading:", round(robot.imu.get_heading(), 1))


def angle_error(target, current):
    return target - current


def ex2():
    print(angle_error(90, 0))     # 90
    print(angle_error(-170, 170))  # -340  (robot would spin the long way)


def angle_wrap(error):
    return ((error + 180) % 360) - 180


def ex3():
    print(angle_wrap(angle_error(-170, 170)))  # +20
    print(angle_wrap(350), angle_wrap(-350), angle_wrap(190))  # -10 10 -170


def turn_to(robot, target_deg, tol=2.0):
    error = angle_wrap(target_deg - robot.imu.get_heading())
    while abs(error) > tol:
        power = 0.4 if error > 0 else -0.4
        robot.set_drive_power(0, 0, power)
        robot.step(0.02)
        error = angle_wrap(target_deg - robot.imu.get_heading())
    robot.set_drive_power(0, 0, 0)


def ex4(robot):
    turn_to(robot, 90)
    print("to 90:", round(robot.imu.get_heading(), 1))
    turn_to(robot, -45)
    print("to -45:", round(robot.imu.get_heading(), 1))


def ex5(robot):
    turn_to(robot, 90)
    print("left to:", round(robot.imu.get_heading(), 1))
    turn_to(robot, -90)
    print("right to:", round(robot.imu.get_heading(), 1))


def turn_to_p(robot, target_deg, gain=0.02, tol=1.0):
    error = angle_wrap(target_deg - robot.imu.get_heading())
    while abs(error) > tol:
        power = max(-0.5, min(0.5, error * gain))
        robot.set_drive_power(0, 0, power)
        robot.step(0.02)
        error = angle_wrap(target_deg - robot.imu.get_heading())
    robot.set_drive_power(0, 0, 0)


def ex6(robot):
    turn_to_p(robot, 90)
    print("proportional to 90:", round(robot.imu.get_heading(), 1))


def drive_straight(robot, inches, power=0.5, target_heading=0.0, disturb=False):
    robot.front_left.reset_encoder()
    target = inches * TICKS_PER_INCH
    n = 0
    while robot.front_left.get_encoder_value() < target:
        error = angle_wrap(target_heading - robot.imu.get_heading())
        rx = error * 0.03
        robot.set_drive_power(0, power, rx)
        robot.step(0.02)
        n += 1
        if disturb and n % 25 == 0:
            robot.heading += 5
    robot.set_drive_power(0, 0, 0)


def ex7(robot):
    drive_straight(robot, 36)
    print("36in heading held:", round(robot.imu.get_heading(), 1))


def ex8():
    on = Robot()
    drive_straight(on, 36, disturb=True)
    print("correction ON  -> heading:", round(on.imu.get_heading(), 1))
    off = Robot()
    # correction OFF: same disturbance, but no rx
    off.front_left.reset_encoder()
    n = 0
    target = 36 * TICKS_PER_INCH
    while off.front_left.get_encoder_value() < target:
        off.set_drive_power(0, 0.5, 0)
        off.step(0.02)
        n += 1
        if n % 25 == 0:
            off.heading += 5
    off.set_drive_power(0, 0, 0)
    print("correction OFF -> heading:", round(off.imu.get_heading(), 1))


def ex9(robot):
    turn_to(robot, 30)
    drive_straight(robot, 24, target_heading=30)
    print("on heading 30:", round(robot.imu.get_heading(), 1), "|", robot.pose_str())


def ex10(robot):
    drive_straight(robot, 24, target_heading=0)
    turn_to(robot, 90)
    drive_straight(robot, 24, target_heading=90)
    print("L-path end:", robot.pose_str())


if __name__ == "__main__":
    print("ex1"); ex1(Robot())
    print("ex2"); ex2()
    print("ex3"); ex3()
    print("ex4"); ex4(Robot())
    print("ex5"); ex5(Robot())
    print("ex6"); ex6(Robot())
    print("ex7"); ex7(Robot())
    print("ex8"); ex8()
    print("ex9"); ex9(Robot())
    print("ex10"); ex10(Robot())
