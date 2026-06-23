"""Chapter 10 solutions - Capstone: Solve a Mission ("Summer Cup")."""
import sys, os, math
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
from ftcsim import Robot, Field

# Reuse autonomous helpers from chapter 9 and state machine from chapter 8.
from importlib import import_module
ch9 = import_module("09_solution")
ch8 = import_module("08_solution")
drive_to_pose = ch9.drive_to_pose
distance_to = ch9.distance_to
run_sequence = ch9.run_sequence


# --- Mission setup ---------------------------------------------------------
ALLIANCE = "BLUE"
DEPOT = (48, 48)
PARK = (0, 48)
CELLS = [
    {"name": "cell1", "pose": (-48, -36), "color": "BLUE"},
    {"name": "cell2", "pose": (-24, -24), "color": "RED"},
    {"name": "cell3", "pose": (-48, 0),  "color": "YELLOW"},
]


def make_robot():
    return Robot(start_x=-36, start_y=-60, start_heading=90)


def should_keep(color, alliance):
    if color == "YELLOW" or color == alliance:
        return 1
    elif color is not None:
        return -1
    return 0


# ex1 - mission breakdown (planning, no code):
#   job: drive to each cell        -> Ch3/4 encoders+gyro / Ch9 drive_to_pose
#   job: identify cell color       -> Ch5 color sensor + should_keep
#   job: decide keep/reject        -> Ch5/Ch8 branching logic
#   job: deliver to depot, score   -> Ch9 sequencing
#   job: manage 30s clock          -> Ch9 time budget
#   job: park on center line       -> Ch9 drive_to_pose
#   organize it all                -> Ch8 subsystems + Ch9 SequentialAction


def ex2():
    r = make_robot()
    score = 0
    print("start:", r.pose_str(), "| score:", score)
    return r, score


def ex3():
    r = make_robot()
    drive_to_pose(r, *CELLS[0]["pose"], heading=90)
    print("at cell1:", r.pose_str(),
          "| arrived:", distance_to(r, *CELLS[0]["pose"]) < 4)


def identify(cell):
    color = cell["color"]
    decision = should_keep(color, ALLIANCE)
    return color, decision


def ex4():
    for cell in CELLS:
        color, decision = identify(cell)
        word = {1: "KEEP", -1: "REJECT", 0: "NONE"}[decision]
        print(f"{cell['name']} {color} -> {word}")


def ex5():
    r = make_robot()
    cell = CELLS[0]
    drive_to_pose(r, *cell["pose"], heading=90)
    color, decision = identify(cell)
    if decision == 1:
        drive_to_pose(r, *DEPOT, heading=45)
        print(f"{cell['name']} {color} -> delivered +5")
    else:
        print(f"{cell['name']} {color} -> rejected red")


def ex6():
    r = make_robot()
    score = 0
    for cell in CELLS:
        drive_to_pose(r, *cell["pose"], heading=90)
        color, decision = identify(cell)
        if decision == 1:
            drive_to_pose(r, *DEPOT, heading=45)
            score += 5
            print(f"{cell['name']} {color} -> delivered +5")
        else:
            print(f"{cell['name']} {color} -> rejected red")
    print("score after cells:", score)
    return r, score


def ex7():
    r, score = ex6()
    drive_to_pose(r, *PARK, heading=90)
    if abs(r.x) <= 4:
        score += 10
        print("parked on center line +10")
    print("FINAL score:", score)


def ex8():
    r = make_robot()
    score = 0
    budget, used = 30.0, 0.0
    cost_per_leg = 5.0  # rough seconds per drive leg
    # Sort deliverable cells by distance from start; skip farthest if over budget.
    deliverable = [c for c in CELLS if identify(c)[1] == 1]
    deliverable.sort(key=lambda c: distance_to(r, *c["pose"]))
    skipped = []
    for cell in deliverable:
        if used + 2 * cost_per_leg > budget - cost_per_leg:  # reserve time to park
            skipped.append(cell["name"])
            continue
        drive_to_pose(r, *cell["pose"], heading=90)
        drive_to_pose(r, *DEPOT, heading=45)
        used += 2 * cost_per_leg
        score += 5
        print(f"delivered {cell['name']} (+5), time used {used:.0f}s")
    drive_to_pose(r, *PARK, heading=90)
    if abs(r.x) <= 4:
        score += 10
    print("skipped (no time):", skipped or "none", "| FINAL score:", score)


def ex9():
    r = make_robot()
    score = [0]
    Lift, Levels = ch8.Lift, ch8.Levels
    lift = Lift()

    def visit_and_deliver(cell):
        def step(rb):
            drive_to_pose(rb, *cell["pose"], heading=90)
            color, decision = identify(cell)
            if decision == 1:
                drive_to_pose(rb, *DEPOT, heading=45)
                lift.run_to_preset(Levels.LOW_BASKET); lift.settle(80)
                score[0] += 5
                print(f"    {cell['name']} {color} delivered +5")
            else:
                print(f"    {cell['name']} {color} rejected")
        return step

    steps = [(c["name"], visit_and_deliver(c)) for c in CELLS]
    steps.append(("park", lambda rb: drive_to_pose(rb, *PARK, heading=90)))
    run_sequence(r, steps)
    if abs(r.x) <= 4:
        score[0] += 10
    print("final:", r.pose_str(), "| total points:", score[0])


# ex10 - reflection + Java translation:
#   To score more: carry multiple cells per trip; use smooth spline paths
#   (RoadRunner) instead of stop-turn-drive; pre-plan the shortest route.
#
#   Java version of visit_and_deliver (Juice style):
#
#   Action visitAndDeliver(Cell cell) {
#       return new SequentialAction(
#           drive.actionBuilder(drive.pose)
#                .splineToLinearHeading(cell.pose, cell.tangent).build(),
#           new InstantAction(() -> {
#               if (robot.detectSample() == BLUE || robot.detectSample() == YELLOW) {
#                   // deliver
#               }
#           }),
#           drive.actionBuilder(cell.pose)
#                .splineToLinearHeading(DEPOT, Math.toRadians(45)).build(),
#           robot.lowBasketAction()
#       );
#   }


def ex10():
    print("see comments in this file for reflection + Java translation")


if __name__ == "__main__":
    for name in ["ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10"]:
        print(name); globals()[name]()
