"""Chapter 1 solutions - Hello, Robot.

Run me:  python solutions/01_solution.py
Each exercise is its own function so you can read them one at a time.
"""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
from ftcsim import Robot


def ex1(robot):
    robot.telemetry.add_data("Team", "Juice 16236")
    robot.telemetry.update()


def ex2(robot):
    wheel_count = 4          # int in Java
    motor_power = 0.75       # double in Java
    team_name = "Juice"      # String in Java
    robot.telemetry.add_data("wheels", wheel_count)
    robot.telemetry.add_data("power", motor_power)
    robot.telemetry.add_data("name", team_name)
    robot.telemetry.update()


# ex3 - Java costume (written, not run):
#   int wheelCount = 4;
#   double motorPower = 0.75;
#   String teamName = "Juice";


def ex4(robot):
    power = 0.6
    distance = power * 3.0
    robot.telemetry.add_data("distance", distance)
    robot.telemetry.update()


def ex5(robot, is_red_alliance=True):
    if is_red_alliance:
        robot.telemetry.add_data("Alliance", "RED")
    else:
        robot.telemetry.add_data("Alliance", "BLUE")
    robot.telemetry.update()


def ex6(robot):
    # Version A: queue three, send once -> all three appear together.
    robot.telemetry.add_data("a", 1)
    robot.telemetry.add_data("b", 2)
    robot.telemetry.add_data("c", 3)
    robot.telemetry.update()
    # Version B: send after each -> three separate screens.
    for caption, value in (("a", 1), ("b", 2), ("c", 3)):
        robot.telemetry.add_data(caption, value)
        robot.telemetry.update()
    # update() = "press send"; addData only QUEUES a line until then.


def ex7(robot):
    avg = (1800 + 1810) / 2
    robot.telemetry.add_data("avg", avg)
    robot.telemetry.update()
    # Java gotcha: (1800 + 1810) / 2 with ints = 1805 here too (even), BUT
    # (1801 + 1810) / 2 as int = 1805 (truncated, .5 dropped), not 1805.5.
    # Integer division throws away the fraction. Use double to keep it.


def ex8(robot):
    robot.telemetry.add_data("two_thirds", round(2 / 3, 2))
    robot.telemetry.update()


def ex9(robot):
    robot.telemetry.add_data("MODE", "SAMPLE")
    robot.telemetry.add_data("COLOR", "YELLOW")
    robot.telemetry.add_data("CLIMB", "LEVEL_3")
    robot.telemetry.add_data("state", "INTAKE")
    robot.telemetry.update()


# ex10 - design notes (no code):
#   I'd want: alliance color, current scoring mode, lift height, whether the
#   claw has a game piece, match time left, loop speed (to catch lag), and any
#   error/warning. Juice shows MODE/COLOR/CLIMB/state because those are the
#   things a driver changes mid-match and must confirm at a glance.


if __name__ == "__main__":
    r = Robot()
    for fn in (ex1, ex2, ex4, ex5, ex6, ex7, ex8, ex9):
        print(f"\n=== {fn.__name__} ===")
        fn(r)
