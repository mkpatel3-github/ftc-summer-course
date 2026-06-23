# Chapter 15 — Command-Based Programming

> Goal: organize robot behavior the way the top teams (and Juice's `commands/` folder) do
> — as small, reusable **Commands** that a **scheduler** runs and combines. This is the
> grown-up version of the state machine from Chapter 8, and it's how you keep a complex
> robot from becoming one giant unreadable loop.

## The problem it solves

By Chapter 10 your autonomous was a list of steps you ran in order. That works until you
need to do two things **at once** (drive while raising the lift), or reuse a step in five
different routines. Cramming all that into one `while` loop gets tangled fast.

**Command-based programming** breaks behavior into little objects called **Commands**.
Each Command knows how to do *one thing* across many loops and how to report **"am I done
yet?"**. A **scheduler** ticks them. You then **compose** them:

- run them **one after another** (`SequentialCommand`)
- run them **at the same time** (`ParallelCommand`)
- do something **instantly** (`InstantCommand`)
- **wait** (`SleepCommand`)

Juice's real repo has exactly these in `commands/primitives/`: `InstantCommand.java`,
`SequentialCommand.java`, `ParallelCommand.java`, `LoopCommand.java`, `SleepCommand.java`,
with a `CommandMaster.java` running them. Popular libraries that give you this for free:
**FTCLib**, **NextFTC**, and **SolversLib**.

## A Command in our sim

A `Command` has `init()`, `update()` (returns `True` when finished), and `end()`:

```python
from ftcsim import Command, InstantCommand, SequentialCommand, ParallelCommand, \
                    SleepCommand, CommandScheduler

class DriveForward(Command):
    def __init__(self, robot, seconds):
        self.robot, self.seconds, self.t = robot, seconds, 0.0
    def init(self):
        self.robot.set_drive_power(0, 1.0, 0)
    def update(self):
        self.t += 0.02
        return self.t >= self.seconds          # True == done
    def end(self):
        self.robot.set_drive_power(0, 0, 0)

scheduler = CommandScheduler()
scheduler.run(robot, DriveForward(robot, 1.0))
```

`InstantCommand(fn)` runs `fn` once. `SleepCommand(sec)` waits. `SequentialCommand(a, b)`
runs a, then b. `ParallelCommand(a, b)` runs both until *both* finish.

## Why it scales

Once your actions are Commands, a whole autonomous reads like a sentence:

```python
auto = SequentialCommand(
    DriveForward(robot, 1.0),
    ParallelCommand(DriveForward(robot, 0.5), RaiseLift(robot, 800)),
    InstantCommand(lambda: print("SCORE")),
)
```

You can read that out loud and it's *exactly* what the robot does. That readability is why
serious teams adopt command-based.

---

## Exercises

Import from the sim: `Command, InstantCommand, SequentialCommand, ParallelCommand,
SleepCommand, CommandScheduler`. Use `CommandScheduler().run(robot, command)`.

**1. Your first command.** Write a `DriveForward(Command)` like the example. Run it with
the scheduler for 1s and print the pose. Confirm the robot moved and then stopped (end()).

**2. InstantCommand.** Use `InstantCommand(lambda: print("CLAW OPEN"))` and run it. Confirm
it prints once and finishes immediately.

**3. SleepCommand.** Run a `SequentialCommand(InstantCommand(print "start"),
SleepCommand(0.5), InstantCommand(print "end"))`. Confirm "start" then a pause then "end".

**4. Sequential drive.** Build a `SequentialCommand` that drives forward 1s, then strafes
1s (write a `Strafe` command). Print the pose after — it should show both legs.

**5. Parallel actions.** Write a `Spin` command (sets rx) and run `ParallelCommand(
DriveForward(robot, 1.0), Spin(robot, 1.0))`. Show the robot both moved *and* rotated —
something a plain sequence can't do in the same second.

**6. "Done yet?" logic.** Write a `DriveToX(robot, target_x)` command whose `update()`
returns True only when `robot.x >= target_x`. Run it and confirm it stops near the target,
not after a fixed time. (Commands end on a *condition*, not a clock.)

**7. Compose a mini-auto.** Combine your commands into a `SequentialCommand` that: drives
to x=30, then in parallel (drives a bit + prints "LIFT UP"), then an InstantCommand prints
"SCORE". Read it out loud — does the code match the sentence?

**8. Reuse.** Show off the payoff: build *two* different autos from the **same** command
classes (e.g. a "left" routine and a "right" routine) without rewriting the commands.
In a comment, note how this compares to copy-pasting loop code.

**9. A LoopCommand.** Juice has `LoopCommand.java`. Write a `LoopCommand(fn, times)` that
calls `fn` once per `update()` and finishes after `times` updates. Use it to print a
countdown 3,2,1. (This is how you fold repeated behavior into the scheduler.)

**10. State machine vs commands.** In a comment, compare Chapter 8's `Levels` state machine
with command-based: when is a simple enum state machine *enough*, and when do commands earn
their complexity? (Hint: number of subsystems acting at once.) Both are correct tools —
explain how you'd choose.

## Java bridge (Juice's commands/ folder)

```java
// Juice's SequentialCommand.java in spirit:
Command auto = new SequentialCommand(
    new DriveForward(robot, 1.0),
    new ParallelCommand(
        new DriveForward(robot, 0.5),
        new RaiseLift(robot, 800)
    ),
    new InstantCommand(() -> claw.score())
);
CommandMaster.schedule(auto);   // CommandMaster.java ticks it every loop
```

With **FTCLib/NextFTC** you'd extend their `CommandBase` and call `schedule(...)` — the
exact same shapes you built here. You now understand Juice's whole `commands/` directory.

➡️ Solutions: [`solutions/15_solution.py`](../solutions/15_solution.py)
