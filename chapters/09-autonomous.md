# Chapter 9 — Autonomous

> Goal: make the robot drive itself with no human, scoring points in the first 30 seconds
> of a match. You'll learn **poses** (where the robot is on the field), **sequencing**
> actions, and read Juice's real RoadRunner autonomous, `BucketSide.java`.

## A pose: x, y, heading

Autonomous is about *positions on the field*. A **pose** is three numbers:
`(x, y, heading)`. Juice's `BucketSide.java` starts with:

```java
Pose2d beginPose = new Pose2d(-30, -60, Math.toRadians(0));
```

That's "30 inches left of center, 60 inches down (at the wall), facing 0°." The field is
144"×144"; (0,0) is the middle. Our sim uses the same coordinate system.

## Two ways to do autonomous

**1. Dead reckoning** — string together the moves you already built: `drive_straight`,
`turn_to`, `drive_inches`. Simple, no extra libraries, and exactly what you can do today.
This is FLL-style autonomous, and it works.

**2. Trajectories (RoadRunner)** — Juice uses a library called RoadRunner that drives
smooth **splines** (curved paths) between poses while doing math to stay accurate. You
won't reimplement RoadRunner, but you'll learn to *read* it and mimic the structure.

Look at how Juice builds and runs paths in `BucketSide.java`:

```java
Action preload = drive.actionBuilder(drive.pose)
        .splineToLinearHeading(new Pose2d(-56, -56, Math.toRadians(45)), Math.toRadians(200))
        .waitSeconds(3)
        .build();
...
Actions.runBlocking(
    new SequentialAction(preload, spike1, depo1, spike2, depo2, spike3, depo3, park)
);
```

Two big ideas you CAN learn from this:
- A path is **built** first (`actionBuilder()...build()`), then **run**.
- The whole auto is a **`SequentialAction`**: a list of steps run one after another. That's
  just a Python list of functions you call in order!

## Sequencing = a list of steps

The deep idea behind `SequentialAction` is simple: an autonomous is a **list of moves run
in order**. You'll build your own tiny version: a list of `(action_name, function)` pairs
that you run one by one, printing progress — the same shape as Juice's auto.

---

## Exercises

Reuse your Chapter 3–4 helpers (`drive_straight`, `turn_to`, `drive_inches`). They're
re-provided in the solution file so this chapter stands alone.

**1. Start at a pose.** Create a robot at `Pose2d(-30, -60, 0)` style start
(`Robot(start_x=-30, start_y=-60, start_heading=0)`). Print its pose.

**2. Go to a point (dead reckoning).** Write `go_to_x(robot, target_x)` that uses
`drive_inches` logic to move the robot's `x` to a target. Move from -30 to 0.

**3. Two-segment path.** Drive forward 24", turn to 45°, drive forward 20". Print the
pose after each segment. (You're hand-building what a spline does smoothly.)

**4. A step list.** Represent an autonomous as a Python list of `(name, function)` tuples.
Write `run_sequence(robot, steps)` that runs each function in order and prints
`"[1/4] preload ... done"`. This is your `SequentialAction`.

**5. Recreate BucketSide's shape.** Build a step list named like Juice's:
`preload, spike1, depo1, spike2, depo2, spike3, depo3, park`. Each step can just be a
small move (drive/turn) — the point is the *structure*. Run it with `run_sequence`.

**6. Pose targeting.** Write `drive_to_pose(robot, x, y, heading)` that: turns to face the
target point, drives straight to it (using distance = hypot of dx,dy), then turns to the
final heading. Drive from start to `(-56, -56, 45)` like Juice's preload. Print how close
you got.

**7. Distance-to-pose helper.** Write `distance_to(robot, x, y)` returning the straight-
line distance (`math.hypot`). Use it to confirm exercise 6 ended within a few inches of
the target.

**8. Auto + subsystem.** Combine with Chapter 8: at the "depo" steps, also call a
`lift.run_to_preset(HIGH_BASKET)` and print "scored". Your autonomous now drives AND
operates a mechanism, like the real thing.

**9. Timed autonomous.** Real auto is 30 seconds. Track elapsed sim time and make
`run_sequence` stop early if a 30-second budget runs out, printing which steps didn't
finish. (Robots that run out of time mid-path is a real problem teams plan for.)

**10. Design a full auto.** Pick a simple scoring plan in plain English: e.g. "score
preload in high basket, grab 2 floor samples, score each, park." Express it as a step
list of `drive_to_pose` + subsystem calls, run it in the sim, and print the final pose +
"points scored" tally. Then write (comment) one thing RoadRunner would do better than
your dead-reckoning version and why Juice uses it.

## Java bridge

```java
// Your run_sequence IS Juice's SequentialAction:
Actions.runBlocking(
    new SequentialAction(
        preload,   // each is an Action (a built path or an InstantAction)
        spike1,
        depo1,
        park
    )
);

// drive_to_pose maps to building a path to a Pose2d:
Action toBasket = drive.actionBuilder(drive.pose)
        .splineToLinearHeading(new Pose2d(-56, -56, Math.toRadians(45)), Math.toRadians(200))
        .build();
```

Your dead-reckoning `drive_to_pose` and Juice's `splineToLinearHeading` solve the same
problem — "get the robot to this pose" — yours in straight lines, theirs in smooth curves.
Understanding the goal is what lets you read their code.

➡️ Solutions: [`solutions/09_solution.py`](../solutions/09_solution.py)
