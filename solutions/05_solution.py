"""Chapter 5 solutions - Sensors & Line Following."""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
from ftcsim import Robot, Field, run_for, TICKS_PER_INCH


def make_robot(color="BLUE", x=10, y=0):
    f = Field()
    f.sample_x, f.sample_y, f.sample_color = x, y, color
    return Robot(field=f)


def drive_to_sample(robot):
    # drive forward until the color sensor is near the sample
    while robot.color.get_distance() > 5 and robot.x < robot.field.sample_x:
        robot.set_drive_power(0, 0.3, 0)
        robot.step(0.02)
    robot.set_drive_power(0, 0, 0)


def ex1():
    robot = make_robot("BLUE")
    drive_to_sample(robot)
    print("R/G/B:", round(robot.color.red(), 2),
          round(robot.color.green(), 2), round(robot.color.blue(), 2))


def detect_color_v1(robot):
    r, g, b = robot.color.red(), robot.color.green(), robot.color.blue()
    if b > r and b > g:
        return "BLUE"
    return None


def ex2():
    print("on blue:", detect_color_v1(make_robot("BLUE") and _at_sample("BLUE")))
    print("on floor:", detect_color_v1(Robot()))


def _at_sample(color):
    robot = make_robot(color)
    drive_to_sample(robot)
    return robot


def detect_color(robot):
    r, g, b = robot.color.red(), robot.color.green(), robot.color.blue()
    if r > 0.5 and g > 0.5 and b < 0.3:
        return "YELLOW"
    elif b > r:
        return "BLUE"
    elif r > b:
        return "RED"
    return None


def ex3():
    for c in ("RED", "BLUE", "YELLOW"):
        print(c, "->", detect_color(_at_sample(c)))


def should_keep(color, alliance):
    if color == "YELLOW" or color == alliance:
        return 1   # keep
    elif color is not None:
        return -1  # eject
    return 0       # nothing


def ex4():
    for c in ("RED", "BLUE", "YELLOW", None):
        print(f"RED alliance sees {c}:", should_keep(c, "RED"))


def ex5():
    robot = make_robot("BLUE", x=15)
    while detect_color(robot) is None:
        robot.set_drive_power(0, 0.3, 0)
        robot.step(0.02)
    robot.set_drive_power(0, 0, 0)
    print("stopped at:", robot.pose_str(), "saw", detect_color(robot))


def ex6():
    robot = Robot()
    while robot.distance.get_distance() > 12:
        robot.set_drive_power(0, 0.5, 0)
        robot.step(0.02)
    robot.set_drive_power(0, 0, 0)
    print("distance to wall:", round(robot.distance.get_distance(), 1))


def ex7():
    robot = Robot()
    while robot.distance.get_distance() > 12.2:
        power = max(0.0, min(0.6, (robot.distance.get_distance() - 12) * 0.05))
        robot.set_drive_power(0, power, 0)
        robot.step(0.02)
    robot.set_drive_power(0, 0, 0)
    print("smooth stop at:", round(robot.distance.get_distance(), 1))


def on_line(robot):
    f = robot.field
    return abs(robot.x - f.line_x) <= f.line_half_width


def ex8():
    robot = Robot(start_x=0)
    print("at x=0 on line?", on_line(robot))
    robot.x = 5
    print("at x=5 on line?", on_line(robot))


def ex9():
    robot = Robot(start_x=4)  # off the line by 4 inches
    for _ in range(150):
        error = 0 - robot.x          # want x -> 0
        correction = error * 0.05
        robot.set_drive_power(0.4, correction, 0)  # strafe up field, correct x
        robot.step(0.02)
        if _ % 30 == 0:
            print(f"  y={robot.y:5.1f}  x_off_line={robot.x:5.2f}")
    robot.set_drive_power(0, 0, 0)
    print("final x (should be ~0):", round(robot.x, 2))


def ex10():
    import random
    color = random.choice(["RED", "BLUE", "YELLOW"])
    robot = make_robot(color, x=12)
    drive_to_sample(robot)
    seen = detect_color(robot)
    decision = should_keep(seen, "BLUE")
    action = {1: "KEEP", -1: "EJECT", 0: "NONE"}[decision]
    print(f"sample was {color}; sensor saw {seen}; action: {action} {seen}")


if __name__ == "__main__":
    print("ex1"); ex1()
    print("ex2"); ex2()
    print("ex3"); ex3()
    print("ex4"); ex4()
    print("ex5"); ex5()
    print("ex6"); ex6()
    print("ex7"); ex7()
    print("ex8"); ex8()
    print("ex9"); ex9()
    print("ex10"); ex10()
