"""Chapter 13 solutions - Odometry & Pose."""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
from ftcsim import Robot, Pose2d, run_for


def turn_to(robot, target_h, max_s=3.0):
    def loop(t):
        err = (target_h - robot.imu.get_heading() + 180) % 360 - 180
        robot.set_drive_power(0, 0, max(-0.5, min(0.5, err * 0.05)))
    run_for(robot, max_s, loop)
    robot.set_drive_power(0, 0, 0)


def ex1():
    r = Robot()
    run_for(r, 1.0, lambda t: r.set_drive_power(0, 1, 0))
    print("pose:", r.odometry.get_pose())


def ex2():
    r = Robot()
    turn_to(r, 90)
    print("heading after turn:", round(r.odometry.get_pose().heading, 1))


def ex3():
    r = Robot()
    run_for(r, 1.0, lambda t: r.set_drive_power(0, 1, 0))
    pose = r.odometry.get_pose()
    print("distance from center:", round(pose.distance_to(Pose2d(0, 0)), 1))


def ex4():
    r = Robot()
    n = [0]

    def loop(t):
        r.set_drive_power(0, 1, 0)
        n[0] += 1
        if n[0] % 25 == 0:
            print("live pose:", r.odometry.get_pose())
    run_for(r, 1.0, loop)


def ex5():
    r = Robot()
    run_for(r, 1.0, lambda t: r.set_drive_power(0, 1, 0))
    print("leg1 (forward):", r.odometry.get_pose())
    run_for(r, 1.0, lambda t: r.set_drive_power(1, 0, 0))
    print("leg2 (strafe): ", r.odometry.get_pose())
    run_for(r, 1.0, lambda t: r.set_drive_power(0, 1, 0))
    print("leg3 (forward):", r.odometry.get_pose())


def ex6():
    r = Robot()
    target = Pose2d(40, 0, 0)
    elapsed = [0.0]

    def loop(t):
        if r.odometry.get_pose().distance_to(target) < 2.0:
            r.set_drive_power(0, 0, 0)
        else:
            r.set_drive_power(0, 1, 0)
            elapsed[0] = t
    run_for(r, 3.0, loop)
    print("final:", r.odometry.get_pose(), "| reached ~t=", round(elapsed[0], 2))


def ex7():
    r = Robot()
    r.odometry.noise = 0.5
    for _ in range(5):
        print("still, but reads:", r.odometry.get_pose())
    # Timing-based (FLL) autonomous has NO sensor reading position, so it can
    # never notice this jitter or a real bump -- it just runs motors on a clock.


def ex8():
    print("""If you tell the software the pods are at robot center but they're
really 6in forward, then when the robot ROTATES the pods trace a circle of
radius 6in. The software thinks the center moved (because the pods moved),
so it reports a phantom x/y shift on every turn -- the pose drifts badly
during rotation. Correct xOffset/yOffset cancel this.""")


def ex9():
    r = Robot(start_x=20, start_y=-30)
    print("seeded start pose:", r.odometry.get_pose())
    # You must seed the starting pose (where the robot physically begins) before
    # autonomous, because odometry only measures CHANGE. If you forget, the robot
    # thinks it started at (0,0) and every "drive to (x,y)" lands 20,-30 off.


def ex10():
    print("""Pinpoint (two encoder pods): cheap-ish, very accurate, but you must
mount two unpowered odometry wheels and tune xOffset/yOffset; struggles if a
pod lifts off the floor or slips. OTOS (optical mouse sensor): almost no setup
and no pods, reads the floor directly; struggles on shiny/uneven floor and
needs a steady mounting height. Many teams pick Pinpoint for accuracy, OTOS
for simplicity. (See gobilda.com / sparkfun OTOS in REFERENCES.)""")


if __name__ == "__main__":
    for name in ["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10"]:
        print("\n===", name, "===")
        globals()[name]()
