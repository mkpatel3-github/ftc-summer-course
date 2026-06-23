"""Chapter 17 solutions - Robot Architecture: One Home for Hardware."""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
from ftcsim import Robot, run_for


class RobotHardware:
    """One object owns all the hardware, created once, shared everywhere."""
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = RobotHardware()
        return cls._instance

    def __init__(self):
        self.robot = Robot()

    def drive(self, x, y, rx):
        self.robot.set_drive_power(x, y, rx)

    def reverse_left_side(self):
        self.robot.front_left.reverse = not self.robot.front_left.reverse
        self.robot.back_left.reverse = not self.robot.back_left.reverse


class Globals:
    LIFT_GROUND = 0
    LIFT_LOW = 800
    LIFT_HIGH = 1600
    CLAW_OPEN = 0.6
    CLAW_CLOSED = 0.2
    ALLIANCE = "RED"


def ex1():
    a = RobotHardware.get_instance()
    b = RobotHardware.get_instance()
    print("same object?", a is b)


def ex2():
    hw = RobotHardware.get_instance()
    run_for(hw.robot, 1.0, lambda t: hw.drive(0, 1.0, 0))
    print("pose through singleton:", hw.robot.pose_str())


def ex3():
    for name in ("LIFT_GROUND", "LIFT_LOW", "LIFT_HIGH", "CLAW_OPEN", "CLAW_CLOSED"):
        print(name, "=", getattr(Globals, name))


def lift_preset(name):
    return {"GROUND": Globals.LIFT_GROUND,
            "LOW": Globals.LIFT_LOW,
            "HIGH": Globals.LIFT_HIGH}[name]


def ex4():
    print("HIGH ->", lift_preset("HIGH"))
    Globals.LIFT_HIGH = 2000           # one line changes the meaning everywhere
    print("HIGH after edit ->", lift_preset("HIGH"))
    Globals.LIFT_HIGH = 1600           # restore for other exercises
    # lift_preset never changed -- it reads the NAMED constant, not a number.


def scoring_x():
    return 50 if Globals.ALLIANCE == "RED" else -50


def ex5():
    Globals.ALLIANCE = "RED"
    print("RED scoring_x:", scoring_x())
    Globals.ALLIANCE = "BLUE"
    print("BLUE scoring_x:", scoring_x())
    Globals.ALLIANCE = "RED"           # restore


def teleop():
    hw = RobotHardware.get_instance()
    run_for(hw.robot, 1.0, lambda t: hw.drive(0, 1.0, 0))
    return hw


def auton():
    hw = RobotHardware.get_instance()
    return hw.robot.pose_str()


def ex6():
    teleop()                            # drives in one "OpMode"
    print("auton sees same robot:", auton())   # reads pose in the other


def ex7():
    hw = RobotHardware.get_instance()
    before = hw.robot.front_left.reverse
    hw.reverse_left_side()
    print("left reversed:", before, "->", hw.robot.front_left.reverse)
    hw.reverse_left_side()              # restore
    # Reversing in the singleton fixes it for TeleOp AND every Auto at once;
    # doing it per-OpMode is how you get "works in TeleOp, broken in auto".


class Lift:
    def __init__(self, hardware):
        self.hw = hardware
        self.position = Globals.LIFT_GROUND

    def go_to(self, name):
        self.position = lift_preset(name)
        return self.position


def ex8():
    hw = RobotHardware.get_instance()
    lift = Lift(hw)                     # never touches Robot directly
    print("GROUND ->", lift.go_to("GROUND"))
    print("HIGH ->", lift.go_to("HIGH"))


class TelemetryData:
    def __init__(self, mode, alliance, pose):
        self.mode = mode
        self.alliance = alliance
        self.pose = pose

    def show(self, telemetry):
        telemetry.add_data("mode", self.mode)
        telemetry.add_data("alliance", self.alliance)
        telemetry.add_data("pose", self.pose)
        telemetry.update()


def ex9():
    hw = RobotHardware.get_instance()
    data = TelemetryData("TELEOP", Globals.ALLIANCE, hw.robot.get_pose())
    data.show(hw.robot.telemetry)


def ex10():
    # BAD version: makes its own Robot, uses bare magic numbers.
    def bad_score():
        r = Robot()
        r.set_drive_power(0, 1.0, 0)
        claw = 0.6          # what is 0.6? a reader can't know
        lift = 1600         # what is 1600?
        return claw, lift
    print("bad:", bad_score())

    # GOOD version: shared hardware + named constants.
    def good_score():
        hw = RobotHardware.get_instance()
        hw.drive(0, 1.0, 0)
        return Globals.CLAW_OPEN, Globals.LIFT_HIGH
    print("good:", good_score())
    # Benefits: one shared hardware object (no duplicate config / reversed-motor
    # bugs), named constants (1600 -> LIFT_HIGH so readers know intent), and a
    # single edit point when gearing/positions change.


if __name__ == "__main__":
    for name in ["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10"]:
        print("\n===", name, "===")
        globals()[name]()
