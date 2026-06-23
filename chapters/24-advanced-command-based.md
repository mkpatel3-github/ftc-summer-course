# Chapter 24 — Advanced Command-Based: Bindings, Requirements & Conditionals

> Goal: level up the command framework from Chapter 15. Bind gamepad buttons to commands
> (`whenPressed`), give subsystems **requirements** so two commands can't fight over the same
> mechanism, and pick behavior at runtime with `ConditionalCommand`. This is exactly how
> KookyBotz and Seattle Solvers structure a real TeleOp on top of FTCLib.

## Where Chapter 15 left off

In Chapter 15 you built Commands and ran one to completion with a scheduler. That's enough for
autonomous, where you script a sequence. But **TeleOp** is different: the driver presses
buttons at unpredictable times, several mechanisms run at once, and you must never let two
pieces of code drive the same motor in the same loop. Real teams solve this with three ideas.

## Idea 1: button bindings (declare, don't poll)

In Chapter 6 you hand-rolled edge detection (`pressed && !wasPressed`). It works, but every
button needs its own `was_pressed` variable and an `if` in the loop — it gets messy fast.
FTCLib lets you **declare** the mapping once, at init:

```python
from ftcsim import Button, RunningCommandScheduler, InstantCommand

sched = RunningCommandScheduler()
sched.register_button(
    Button(lambda: gamepad.a).when_pressed(InstantCommand(fire))
)
# ...then each loop, just:
sched.run()      # polls buttons, fires commands on the rising edge
```

No per-button state in your loop, no repeated edge-detection code. The binding *is* the
intent: "when A is pressed, run this command."

## Idea 2: requirements (one command per subsystem)

Here's the bug that bites every team: two commands both try to drive the claw in the same
loop — one says "open," one says "close" — and the servo jitters or does the wrong thing. The
fix is **requirements**. A command declares which subsystems it needs:

```python
from ftcsim import Subsystem, InstantCommand

claw = Subsystem()
open_cmd  = InstantCommand(open_claw).requires(claw)
close_cmd = InstantCommand(close_claw).requires(claw)
```

When you `schedule()` a command, the scheduler **cancels any running command that shares a
requirement**. So scheduling `close_cmd` automatically stops `open_cmd` — they can never run
together. One subsystem, one command, guaranteed. (FTCLib calls this `addRequirements(...)`.)

## Idea 3: ConditionalCommand (pick at runtime)

Sometimes which command to run depends on *current state* — and you don't know that until the
button is pressed. `ConditionalCommand` chooses between two commands using a condition checked
at init:

```python
from ftcsim import ConditionalCommand

toggle = ConditionalCommand(
    on_true  = InstantCommand(open_claw),
    on_false = InstantCommand(close_claw),
    condition = lambda: claw_is_closed(),    # checked when the command starts
)
```

KookyBotz's real `ClawToggleCommand` **nests** these to make a 3-state toggle
(closed → open → intermediate → closed) from one button. The whole behavior is data, not a
pile of `if`s scattered through the loop.

## Java bridge (KookyBotz, on FTCLib)

```java
// Button binding (Solo.java):
gamepadEx.getGamepadButton(GamepadKeys.Button.RIGHT_BUMPER)
         .whenPressed(new ClawToggleCommand(robot, ClawSide.LEFT));

// ConditionalCommand nested for a 3-state toggle (ClawToggleCommand.java):
super(
    new ClawCommand(INTERMEDIATE, side),                       // if currently closed
    new ConditionalCommand(
        new ClawCommand(OPEN, side),                           // if currently intermediate
        new ClawCommand(CLOSED, side),                         // otherwise
        () -> robot.intake.getClawState(side) == INTERMEDIATE),
    () -> robot.intake.getClawState(side) == CLOSED);

// Each loop, the whole thing is one call:
CommandScheduler.getInstance().run();   // polls bindings, runs commands, enforces requirements
```

---

## Exercises

