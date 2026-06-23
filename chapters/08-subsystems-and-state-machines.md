# Chapter 8 — Subsystems & State Machines

> Goal: organize a robot the way Juice actually does. Stop writing one giant pile of
> code; instead build **subsystems** (a class per mechanism) and a **state machine** (the
> `Levels` enum) that decides what the robot is doing right now. This is the leap from
> "code that works" to "code a team can build on."

## Why subsystems

Juice's robot has a lift, an arm, an extension, a claw, a climber. Each is its own
**class** with its own methods. Look at `Robot.java`:

```java
public Lift lift;
public Arm arm;
public Claw claw;
...
this.lift = new Lift((Motor) components[4], (Motor) components[5], voltageSensor);
this.claw = new Claw(...);
```

And each subsystem hides its details. `Lift.java` exposes friendly methods —
`runToPosition(ticks)`, `runToPreset(level)`, `update()` — and *hides* the PID, the
voltage compensation, the two motors. The rest of the robot just says "lift, go to high
basket" and trusts the lift to figure out how.

That's **encapsulation**: the same idea as a Python class with methods. You already know
this from Python; FTC just makes it the backbone of the whole robot.

## Why a state machine

A match is chaos: the driver mashes buttons. How does the robot know whether pressing
"outtake" should drop a sample in a basket or clip a specimen on a rung? **It depends on
what state the robot is in.** Juice tracks this with one enum, `Levels`:

```java
public enum Levels {
    ZERO, INIT, INTAKE, INTERMEDIATE, LOCATING_TARGETS,
    LOW_BASKET, HIGH_BASKET, LOW_RUNG, HIGH_RUNG,
    CLIMB_EXTENDED, CLIMB_RETRACTED, CLIMB_PRIMED, ASCENDING, ...
}
```

and a field `public Levels state`. Every preset sets the state, and behavior *branches*
on it. The cleanest example is `smartOuttake()`:

```java
if (state == Levels.LOW_BASKET || state == Levels.HIGH_BASKET) {
    outtakeSample();          // we're at a basket -> drop a sample
} else if (state == Levels.LOW_RUNG || state == Levels.HIGH_RUNG) {
    outtakeSpecimen();        // we're at a rung -> release a specimen
}
```

One button, smart behavior, because the robot **knows its state**. A state machine is
just: *a current state + rules for moving between states + behavior that depends on the
state.* You'll build a small one.

## Presets

Notice `runToPreset(Levels level)` in `Lift.java` — a big if/else mapping each state to a
target number (`HIGH_BASKET -> 2160`, `HIGH_RUNG -> 960`). Presets turn "go to high
basket" into the exact encoder targets for lift, arm, and extension *together*. This is
how a driver scores in one button press.

---

## Exercises

For these you'll write plain Python classes plus use the sim. A "Lift" here is modeled
by a PID pushing a `ticks` value toward a target (reuse Chapter 7).

**1. A Claw class.** Write a `Claw` class with `is_open` state and methods `open()`,
`close()`, and `status()` (returns "OPEN"/"CLOSED"). This mirrors `Claw.java`'s
start/stop intake. Use it; print status before and after closing.

**2. Encapsulate a Lift.** Write a `Lift` class wrapping a `MyPIDF` (from Ch.7) and a
`ticks` value. Methods: `run_to_position(target)`, `update()` (one PID step), `get_pos()`.
Drive it to 1000 and loop `update()` until it settles.

**3. The Levels enum.** Use Python's `enum` to recreate a trimmed `Levels`: `INIT`,
`INTAKE`, `INTERMEDIATE`, `LOW_BASKET`, `HIGH_BASKET`, `LOW_RUNG`, `HIGH_RUNG`. Print all
of them.

**4. Lift presets.** Give `Lift` a `run_to_preset(level)` method that maps each `Levels`
value to a target tick count (use Juice's real numbers: HIGH_BASKET=2160, HIGH_RUNG=960,
INTAKE=-15, others 0). Send it to HIGH_BASKET and settle.

**5. A Robot with a state.** Write a small `Robot` wrapper class holding a `lift` and a
`state` field (a `Levels`). Methods `high_basket()` and `high_rung()` that set BOTH the
lift preset AND `self.state`. Verify state updates when you call them.

**6. smartOuttake.** Add `smart_outtake()` that returns `"DROP SAMPLE"` if state is a
basket, `"RELEASE SPECIMEN"` if state is a rung, else `"NOTHING"`. Test it after calling
`high_basket()` and after `high_rung()`. (This is the real `smartOuttake` logic.)

**7. toggleGamepiece.** Add a `mode` ("SAMPLE"/"SPECIMEN") and a `toggle_gamepiece()`
method that flips it (mirror `Robot.toggleGamepiece`). Also add `tele_deposit_preset()`
that calls `high_basket()` if mode is SAMPLE else `high_rung()`. Test both modes.

**8. Legal transitions.** Not every state can follow every other. Write a
`can_transition(from_state, to_state)` using a dictionary of allowed next-states (e.g.
from INTAKE you can go to INTERMEDIATE; from INTERMEDIATE to any scoring level; you can't
jump straight INTAKE→HIGH_BASKET). Test a legal and an illegal transition.

**9. Full sequence.** Drive the state machine through a realistic scoring cycle:
INIT → INTAKE → INTERMEDIATE → HIGH_BASKET → (smart_outtake) → INTERMEDIATE. At each step
print the state and, for scoring states, the lift target. Reject any illegal transition
using exercise 8.

**10. Design your own subsystem.** Pick a mechanism from a real FTC game (an intake, a
shooter, a hanger). On paper/comment: list its states, its hardware (motors/servos/
sensors), and the public methods you'd expose. Then implement a minimal version as a
Python class with at least 2 states and a `update()`/`status()`. This is exactly the
first thing you'll do on Juice for a new season.

## Java bridge

```java
// Your Robot wrapper IS Juice's Robot.java pattern:
public Levels state = Levels.INIT;

public void highBasket() {
    arm.runToPreset(Levels.HIGH_BASKET);
    extension.runToPreset(Levels.HIGH_BASKET);
    lift.runToPreset(Levels.HIGH_BASKET);
    state = Levels.HIGH_BASKET;     // <-- update the state!
}

public void smartOuttake() {
    if (state == Levels.LOW_BASKET || state == Levels.HIGH_BASKET) {
        outtakeSample();
    } else if (state == Levels.LOW_RUNG || state == Levels.HIGH_RUNG) {
        outtakeSpecimen();
    }
}
```

When you can explain why every preset method ends with `state = ...`, you understand the
single most important organizing idea in Juice's codebase.

➡️ Solutions: [`solutions/08_solution.py`](../solutions/08_solution.py)
