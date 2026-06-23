"""Chapter 9 solutions - Autonomous."""
import sys, os, math
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
from ftcsim import Robot, TICKS_PER_INCH


# --- helpers reused from chapters 3-4 ---
def angle_wrap(error):
    return ((error + 180) % 360) - 180


def turn_to(robot, target_deg, tol=2.0):
    error = angle_wrap(target_deg - robot.imu.get_heading())
    while abs(error) > tol:
        robot.set_drive_power(0, 0, 0.4 if error > 0 else -0.4)
        robot.step(0.02)
        error = angle_wrap(target_deg - robot.imu.get_heading())
    robot.set_drive_power(0, 0, 0)


def drive_straight(robot, inches, power=0.5, target_heading=None):
    if target_heading is None:
        target_heading = robot.imu.get_heading()
    robot.front_left.reset_encoder()
    target = inches * TICKS_PER_INCH
    while robot.front_left.get_encoder_value() < target:
        error = angle_wrap(target_heading - robot.imu.get_heading())
        robot.set_drive_power(0, power, error * 0.03)
        robot.step(0.02)
    robot.set_drive_power(0, 0, 0)


def ex1():
    r = Robot(start_x=-30, start_y=-60, start_heading=0)
    print("start pose:", r.pose_str())


def go_to_x(robot, target_x):
    inches = target_x - robot.x
    drive_straight(robot, abs(inches), power=0.5 if inches >= 0 else -0.5,
                   target_heading=0)


def ex2():
    r = Robot(start_x=-30, start_y=-60, start_heading=0)
    go_to_x(r, 0)
    print("after go_to_x(0):", r.pose_str())


def ex3():
    r = Robot()
    drive_straight(r, 24, target_heading=0)
    print("seg1:", r.pose_str())
    turn_to(r, 45)
    print("turn:", r.pose_str())
    drive_straight(r, 20, target_heading=45)
    print("seg2:", r.pose_str())


def run_sequence(robot, steps, time_budget=None):
    elapsed = 0.0
    for i, (name, fn) in enumerate(steps, 1):
        if time_budget is not None and elapsed >= time_budget:
            print(f"[{i}/{len(steps)}] {name} ... SKIPPED (out of time)")
            continue
        before = robot
        fn(robot)
        elapsed += 2.0  # rough cost per step for the timed demo
        print(f"[{i}/{len(steps)}] {name} ... done")
    return elapsed


def ex4():
    r = Robot()
    steps = [
        ("preload", lambda rb: drive_straight(rb, 10)),
        ("spike1", lambda rb: turn_to(rb, 30)),
        ("depo1", lambda rb: drive_straight(rb, 8, target_heading=30)),
        ("park", lambda rb: turn_to(rb, 0)),
    ]
    run_sequence(r, steps)


def distance_to(robot, x, y):
    return math.hypot(x - robot.x, y - robot.y)


def drive_to_pose(robot, x, y, heading):
    dx, dy = x - robot.x, y - robot.y
    if abs(dx) > 0.1 or abs(dy) > 0.1:
        face = math.degrees(math.atan2(dy, dx))
        turn_to(robot, face)
        dist = math.hypot(dx, dy)
        drive_straight(robot, dist, target_heading=face)
    turn_to(robot, heading)


def ex5():
    r = Robot(start_x=-30, start_y=-60, start_heading=0)
    names = ["preload", "spike1", "depo1", "spike2", "depo2", "spike3", "depo3", "park"]
    poses = [(-56, -56, 45), (-48, -48, 90), (-56, -56, 45), (-58, -48, 90),
             (-56, -56, 45), (-54, -45, 127), (-56, -56, 45), (-25, -10, 0)]
    steps = [(nm, (lambda p: lambda rb: drive_to_pose(rb, *p))(p))
             for nm, p in zip(names, poses)]
    run_sequence(r, steps)
    print("final:", r.pose_str())


def ex6():
    r = Robot(start_x=-30, start_y=-60, start_heading=0)
    drive_to_pose(r, -56, -56, 45)
    print("reached:", r.pose_str(), "| miss:", round(distance_to(r, -56, -56), 2), "in")


def ex7():
    r = Robot(start_x=-30, start_y=-60, start_heading=0)
    drive_to_pose(r, -56, -56, 45)
    d = distance_to(r, -56, -56)
    print("distance to target pose:", round(d, 2), "-> within few inches:", d < 4)


def ex8():
    from importlib import import_module
    mod = import_module("08_solution")
    Lift, Levels = mod.Lift, mod.Levels
    r = Robot(start_x=-30, start_y=-60, start_heading=0)
    lift = Lift()
    score = [0]

    def depo(rb):
        drive_to_pose(rb, -56, -56, 45)
        lift.run_to_preset(Levels.HIGH_BASKET)
        lift.settle(150)
        score[0] += 8
        print("    scored! lift at", round(lift.get_pos(), 0))

    steps = [("preload", lambda rb: drive_to_pose(rb, -50, -50, 45)),
             ("depo1", depo)]
    run_sequence(r, steps)
    print("points:", score[0])


def ex9():
    r = Robot()
    steps = [(f"step{i}", lambda rb: drive_straight(rb, 5)) for i in range(20)]
    elapsed = run_sequence(r, steps, time_budget=30.0)  # 30s budget, 2s/step
    print("ran ~", int(elapsed / 2), "of", len(steps), "steps within 30s")


def ex10():
    from importlib import import_module
    mod = import_module("08_solution")
    Lift, Levels = mod.Lift, mod.Levels
    r = Robot(start_x=-30, start_y=-60, start_heading=0)
    lift = Lift()
    score = [0]

    def score_basket(rb):
        lift.run_to_preset(Levels.HIGH_BASKET); lift.settle(120)
        score[0] += 8; print("    +8 high basket")

    plan = [
        ("score preload", lambda rb: (drive_to_pose(rb, -56, -56, 45), score_basket(rb))),
        ("grab sample 1", lambda rb: drive_to_pose(rb, -48, -40, 90)),
        ("score 1", lambda rb: (drive_to_pose(rb, -56, -56, 45), score_basket(rb))),
        ("grab sample 2", lambda rb: drive_to_pose(rb, -58, -40, 90)),
        ("score 2", lambda rb: (drive_to_pose(rb, -56, -56, 45), score_basket(rb))),
        ("park", lambda rb: drive_to_pose(rb, -25, -10, 0)),
    ]
    run_sequence(r, plan)
    print("final:", r.pose_str(), "| total points:", score[0])
    # RoadRunner drives smooth splines and corrects position with odometry, so it
    # is faster and more accurate than stop-turn-drive dead reckoning -> more cycles
    # in 30s. That's why Juice uses it for competition autos.


if __name__ == "__main__":
    for name in ["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10"]:
        print(name); globals()[name]()
