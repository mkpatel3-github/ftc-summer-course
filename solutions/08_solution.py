"""Chapter 8 solutions - Subsystems & State Machines."""
import sys, os
from enum import Enum
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))

# Reuse the PID we built in Chapter 7.
sys.path.append(os.path.join(os.path.dirname(__file__)))
from importlib import import_module
MyPIDF = import_module("07_solution").MyPIDF


# --- ex1 ---
class Claw:
    def __init__(self):
        self.is_open = True

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False

    def status(self):
        return "OPEN" if self.is_open else "CLOSED"


def ex1():
    claw = Claw()
    print("before:", claw.status())
    claw.close()
    print("after: ", claw.status())


# --- ex3 (enum, used by later exercises) ---
class Levels(Enum):
    INIT = 0
    INTAKE = 1
    INTERMEDIATE = 2
    LOW_BASKET = 3
    HIGH_BASKET = 4
    LOW_RUNG = 5
    HIGH_RUNG = 6


def ex3():
    for lv in Levels:
        print(" ", lv.name)


# --- ex2 / ex4 ---
class Lift:
    PRESETS = {
        Levels.INIT: 0, Levels.INTAKE: -15, Levels.INTERMEDIATE: 0,
        Levels.LOW_BASKET: 1300, Levels.HIGH_BASKET: 2160,
        Levels.LOW_RUNG: 0, Levels.HIGH_RUNG: 960,
    }

    def __init__(self):
        self.pid = MyPIDF(0.02, 0.0, 0.00045, 0.125)
        self.ticks = 0.0
        self.target = 0.0

    def run_to_position(self, target):
        self.target = target

    def run_to_preset(self, level):
        self.run_to_position(self.PRESETS[level])

    def update(self):
        out = self.pid.update(self.ticks, self.target)
        self.ticks += out * 200 * 0.02

    def get_pos(self):
        return self.ticks

    def settle(self, loops=300):
        for _ in range(loops):
            self.update()
        return round(self.ticks, 1)


def ex2():
    lift = Lift()
    lift.run_to_position(1000)
    print("settled at:", lift.settle())


def ex4():
    lift = Lift()
    lift.run_to_preset(Levels.HIGH_BASKET)
    print("HIGH_BASKET settled at:", lift.settle(), "(target 2160)")


# --- ex5 / ex6 / ex7 ---
class Robot:
    def __init__(self):
        self.lift = Lift()
        self.state = Levels.INIT
        self.mode = "SAMPLE"

    def high_basket(self):
        self.lift.run_to_preset(Levels.HIGH_BASKET)
        self.state = Levels.HIGH_BASKET

    def high_rung(self):
        self.lift.run_to_preset(Levels.HIGH_RUNG)
        self.state = Levels.HIGH_RUNG

    def smart_outtake(self):
        if self.state in (Levels.LOW_BASKET, Levels.HIGH_BASKET):
            return "DROP SAMPLE"
        elif self.state in (Levels.LOW_RUNG, Levels.HIGH_RUNG):
            return "RELEASE SPECIMEN"
        return "NOTHING"

    def toggle_gamepiece(self):
        self.mode = "SPECIMEN" if self.mode == "SAMPLE" else "SAMPLE"

    def tele_deposit_preset(self):
        if self.mode == "SAMPLE":
            self.high_basket()
        else:
            self.high_rung()


def ex5():
    r = Robot()
    print("start state:", r.state.name)
    r.high_basket()
    print("after high_basket:", r.state.name, "target", r.lift.target)


def ex6():
    r = Robot()
    r.high_basket()
    print("at basket -> smart_outtake:", r.smart_outtake())
    r.high_rung()
    print("at rung   -> smart_outtake:", r.smart_outtake())


def ex7():
    r = Robot()
    r.tele_deposit_preset()
    print("SAMPLE mode deposit ->", r.state.name)
    r.toggle_gamepiece()
    r.tele_deposit_preset()
    print("SPECIMEN mode deposit ->", r.state.name)


# --- ex8 ---
ALLOWED = {
    Levels.INIT: {Levels.INTAKE, Levels.INTERMEDIATE},
    Levels.INTAKE: {Levels.INTERMEDIATE},
    Levels.INTERMEDIATE: {Levels.LOW_BASKET, Levels.HIGH_BASKET,
                          Levels.LOW_RUNG, Levels.HIGH_RUNG, Levels.INTAKE},
    Levels.LOW_BASKET: {Levels.INTERMEDIATE},
    Levels.HIGH_BASKET: {Levels.INTERMEDIATE},
    Levels.LOW_RUNG: {Levels.INTERMEDIATE},
    Levels.HIGH_RUNG: {Levels.INTERMEDIATE},
}


def can_transition(from_state, to_state):
    return to_state in ALLOWED.get(from_state, set())


def ex8():
    print("INTERMEDIATE->HIGH_BASKET (legal):",
          can_transition(Levels.INTERMEDIATE, Levels.HIGH_BASKET))
    print("INTAKE->HIGH_BASKET (illegal):    ",
          can_transition(Levels.INTAKE, Levels.HIGH_BASKET))


# --- ex9 ---
def ex9():
    r = Robot()
    sequence = [Levels.INTAKE, Levels.INTERMEDIATE, Levels.HIGH_BASKET]
    for nxt in sequence:
        if can_transition(r.state, nxt):
            r.state = nxt
            extra = ""
            if nxt in Lift.PRESETS and nxt in (Levels.HIGH_BASKET, Levels.LOW_BASKET,
                                               Levels.HIGH_RUNG, Levels.LOW_RUNG):
                r.lift.run_to_preset(nxt)
                extra = f"  lift target={r.lift.target}"
            print(f"  -> {r.state.name}{extra}")
        else:
            print(f"  REJECTED illegal transition to {nxt.name}")
    print("  smart_outtake:", r.smart_outtake())
    if can_transition(r.state, Levels.INTERMEDIATE):
        r.state = Levels.INTERMEDIATE
        print("  -> INTERMEDIATE (cycle complete)")


# --- ex10 ---
class Intake:
    """A simple game intake: states EMPTY -> INTAKING -> FULL."""
    def __init__(self):
        self.state = "EMPTY"

    def start(self):
        if self.state == "EMPTY":
            self.state = "INTAKING"

    def detect_piece(self):
        if self.state == "INTAKING":
            self.state = "FULL"

    def eject(self):
        self.state = "EMPTY"

    def status(self):
        return self.state


def ex10():
    intake = Intake()
    print("design: states EMPTY/INTAKING/FULL; hardware: 1 motor + color sensor;")
    print("methods: start(), detect_piece(), eject(), status()")
    print(" ", intake.status())
    intake.start(); print(" ", intake.status())
    intake.detect_piece(); print(" ", intake.status())
    intake.eject(); print(" ", intake.status())


if __name__ == "__main__":
    for name in ["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10"]:
        print(name); globals()[name]()
