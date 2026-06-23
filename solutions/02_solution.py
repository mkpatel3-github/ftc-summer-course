"""Chapter 2 solutions - Motors & Power."""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
from ftcsim import Robot, Motor, run_for


def ex1(robot):
    robot.front_left.set_speed(0.5)
    for _ in range(50):
        robot.step(0.02)
    print("encoder:", round(robot.front_left.get_encoder_value(), 1))


def ex2(robot):
    robot.front_left.set_speed(2.0)
    print("stored speed:", robot.front_left.speed)
    # It's 1.0, not 2.0: set_speed clamps to [-1, 1]. A motor can't exceed 100%.


def ex3(robot):
    run_for(robot, 1.0, lambda t: robot.set_drive_power(0, 1.0, 0))
    print("after forward:", robot.pose_str())
    run_for(robot, 1.0, lambda t: robot.set_drive_power(0, -1.0, 0))
    print("after back:   ", robot.pose_str())
    # x returns near 0 -- forward then equal backward cancels out.


def ex4():
    a = Robot(); run_for(a, 2.0, lambda t: a.set_drive_power(0, 0.5, 0))
    b = Robot(); run_for(b, 1.0, lambda t: b.set_drive_power(0, 1.0, 0))
    print("0.5 x 2s:", a.pose_str())
    print("1.0 x 1s:", b.pose_str())
    # Similar distance: power*time is the same (0.5*2 == 1.0*1).


def ex5():
    fwd = Motor(0, "a", reverse=False)
    rev = Motor(1, "b", reverse=True)
    fwd.set_speed(0.5)
    rev.set_speed(0.5)
    print("forward motor speed:", fwd.speed, "| reversed motor speed:", rev.speed)
    # Reverse flips the sign so the same command spins it the other way.


def drive(robot, power, seconds):
    run_for(robot, seconds, lambda t: robot.set_drive_power(0, power, 0))


def ex6(robot):
    drive(robot, 1.0, 1.5)
    print("after drive helper:", robot.pose_str())


def ex7(robot):
    run_for(robot, 1.0, lambda t: robot.set_drive_power(1.0, 0, 0))
    print("after strafe:", robot.pose_str())  # y changes (sideways in field frame)


def ex8():
    a = Robot(); run_for(a, 1.0, lambda t: a.set_drive_power(0, 0, 0.5))
    b = Robot(); run_for(b, 1.0, lambda t: b.set_drive_power(0, 0, -0.5))
    print("rx=+0.5 heading:", round(a.imu.get_heading(), 1))
    print("rx=-0.5 heading:", round(b.imu.get_heading(), 1))


def clamp(value, lo=-1.0, hi=1.0):
    return max(lo, min(hi, value))


def ex9():
    print(clamp(2.0), clamp(-3.0), clamp(0.4))  # 1.0 -1.0 0.4


def normalize(powers):
    biggest = max(abs(p) for p in powers)
    if biggest > 1.0:
        powers = [p / biggest for p in powers]
    return powers


def ex10():
    print(normalize([1.5, -0.5, 1.0, 0.2]))
    # [1.0, -0.333, 0.667, 0.133] -- same ratios, nothing over 1.0.


if __name__ == "__main__":
    print("ex1"); ex1(Robot())
    print("ex2"); ex2(Robot())
    print("ex3"); ex3(Robot())
    print("ex4"); ex4()
    print("ex5"); ex5()
    print("ex6"); ex6(Robot())
    print("ex7"); ex7(Robot())
    print("ex8"); ex8()
    print("ex9"); ex9()
    print("ex10"); ex10()
