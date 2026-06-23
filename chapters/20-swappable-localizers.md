# Chapter 20 — Swappable Localizers

> Goal: learn the design trick that lets a team change their odometry hardware — dead wheels,
> drive encoders, OTOS, Pinpoint — **without rewriting the rest of the robot**. It's one
> simple idea (a shared interface) that ACME's RoadRunner quickstart is built around, and
> it's your first taste of real software *design*.

## The situation

In Chapter 13 you used `robot.odometry` to get a pose. But there are *many* ways a robot can
know its position:

- **Drive-encoder** localization — cheapest, just uses the drive motors. Drifts when wheels
  slip.
- **Dead wheels** (odometry pods) — unpowered wheels on encoders. Accurate, low drift. (Like
  a goBILDA Pinpoint.)
- **OTOS** — an optical sensor that watches the floor. Easy to mount, a bit jumpy.

A team might start the season on drive encoders, then upgrade to dead wheels. If position
code is sprinkled everywhere, that upgrade means editing dozens of files. There's a better
way.

## The idea: code against an interface, not a device

ACME defines a tiny **`Localizer` interface** — a contract that says "whatever you are, you
must offer `getPose()` and `update()`." Then they write several classes that each *fulfill*
that contract differently: `ThreeDeadWheelLocalizer`, `TwoDeadWheelLocalizer`,
`OTOSLocalizer`, `PinpointLocalizer`. The rest of the robot only ever talks to the
**interface** — it never knows or cares which one is plugged in.

This is the **Strategy pattern**: interchangeable implementations behind one contract. Swap
the strategy, the rest of the code doesn't change.

```python
from ftcsim import Robot, DriveEncoderLocalizer, DeadWheelLocalizer, OTOSLocalizer

def run_with(localizer):              # this code doesn't care which localizer!
    pose = localizer.get_pose()
    print(pose)

robot = Robot()
run_with(DriveEncoderLocalizer(robot))
run_with(DeadWheelLocalizer(robot))   # swapped hardware, SAME run_with()
run_with(OTOSLocalizer(robot))
```

All three offer `get_pose()`. They behave differently (the drive-encoder one drifts more,
the OTOS one is jumpier), but any code written against "a localizer" works with all of them.

## Why this is a big deal

This is the moment the course stops being "make the robot move" and starts being "design
code that survives change." Interfaces let big teams work on subsystems independently and
let you swap hardware mid-season. Once you see it for localizers, you'll spot it everywhere
(drive bases, cameras, grippers).

## Java bridge (ACME's Localizer.java)

```java
public interface Localizer {
    void setPose(Pose2d pose);
    Pose2d getPose();
    PoseVelocity2d update();   // refresh + return current velocity
}

// Many implementations fulfill it; drive code holds a `Localizer localizer;`
// and never knows which concrete class it is:
Localizer localizer = new ThreeDeadWheelLocalizer(hardwareMap, ...);
// later, to switch hardware, change ONLY this line:
// Localizer localizer = new PinpointLocalizer(hardwareMap, ...);
```

---

## Exercises

Use `from ftcsim import Robot, Localizer, DriveEncoderLocalizer, DeadWheelLocalizer,
OTOSLocalizer, run_for`. Each localizer has `get_pose()` returning a `Pose2d`.

**1. Three localizers, one robot.** Make a `Robot`, then create all three localizer types
on it. Print each one's `get_pose()` right away. Confirm all three report (about) the
starting pose.

**2. Code against the interface.** Write `report(localizer)` that just calls
`localizer.get_pose()` and prints it — with **no** mention of which type it is. Call it with
all three. This function is "interface-only" code.

**3. Drive and compare.** Drive the robot forward 2s. Then read all three localizers and
print their poses. They should be close, but not identical — note which drifts most.

**4. Feel the drift.** Read each localizer 20 times *without moving the robot* and print the
first and last reading. Rank the three by how much they wander. In a comment, match each to
its real-world cause (wheel slip / clean pods / optical jitter).

**5. A swappable drive function.** Write `drive_until_x(robot, localizer, target_x)` that
drives forward until `localizer.get_pose().x >= target_x`. Run it with a
`DriveEncoderLocalizer` and again with a `DeadWheelLocalizer` — **same function**, swapped
strategy. Print where each stopped.

**6. Make your own localizer.** Subclass `Localizer` to create `PerfectLocalizer` whose
`get_pose()` returns the robot's true pose with zero drift/noise (use `robot.get_pose()`).
Pass it to your `report()` from exercise 2 — it just works, because it honors the contract.

**7. The contract enforced.** Create a broken "localizer" class that forgets to implement
`get_pose()` (just `pass` the base). Call `get_pose()` on it inside a `try/except` and print
the error. In a comment, explain how the interface tells you *at the point of use* that you
broke the contract.

**8. Strategy at runtime.** Put your three localizers in a dict keyed by name
(`"encoder"`, `"deadwheel"`, `"otos"`). Write code that picks one by a string variable and
uses it — simulating choosing your hardware from a config without changing logic.

**9. Best of both (preview).** Drive forward 2s. The drive-encoder localizer has drifted; a
(hypothetical) perfect one hasn't. Print the gap between them. In a comment, predict how
you'd *combine* a drifting-but-smooth source with an absolute one — this is exactly Chapter
21 (sensor fusion).

**10. Why interfaces win.** In a comment block, describe a concrete mid-season scenario:
your team buys a Pinpoint to replace drive-encoder odometry. With the Localizer interface,
how many files change? Without it (position code copy-pasted everywhere), what's the risk?
This is the design lesson of the chapter.

## Java bridge

```java
// The whole point: drive code depends on the INTERFACE...
public class MecanumDrive {
    public Localizer localizer;   // could be ANY implementation
    public void updatePoseEstimate() { pose = localizer.update(); }
}
// ...so swapping hardware is a one-line change, not a rewrite.
```

➡️ Solutions: [`solutions/20_solution.py`](../solutions/20_solution.py)
