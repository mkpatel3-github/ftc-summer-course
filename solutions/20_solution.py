"""Chapter 20 solutions - Swappable Localizers."""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
from ftcsim import (Robot, Localizer, DriveEncoderLocalizer, DeadWheelLocalizer,
                    OTOSLocalizer, run_for)


def ex1():
    r = Robot()
    for L in (DriveEncoderLocalizer(r), DeadWheelLocalizer(r), OTOSLocalizer(r)):
        print(type(L).__name__, L.get_pose())


def report(localizer):
    # interface-only code: no idea which concrete type this is.
    print(localizer.get_pose())


def ex2():
    r = Robot()
    for L in (DriveEncoderLocalizer(r), DeadWheelLocalizer(r), OTOSLocalizer(r)):
        report(L)


def ex3():
    r = Robot()
    enc, dead, otos = DriveEncoderLocalizer(r), DeadWheelLocalizer(r), OTOSLocalizer(r)
    # 1.0s keeps the robot off the field wall so drift isn't hidden by clamping.
    # forward stick (y) moves the sim robot along +x at heading 0.
    run_for(r, 1.0, lambda t: r.set_drive_power(0, 1.0, 0))
    print("true x:", round(r.x, 3))
    print("encoder:", enc.get_pose())     # biggest x drift
    print("deadwheel:", dead.get_pose())  # tiny drift
    print("otos:", otos.get_pose())       # jitter, not trend
    # drive-encoder drifts most (each read adds bias); deadwheel barely drifts.


def ex4():
    r = Robot()
    results = {}
    for name, L in (("encoder", DriveEncoderLocalizer(r)),
                    ("deadwheel", DeadWheelLocalizer(r)),
                    ("otos", OTOSLocalizer(r))):
        first = L.get_pose().x
        for _ in range(18):
            L.get_pose()
        last = L.get_pose().x
        results[name] = abs(last - first)
        print(f"{name}: first={first:.3f} last={last:.3f} wander={results[name]:.3f}")
    ranked = sorted(results, key=results.get)
    print("least->most wander:", ranked)
    # encoder = wheel slip accumulates (worst), deadwheel = clean pods (best),
    # otos = optical jitter (noisy but unbiased, doesn't trend away).


def drive_until_x(robot, localizer, target_x):
    def loop(t):
        if localizer.get_pose().x < target_x:
            robot.set_drive_power(0, 1.0, 0)
        else:
            robot.set_drive_power(0, 0, 0)
    run_for(robot, 3.0, loop)
    return localizer.get_pose()


def ex5():
    r1 = Robot(start_heading=0)         # face +x so forward increases x... but
    # the sim's "forward" stick is +y; drive along +x by strafing instead:
    def make_loop(robot, localizer, target_x):
        def loop(t):
            if localizer.get_pose().x < target_x:
                robot.set_drive_power(1.0, 0, 0)   # strafe +x
            else:
                robot.set_drive_power(0, 0, 0)
        return loop

    r = Robot()
    enc = DriveEncoderLocalizer(r)
    run_for(r, 3.0, make_loop(r, enc, 20))
    print("encoder stopped at:", enc.get_pose())

    r2 = Robot()
    dead = DeadWheelLocalizer(r2)
    run_for(r2, 3.0, make_loop(r2, dead, 20))
    print("deadwheel stopped at:", dead.get_pose())
    # SAME function, swapped strategy -- only the localizer object differs.


class PerfectLocalizer(Localizer):
    def __init__(self, robot):
        self._robot = robot

    def get_pose(self):
        return self._robot.get_pose()      # true pose, zero drift/noise


def ex6():
    r = Robot()
    run_for(r, 1.0, lambda t: r.set_drive_power(0, 1.0, 0))
    report(PerfectLocalizer(r))            # works because it honors the contract


class BrokenLocalizer(Localizer):
    pass                                    # forgot to implement get_pose()


def ex7():
    try:
        BrokenLocalizer().get_pose()
    except NotImplementedError as e:
        print("contract violation caught:", repr(e))
    # The interface raises at the POINT OF USE -- you find the broken contract
    # the moment anyone calls get_pose(), not via a silent wrong answer.


def ex8():
    r = Robot()
    strategies = {
        "encoder": DriveEncoderLocalizer(r),
        "deadwheel": DeadWheelLocalizer(r),
        "otos": OTOSLocalizer(r),
    }
    choice = "deadwheel"                     # imagine read from a config string
    print(f"using '{choice}':", strategies[choice].get_pose())


def ex9():
    r = Robot()
    drifting = DriveEncoderLocalizer(r)
    perfect = PerfectLocalizer(r)
    run_for(r, 2.0, lambda t: r.set_drive_power(0, 1.0, 0))
    gap = abs(drifting.get_pose().x - perfect.get_pose().x)
    print("drift gap:", round(gap, 3))
    # To combine: trust the smooth drifting source moment-to-moment (PREDICT),
    # but periodically pull it toward an absolute source (CORRECT). That weighted
    # blend is a Kalman filter -- Chapter 21.


def ex10():
    print("""Mid-season scenario: team buys a goBILDA Pinpoint to replace
drive-encoder odometry.
  WITH the Localizer interface: write ONE new PinpointLocalizer class and change
  ONE line where the localizer is constructed. Every drive/auto file that holds
  a `Localizer` keeps working untouched.
  WITHOUT it: position code copy-pasted everywhere means editing dozens of files,
  and the risk is you miss one -- a stale localizer in a single auto that silently
  uses the old hardware. The interface localizes the change to one place.""")


if __name__ == "__main__":
    for name in ["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10"]:
        print("\n===", name, "===")
        globals()[name]()
