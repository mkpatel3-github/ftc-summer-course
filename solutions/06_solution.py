"""Chapter 6 solutions - Mecanum TeleOp."""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
from ftcsim import Robot, Gamepad, run_for


def ex1():
    robot, gp = Robot(), Gamepad()
    gp.left_stick_y = -1.0  # up is negative on real sticks
    run_for(robot, 1.0,
            lambda t: robot.set_drive_power(-gp.left_stick_x, -gp.left_stick_y, gp.right_stick_x))
    print("forward:", robot.pose_str())


def ex2():
    robot, gp = Robot(), Gamepad()
    gp.left_stick_x = 1.0
    run_for(robot, 1.0,
            lambda t: robot.set_drive_power(-gp.left_stick_x, -gp.left_stick_y, gp.right_stick_x))
    print("strafe:", robot.pose_str())  # y changes (field frame)


def ex3():
    robot, gp = Robot(), Gamepad()
    gp.right_stick_x = 0.5
    run_for(robot, 1.0,
            lambda t: robot.set_drive_power(-gp.left_stick_x, -gp.left_stick_y, gp.right_stick_x))
    print("rotate heading:", round(robot.imu.get_heading(), 1))


def ex4():
    robot, gp = Robot(), Gamepad()
    gp.left_stick_x = 0.7
    gp.left_stick_y = -0.7
    run_for(robot, 1.0,
            lambda t: robot.set_drive_power(-gp.left_stick_x, -gp.left_stick_y, gp.right_stick_x))
    print("diagonal:", robot.pose_str())


def wheel_powers(x, y, rx):
    fl = y + x + rx
    fr = y - x - rx
    bl = (y - x + rx) * -1
    br = (y + x - rx) * -1
    return [fl, fr, bl, br]


def ex5():
    print("forward:", wheel_powers(0, 1, 0))
    print("strafe: ", wheel_powers(1, 0, 0))
    print("spin:   ", wheel_powers(0, 0, 1))


class EdgeDetector:
    def __init__(self):
        self.prev = False

    def rising(self, current):
        fired = current and not self.prev
        self.prev = current
        return fired


def ex6():
    ed = EdgeDetector()
    fires = [ed.rising(True) for _ in range(5)]  # held 5 loops
    print("fired on:", fires, "-> count:", sum(fires))  # exactly 1


def ex7():
    mode = "SAMPLE"
    ed = EdgeDetector()
    presses = {10, 30}
    for loop in range(40):
        a = loop in presses
        if ed.rising(a):
            mode = "SPECIMEN" if mode == "SAMPLE" else "SAMPLE"
            print(f"loop {loop}: toggled -> {mode}")


def ex8():
    robot = Robot()

    def loop(t):
        if t < 1.0:
            robot.set_drive_power(0, 1.0, 0)   # forward
        elif t < 2.0:
            robot.set_drive_power(1.0, 0, 0)   # strafe
        else:
            robot.set_drive_power(0, 0, 0.5)   # spin
    run_for(robot, 3.0, loop)
    print("3-phase end:", robot.pose_str())


def ex9():
    for slow in (False, True):
        robot, gp = Robot(), Gamepad()
        gp.left_stick_y = -1.0
        gp.right_bumper = slow

        def loop(t):
            scale = 0.3 if gp.right_bumper else 1.0
            robot.set_drive_power(-gp.left_stick_x * scale,
                                  -gp.left_stick_y * scale,
                                  gp.right_stick_x * scale)
        run_for(robot, 1.0, loop)
        print(f"slow={slow}:", robot.pose_str())


def ex10():
    robot, gp = Robot(), Gamepad()
    gp.left_stick_y = -0.8
    mode = "SAMPLE"
    ed_a, ed_b = EdgeDetector(), EdgeDetector()
    loop_count = [0]

    def loop(t):
        nonlocal mode
        gp.a = abs(t - 0.5) < 0.02   # press 'a' once around t=0.5
        gp.b = abs(t - 1.5) < 0.02   # press 'b' once around t=1.5
        if ed_a.rising(gp.a):
            mode = "SPECIMEN" if mode == "SAMPLE" else "SAMPLE"
        if ed_b.rising(gp.b):
            print("EJECT")
        robot.set_drive_power(-gp.left_stick_x, -gp.left_stick_y, gp.right_stick_x)
        loop_count[0] += 1
        if loop_count[0] % 25 == 0:
            robot.telemetry.add_data("MODE", mode)
            robot.telemetry.add_data("pose", robot.pose_str())
            robot.telemetry.add_data("loop", loop_count[0])
            robot.telemetry.update()
    run_for(robot, 2.0, loop)


if __name__ == "__main__":
    for name in ["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10"]:
        print(name); globals()[name]()
