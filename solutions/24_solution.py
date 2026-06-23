"""Chapter 24 solutions - Advanced Command-Based: Bindings, Requirements, Conditionals."""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
from ftcsim import (RunningCommandScheduler, Button, Subsystem, InstantCommand,
                    ConditionalCommand, SequentialCommand, Command)


def ex1():
    # Bind a button to a command; it fires only on the rising edge.
    state = {"pressed": False}
    sched = RunningCommandScheduler()
    sched.register_button(
        Button(lambda: state["pressed"]).when_pressed(InstantCommand(lambda: print("FIRE"))))
    state["pressed"] = True
    sched.run()                 # rising edge -> fires
    state["pressed"] = False
    sched.run()                 # no edge -> silent
    print("(no second FIRE above)")


def ex2():
    # Held button fires EXACTLY once, not every loop.
    state = {"pressed": True}
    fires = {"n": 0}
    sched = RunningCommandScheduler()
    sched.register_button(
        Button(lambda: state["pressed"]).when_pressed(
            InstantCommand(lambda: fires.__setitem__("n", fires["n"] + 1))))
    for _ in range(5):          # held True for 5 loops
        sched.run()
    print("fires while held 5 loops:", fires["n"], "(expect 1)")
    # Polling the flag directly (if state["pressed"]: fire()) would fire 5 times.
    # Edge detection turns "is it down?" into "did it just go down?" -- once.


def ex3():
    # Two buttons, two commands -- no was_pressed bookkeeping in the loop.
    a, b = {"v": False}, {"v": False}
    sched = RunningCommandScheduler()
    sched.register_button(Button(lambda: a["v"]).when_pressed(
        InstantCommand(lambda: print("open"))))
    sched.register_button(Button(lambda: b["v"]).when_pressed(
        InstantCommand(lambda: print("close"))))
    for press in ("a", "b", "a"):
        a["v"], b["v"] = (press == "a"), (press == "b")
        sched.run()
        a["v"], b["v"] = False, False
        sched.run()             # release between presses


class CountdownCommand(Command):
    """Takes N loops to finish, so we can observe it being cancelled."""
    def __init__(self, name, loops):
        self.name, self.loops, self._left = name, loops, loops
    def update(self):
        self._left -= 1
        return self._left <= 0
    def end(self):
        pass


def ex4():
    # Shared requirement -> scheduling the second cancels the first.
    claw = Subsystem()
    sched = RunningCommandScheduler()
    first = CountdownCommand("first", 10).requires(claw)
    second = CountdownCommand("second", 10).requires(claw)
    sched.schedule(first)
    sched.run()                                 # tick once
    sched.schedule(second)                      # shares claw -> cancels first
    print("first scheduled?", sched.is_scheduled(first), "(expect False)")
    print("second scheduled?", sched.is_scheduled(second), "(expect True)")


def ex5():
    # Different subsystems -> no cancel, both run together.
    claw, lift = Subsystem(), Subsystem()
    sched = RunningCommandScheduler()
    a = CountdownCommand("a", 10).requires(claw)
    b = CountdownCommand("b", 10).requires(lift)
    sched.schedule(a)
    sched.schedule(b)
    print("a scheduled?", sched.is_scheduled(a), " b scheduled?", sched.is_scheduled(b))
    # Requirements are PER-SUBSYSTEM: only commands fighting over the SAME
    # mechanism cancel each other. A claw command and a lift command are
    # independent, so both run at once -- which is what you want in TeleOp.


def ex6():
    # ConditionalCommand picks a branch from the condition AT INIT.
    state = {"closed": True}
    cmd_true = ConditionalCommand(
        on_true=InstantCommand(lambda: print("OPEN")),
        on_false=InstantCommand(lambda: print("CLOSE")),
        condition=lambda: state["closed"])
    cmd_true.init(); cmd_true.update()          # closed -> OPEN
    state["closed"] = False
    cmd_false = ConditionalCommand(
        on_true=InstantCommand(lambda: print("OPEN")),
        on_false=InstantCommand(lambda: print("CLOSE")),
        condition=lambda: state["closed"])
    cmd_false.init(); cmd_false.update()        # open -> CLOSE


