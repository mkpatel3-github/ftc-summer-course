# Chapter 16 — Modern Autonomous: Driving to Poses

> Goal: write autonomous the way every competitive team does in 2024+ — by saying "go to
> *this spot* on the field" and letting a controller + odometry get you there, instead of
> timing motor powers. This is the world of **RoadRunner 1.0 Actions** and **Pedro
> Pathing**, and it's Juice's `BucketSide.java` + `KalmanDrive.java` working together.

## From "drive 2 seconds" to "go to (30, 0)"

In Chapter 9 you sequenced *timed* moves. The problem: timing is fragile. A low battery, a
bump, a slightly different start — and "1.5 seconds forward" lands somewhere new.

Modern autonomous is **pose-based**. You have odometry (Chapter 13) telling you where you
are, so you just command **targets**:

```python
go_to(Pose2d(30, 0, 0))      # drive to x=30, then
go_to(Pose2d(30, 24, 90))    # drive to (30,24) and face 90 deg
```

A controller (a P-controller — same family as Chapter 7's PID) looks at the error between
where you *are* and where you *want to be*, and drives to close it. When the error is small
enough, that leg is done and the next begins. Battery and bumps don't matter — it drives
until it *arrives*.

## Actions: the RoadRunner 1.0 / Pedro style

RoadRunner 1.0 introduced the **Action** API: an action's `run()` returns `True` while it
still has work and `False` when finished. You chain them with `SequentialAction`. (Note:
this is the *opposite* return convention from Chapter 15's Commands — RoadRunner really
does return `true` to mean "keep going.") Our sim mirrors it:

```python
from ftcsim import Pose2d, DriveToPoseAction, SequentialAction, run_action

auto = SequentialAction(
    DriveToPoseAction(robot, Pose2d(30, 0, 0)),
    DriveToPoseAction(robot, Pose2d(30, 24, 90)),
)
run_action(robot, auto)
```

`DriveToPoseAction` is a P-controller that drives to a target `Pose2d` and stops. That's a
teaching-sized version of what a RoadRunner trajectory or a Pedro path does — real ones
also follow smooth **splines** and respect acceleration limits (motion profiling), but the
*sequencing* idea is identical.

## The big picture (how it all connects)

This is where the whole course comes together:

- **Odometry** (Ch 13) says where you are.
- **Vision** (Ch 14) corrects drift, fused by a **Kalman filter** → Juice's `KalmanDrive`.
- A **controller** (Ch 7 PID) drives to each target pose.
- **Actions/Commands** (Ch 15) sequence and parallelize the steps.
- The result is a robust **autonomous** like Juice's `BucketSide.java`.

The tools real teams pick: **RoadRunner** (what Juice uses) and **Pedro Pathing** (a newer,
popular path follower). Both do the same job — turn "go here" into wheel powers.

---

## Exercises

Import `Pose2d, DriveToPoseAction, SequentialAction, run_action` from the sim. The robot
starts at `(0,0,0)`. `DriveToPoseAction(robot, target, tol=1.0)` drives to a target and
finishes (stops) within `tol` inches / a couple degrees of heading.

**1. Drive to a point.** Run a single `DriveToPoseAction(robot, Pose2d(30, 0, 0))` with
`run_action`. Print the final pose — it should be near (30, 0, 0).

**2. Drive and turn.** Target `Pose2d(0, 0, 90)` — same spot, but rotate to face 90°.
Confirm the heading ends near 90.

**3. Two legs.** `SequentialAction` of `(20, 0, 0)` then `(20, 20, 0)`. Print the pose
after each? (Tip: run them as two separate `run_action` calls so you can print between.)
The robot should trace an L.

**4. A box.** Sequence four targets that drive a 24" square back to the start. Print the
final pose; it should be near (0,0). Compare in a comment to Chapter 12's *timed* square —
which is more reliable and why?

**5. Tolerance matters.** Run the same target with `tol=0.5` and again with `tol=5.0`.
Print both final poses and the difference. In a comment: why might a team use a *looser*
tolerance on early legs and a tight one on the scoring leg?

**6. Start somewhere else.** Make `Robot(start_x=-30, start_y=-60, start_heading=0)` (like
a real autonomous start corner) and drive to `Pose2d(0, 0, 0)`. Pose-based autonomous
doesn't care where you start, as long as odometry is seeded — show it arrives.

**7. Battery-proof.** This is the headline. In a comment, explain why this pose-based
action arrives at the same place whether the battery is full or low, while Chapter 9's
"drive 1.5s at 0.6 power" would not. Tie it back to the controller closing the error.

**8. Mimic BucketSide.** Juice's `BucketSide.java` drives to a scoring spot, scores, then
to a sample, repeatedly. Build a `SequentialAction` that drives to a "basket"
`Pose2d(-50, -50, 45)`, prints "SCORE", drives to a "sample" `Pose2d(-30, -30, 0)`, prints
"PICKUP". Run it and print the final pose.

**9. Combine with a command.** Bridge Chapters 15 and 16: after driving to a pose with an
action, run an `InstantCommand` (or just call a function) that prints "LIFT + SCORE". In a
comment, describe how a real auto interleaves *driving* (actions) with *mechanisms*
(commands) — often in parallel.

**10. Design your own autonomous.** Pick a made-up mission (e.g., "score 3 samples in the
basket, then park"). In a comment block, write the full sequence of `Pose2d` targets and
mechanism actions you'd run, in order. Then implement as much as you can with
`DriveToPoseAction` + prints. This is a real autonomous plan — the capstone of the whole
course.

## Java bridge (RoadRunner 1.0, what Juice runs)

```java
// RoadRunner 1.0 Action API (BucketSide.java in spirit):
Action auto = drive.actionBuilder(startPose)
        .splineTo(new Vector2d(30, 0), Math.toRadians(0))
        .splineTo(new Vector2d(30, 24), Math.toRadians(90))
        .build();

Actions.runBlocking(auto);   // runs the whole sequence to completion
```

`splineTo` follows a smooth curve (with motion profiling) instead of a straight P-drive,
but the mental model — *a sequence of "get to this pose" actions* — is precisely what you
built. With **Pedro Pathing** it's `follower.followPath(path)`; same idea, different
library. You can now read Juice's autonomous.

➡️ Solutions: [`solutions/16_solution.py`](../solutions/16_solution.py)
