"""Chapter 16 solutions - Modern Autonomous: Driving to Poses."""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
from ftcsim import (Robot, Pose2d, DriveToPoseAction, SequentialAction,
                    run_action)


def ex1():
    r = Robot()
    run_action(r, DriveToPoseAction(r, Pose2d(30, 0, 0)))
    print("arrived:", r.pose_str())


def ex2():
    r = Robot()
    run_action(r, DriveToPoseAction(r, Pose2d(0, 0, 90)))
    print("turned in place:", r.pose_str())


def ex3():
    r = Robot()
    run_action(r, DriveToPoseAction(r, Pose2d(20, 0, 0)))
    print("leg1:", r.pose_str())
    run_action(r, DriveToPoseAction(r, Pose2d(20, 20, 0)))
    print("leg2:", r.pose_str())


def ex4():
    r = Robot()
    box = SequentialAction(
        DriveToPoseAction(r, Pose2d(24, 0, 0)),
        DriveToPoseAction(r, Pose2d(24, 24, 0)),
        DriveToPoseAction(r, Pose2d(0, 24, 0)),
        DriveToPoseAction(r, Pose2d(0, 0, 0)),
    )
    run_action(r, box)
    print("box end (near 0,0):", r.pose_str())
    # More reliable than Ch12's timed square: the controller drives until it
    # ARRIVES at each corner, so battery/bumps don't change where it ends.


def ex5():
    for tol in (0.5, 5.0):
        r = Robot()
        run_action(r, DriveToPoseAction(r, Pose2d(30, 0, 0), tol=tol))
        print(f"tol={tol}: {r.pose_str()}")
    # Loose tol on early legs = faster (don't waste time nailing a waypoint);
    # tight tol on the scoring leg = accuracy where points depend on it.


def ex6():
    r = Robot(start_x=-30, start_y=-60, start_heading=0)
    run_action(r, DriveToPoseAction(r, Pose2d(0, 0, 0)))
    print("from corner to center:", r.pose_str())


def ex7():
    print("""A pose-based action measures the ERROR between where odometry says
it is and the target, and drives until that error is ~0. Low battery just
means it pushes a little longer to cover the same distance -- it still ARRIVES.
"Drive 1.5s at 0.6 power" computes no error and watches no sensor, so a weak
battery travels less and it stops short. The controller closing the loop is
what makes pose-based autonomous battery-proof.""")


def ex8():
    r = Robot(start_x=-30, start_y=-60, start_heading=0)
    run_action(r, DriveToPoseAction(r, Pose2d(-50, -50, 45)))
    print("at basket:", r.pose_str(), "-> SCORE")
    run_action(r, DriveToPoseAction(r, Pose2d(-30, -30, 0)))
    print("at sample:", r.pose_str(), "-> PICKUP")


def ex9():
    r = Robot()
    run_action(r, DriveToPoseAction(r, Pose2d(30, 0, 0)))
    print("LIFT + SCORE")  # an InstantCommand-style mechanism step
    print("end:", r.pose_str())
    # A real auto runs the drive action and a lift command IN PARALLEL so the
    # lift is already up by the time the robot arrives -- no wasted seconds.


def ex10():
    print("""Mission: score 3 samples in the basket, then park.
Plan (targets + mechanisms):
  1. seed start pose (-35, -60, 90)
  2. DriveToPose(-50, -50, 45)   ; raise lift (parallel) ; SCORE sample #1
  3. DriveToPose(-36, -48, 0)    ; intake               ; PICKUP sample #2
  4. DriveToPose(-50, -50, 45)   ; raise lift            ; SCORE sample #2
  5. DriveToPose(-24, -48, 0)    ; intake               ; PICKUP sample #3
  6. DriveToPose(-50, -50, 45)   ; raise lift            ; SCORE sample #3
  7. DriveToPose(-10, -36, 0)    ; PARK""")
    r = Robot(start_x=-35, start_y=-60, start_heading=90)
    auto = SequentialAction(
        DriveToPoseAction(r, Pose2d(-50, -50, 45)),
        DriveToPoseAction(r, Pose2d(-36, -48, 0)),
        DriveToPoseAction(r, Pose2d(-50, -50, 45)),
        DriveToPoseAction(r, Pose2d(-10, -36, 0)),
    )
    run_action(r, auto)
    print("autonomous end (parked):", r.pose_str())


if __name__ == "__main__":
    for name in ["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10"]:
        print("\n===", name, "===")
        globals()[name]()