def make_toggle(state):
    """Fresh ConditionalCommand that opens/closes and flips the flag."""
    def open_it():
        print("OPEN"); state["closed"] = False
    def close_it():
        print("CLOSE"); state["closed"] = True
    return ConditionalCommand(
        on_true=InstantCommand(open_it),        # closed -> open
        on_false=InstantCommand(close_it),      # open -> close
        condition=lambda: state["closed"])


def ex7():
    # One button alternates open/close. A button binding needs a command that
    # re-reads state each press, so bind a small command that builds + runs a
    # fresh toggle each time it fires.
    state = {"closed": True}
    press = {"v": False}
    sched = RunningCommandScheduler()
    sched.register_button(Button(lambda: press["v"]).when_pressed(
        InstantCommand(lambda: _run_once(make_toggle(state)))))
    for _ in range(3):
        press["v"] = True; sched.run()
        press["v"] = False; sched.run()
    # closed -> OPEN -> CLOSE -> OPEN


def _run_once(cmd):
    cmd.init()
    cmd.update()
    cmd.end()


def ex8():
    # Nested ConditionalCommand: a 3-state toggle, KookyBotz ClawToggleCommand.
    state = {"s": "CLOSED"}
    def set_to(name):
        return InstantCommand(lambda: state.__setitem__("s", name))
    def make_3state():
        # if CLOSED -> INTERMEDIATE; elif INTERMEDIATE -> OPEN; else -> CLOSED
        return ConditionalCommand(
            on_true=set_to("INTERMEDIATE"),
            on_false=ConditionalCommand(
                on_true=set_to("OPEN"),
                on_false=set_to("CLOSED"),
                condition=lambda: state["s"] == "INTERMEDIATE"),
            condition=lambda: state["s"] == "CLOSED")
    for _ in range(4):
        _run_once(make_3state())
        print("state:", state["s"])
    # CLOSED->INTERMEDIATE->OPEN->CLOSED->INTERMEDIATE. Maps to the Java bridge:
    # outer condition = isClosed (-> INTERMEDIATE), nested = isIntermediate
    # (-> OPEN) else CLOSED.


def ex9():
    # A requirement cancels a SequentialCommand mid-run -- correct for a driver
    # who changes their mind.
    lift = Subsystem()
    sched = RunningCommandScheduler()
    seq = SequentialCommand(
        CountdownCommand("step1", 3),
        CountdownCommand("step2", 3),
        CountdownCommand("step3", 3)).requires(lift)
    sched.schedule(seq)
    sched.run(); sched.run()                    # a couple loops into the sequence
    print("sequence scheduled mid-run?", sched.is_scheduled(seq))
    takeover = CountdownCommand("takeover", 5).requires(lift)
    sched.schedule(takeover)                    # shares lift -> cancels sequence
    print("sequence after takeover?", sched.is_scheduled(seq), "(expect False)")
    print("takeover scheduled?", sched.is_scheduled(takeover))
    # The driver pressed a new button; the half-finished lift routine must yield
    # immediately rather than fight the new command for the same motor.


def ex10():
    # A tiny TeleOp: scheduler, two subsystems, two bound buttons, a 30-loop match.
    drive, claw = Subsystem(), Subsystem()
    gp = {"a": False, "b": False}
    sched = RunningCommandScheduler()
    sched.register_button(Button(lambda: gp["a"]).when_pressed(
        InstantCommand(lambda: print("  -> claw command")).requires(claw)))
    sched.register_button(Button(lambda: gp["b"]).when_pressed(
        InstantCommand(lambda: print("  -> drive command")).requires(drive)))
    script = {5: "a", 10: "b", 20: "a"}         # press these on these loops
    for loop in range(30):
        gp["a"] = gp["b"] = False
        if loop in script:
            gp[script[loop]] = True
            print(f"loop {loop}: press {script[loop]}")
        sched.run()
    # This loop body == CommandScheduler.getInstance().run(): it polls bindings,
    # runs commands, and enforces requirements. Compared to a Ch 6 polling loop,
    # you no longer hand-write was_pressed edge detection per button, nor guard
    # against two commands driving the same mechanism -- the framework does both.


if __name__ == "__main__":
    for name in ["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10"]:
        print("\n===", name, "===")
        globals()[name]()