Use `from ftcsim import (RunningCommandScheduler, Button, Subsystem, InstantCommand,
ConditionalCommand, SequentialCommand, Command)`. A `Button(read_fn)` edge-detects `read_fn()`;
`.when_pressed(cmd)` sets the command. Register buttons on a `RunningCommandScheduler` and call
`.run()` each loop. `cmd.requires(sub)` declares a requirement.

**1. Bind a button.** Make a `RunningCommandScheduler` and a `Button` reading a flag you
control. Bind it (`when_pressed`) to an `InstantCommand` that prints "FIRE". Flip the flag
True and call `sched.run()`; show it fires. Set it back False, run again; show it does **not**
re-fire. (Edge detection, for free.)

**2. Only on the rising edge.** Keep the flag True for 5 consecutive `run()` calls. Count how
many times the command fires. Show it's **exactly once** — held buttons don't repeat. In a
comment, contrast with polling the flag directly in a loop.

**3. Two buttons, two commands.** Bind button A to "open" and button B to "close" (each an
`InstantCommand` printing its name). Press A, then B, then A. Show the prints follow your
presses. No `was_pressed` variables in your loop.

**4. A subsystem requirement.** Make a `Subsystem` `claw`. Build two commands that both
`.requires(claw)` but take several loops to finish (subclass `Command`, finish after N
updates). Schedule the first, tick once, then schedule the second. Show the first is **no
longer scheduled** (`sched.is_scheduled`) — the second cancelled it.

**5. No shared requirement, no cancel.** Repeat exercise 4 but give the two commands
**different** subsystems (`claw` and `lift`). Schedule both. Show **both** stay scheduled and
run at the same time. In a comment: this is why requirements are per-subsystem, not global.

**6. ConditionalCommand basics.** Make a `claw_closed` flag. Build a `ConditionalCommand` that
runs "OPEN" when closed and "CLOSE" when open. Run it with the flag True, then False; show it
picks the right branch each time based on the condition **at init**.

**7. A real toggle.** Wire exercise 6 to a button so one button alternates open/close. Have
each branch also flip the `claw_closed` flag. Press the button three times; show it goes
closed→open→closed→open. This is a one-button toggle, the command-based way.

**8. Nested conditional (3-state).** Mimic KookyBotz's `ClawToggleCommand`: a state variable
that is "CLOSED", "OPEN", or "INTERMEDIATE", and a nested `ConditionalCommand` so one button
cycles closed→intermediate→open→… Print the state after each press. In a comment, match it to
the Java bridge above.

**9. Requirement during a sequence.** Schedule a `SequentialCommand` (several steps, requires
`lift`) and let it run a couple loops. Mid-sequence, schedule a different command that also
requires `lift`. Show the sequence is cancelled and the new command takes over. Explain why
this is the *correct* behavior for a driver who changes their mind mid-action.

**10. A tiny TeleOp.** Put it together: a scheduler, two subsystems (`drive`, `claw`), a couple
of buttons bound to commands, and a 30-loop "match" where you script some button presses by
flipping flags on certain loops. Print what runs each loop. In a comment, map your loop body to
KookyBotz's `CommandScheduler.getInstance().run()` and explain what you'd no longer have to
hand-write compared to a Chapter 6 polling loop.

## Java bridge

```java
// A complete TeleOp init, in spirit -- declarative bindings, then a one-line loop:
gamepadEx.getGamepadButton(Button.A).whenPressed(new ClawToggleCommand(robot, LEFT));
gamepadEx.getGamepadButton(Button.B).whenPressed(new LiftCommand(robot, HIGH));
while (opModeIsActive()) {
    CommandScheduler.getInstance().run();   // bindings + requirements + scheduling, all here
}
```

You now have the TeleOp architecture real teams ship: behavior declared as commands, inputs
bound to them, and a scheduler that guarantees no two commands ever fight over a mechanism.

➡️ Solutions: [`solutions/24_solution.py`](../solutions/24_solution.py)
