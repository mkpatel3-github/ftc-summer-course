"""Chapter 12 solutions - Field-Centric Driving."""
import sys, os, math
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
from ftcsim import Robot, Gamepad, run_for


def turn_to(robot, target_h, max_s=3.0):
    """Helper: spin the robot until heading is near target_h."""
    def loop(t):
        err = (target_h - robot.imu.get_heading() + 180) % 360 - 180
        robot.set_drive_power(0, 0, max(-0.5, min(0.5, err * 0.05)))
    run_for(robot, max_s, loop)
    robot.set_drive_power(0, 0, 0)


def ex1():
    r1 = Robot()
    run_for(r1, 1.0, lambda t: r1.set_drive_power_field_centric(0, 1, 0))
    r2 = Robot()
    run_for(r2, 1.0, lambda t: r2.set_drive_power(0, 1, 0))
    print("field-centric:", r1.pose_str())
    print("robot-centric:", r2.pose_str(), "(same at heading 0)")


def ex2():
    r = Robot()
    turn_to(r, 90)
    run_for(r, 1.0, lambda t: r.set_drive_power(0, 1, 0))
    print("robot-centric after 90deg turn:", r.pose_str(),
          "-> nose points +y, so it drove +y, NOT what driver wanted")


def ex3():
    r = Robot()
    turn_to(r, 90)
    run_for(r, 1.0, lambda t: r.set_drive_power_field_centric(0, 1, 0))
    print("field-centric after 90deg turn:", r.pose_str(),
          "-> still moved downfield (+y) like the driver intended")


def rotate_stick(x, y, heading_deg):
    h = math.radians(heading_deg)
    x_r = x * math.cos(-h) - y * math.sin(-h)
    y_r = x * math.sin(-h) + y * math.cos(-h)
    return x_r, y_r


def ex4():
    xr, yr = rotate_stick(0, 1, 90)
    print(f"(0,1) at heading 90 -> ({xr:.2f}, {yr:.2f})")
    # at heading 90, "forward" for the field becomes "strafe" for the robot:
    # x_r ~ +1, y_r ~ 0. Sign of x_r is +1 because we rotate by -90.


def ex5():
    r = Robot()

    def loop(t):
        if t < 1.0:    r.set_drive_power_field_centric(0, 1, 0)   # +y
        elif t < 2.0:  r.set_drive_power_field_centric(1, 0, 0)   # +x
        elif t < 3.0:  r.set_drive_power_field_centric(0, -1, 0)  # -y
        else:          r.set_drive_power_field_centric(-1, 0, 0)  # -x
    run_for(r, 4.0, loop)
    print("square end:", r.pose_str(), "(heading stayed ~0)")


def ex6():
    r = Robot()
    turn_to(r, 90)
    r.imu.reset_heading()   # driver presses "reset" while facing downfield
    run_for(r, 1.0, lambda t: r.set_drive_power_field_centric(0, 1, 0))
    print("after reset, field-centric:", r.pose_str())
    # A driver presses this at match start (or after IMU drift) so "forward"
    # re-aligns with the field from the robot's current orientation.


def ex7():
    rc = Robot(); fc = Robot()
    turn_to(rc, 45); turn_to(fc, 45)
    run_for(rc, 1.0, lambda t: rc.set_drive_power(0, 1, 0))
    run_for(fc, 1.0, lambda t: fc.set_drive_power_field_centric(0, 1, 0))
    print("robot-centric @45:", rc.pose_str())
    print("field-centric @45:", fc.pose_str())
    print("robot-centric drove along the 45deg nose; field-centric drove +y.")


def ex8():
    for slow in (False, True):
        r = Robot()
        scale = 0.3 if slow else 1.0
        run_for(r, 1.0, lambda t: r.set_drive_power_field_centric(0, 1 * scale, 0))
        print(f"slow={slow}:", r.pose_str())


def ex9():
    r, gp = Robot(), Gamepad()
    gp.left_stick_y = -0.8
    prev_reset = [False]
    n = [0]

    def loop(t):
        gp.x = abs(t - 1.0) < 0.02   # press "reset heading" once near t=1.0
        if gp.x and not prev_reset[0]:
            r.imu.reset_heading()
        prev_reset[0] = gp.x
        r.set_drive_power_field_centric(-gp.left_stick_x, -gp.left_stick_y,
                                        gp.right_stick_x)
        n[0] += 1
        if n[0] % 25 == 0:
            r.telemetry.add_data("heading", round(r.imu.get_heading(), 1))
            r.telemetry.add_data("pose", r.pose_str())
            r.telemetry.update()
    run_for(r, 2.0, loop)


def ex10():
    print("""Prefer robot-centric when:
1. Lining up to a wall / scoring board -- you think in the robot's frame
   ("nudge forward into the board") and the IMU heading is irrelevant.
2. The IMU has drifted mid-match -- field-centric would send the robot the
   wrong way; robot-centric still does exactly what the nose does.
Teams bind a single button (e.g. 'back') to toggle a boolean fieldCentric,
and force heading=0 in the math when it's off -- one code path, one toggle.""")


if __name__ == "__main__":
    for name in ["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10"]:
        print("\n===", name, "===")
        globals()[name]()
