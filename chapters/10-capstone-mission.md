# Chapter 10 — Capstone: Solve a Mission

> Goal: put *everything* together. Given a brand-new mission, break it into a plan and
> code a robot that solves it — in the simulator, in Python, structured exactly the way
> you'd then write it in Java for Juice. This is the chapter that proves you're FTC-ready.

## The skill that actually matters

Each FTC season has a new game, so you can never just memorize last year's code. What
transfers is the **problem-solving loop** every good team runs:

1. **Read the mission.** What scores points? What are the rules/penalties?
2. **List the robot's jobs.** "drive to X", "pick up Y", "place Y at Z", "park".
3. **Map each job to a tool you know.** drive→encoders/gyro, sense→color sensor,
   hold a position→PID, organize→subsystems+state machine, self-drive→sequence of poses.
4. **Build the smallest version that scores**, test it, then improve.
5. **Tune and add cycles** until time runs out.

You now own every tool in step 3. This chapter is practice running the whole loop.

## A made-up mission ("Summer Cup")

So nobody can copy a real solution, here's an invented game. Field is the usual 144"×144".

- Three **fuel cells** sit on the floor at known poses. Each is RED, BLUE, or YELLOW.
- Your alliance is **BLUE**. Scoring:
  - Deliver a **BLUE or YELLOW** cell to the **Depot** at pose `(48, 48)` → **+5** each.
  - Delivering a **RED** cell to the depot → **−3** (penalty) — so you must *detect and
    reject* red.
  - **Park** touching the center line (x within ±4 of 0) at the end → **+10**.
- Autonomous is **30 seconds**.

Your job: write an autonomous that scores as many points as possible without penalties.

---

## Exercises

The solution file gives you a `mission` setup (cell poses/colors) and all your helpers
from earlier chapters. Build up the solution exercise by exercise.

**1. Restate the mission.** In a comment, list every job the robot must do and which
chapter's tool solves it. (No code — this is step 1–3 of the loop.)

**2. Robot scaffold.** Make a robot at start pose `(-36, -60, 90)` and a `score = 0`
counter. Print the starting state.

**3. Visit one cell.** Use `drive_to_pose` to drive to the first cell's pose. Confirm you
arrived (distance < 4 in).

**4. Identify the cell.** At the cell, read the color (the mission tells the sim what
color is there). Decide keep/reject for the BLUE alliance using your Chapter 5
`should_keep` logic. Print the decision.

**5. Deliver or skip.** If the cell should be kept, `drive_to_pose` to the Depot `(48,48)`
and add +5 to score. If it's red, skip it (don't deliver) and print "rejected red". Do
this for the first cell.

**6. Loop all three cells.** Wrap exercises 3–5 in a loop over all three cells. Tally the
score. Print a line per cell (`cell 2 BLUE -> delivered +5`).

**7. Park for points.** After the cells, `drive_to_pose` to a parking spot on the center
line (x≈0). Add +10. Print final score.

**8. Respect the clock.** Add a 30-second budget (like Chapter 9). If delivering all
three cells would blow the budget, skip the farthest one and still park. Print which
cells were skipped and why. (Real strategic decision!)

**9. Full autonomous, as a sequence.** Refactor your whole solution into a step list run
by `run_sequence` (Chapter 9) + subsystem/state usage (Chapter 8) — so it reads like
`BucketSide.java`: a clean ordered list of named actions. Run it end to end.

**10. Reflect + translate.** (a) In a comment, write what you'd change to score more
(faster paths? carry multiple cells?). (b) Pick ONE method from your solution and write
its **Java** version in a comment, using Juice's patterns (`setDrivePower`,
`runToPreset`, `SequentialAction`). This is the Python→Java bridge you'll cross for real
when the season starts.

## You're ready

If you can do exercise 9 — drive to scored poses, sense and decide, manage a state and a
clock, all organized as a clean sequence — you have independently rebuilt the shape of
Juice's real competition code. When the new season's game manual drops, you'll run the
exact same problem-solving loop on the real robot, write it in Python to think it
through, then translate to Java for the team.

## Java bridge (your whole capstone, sketched in Juice's style)

```java
@Autonomous(name = "SummerCup")
public class SummerCup extends LinearOpMode {
    public void runOpMode() {
        Robot robot = new Robot(hardwareMap, true);
        Pose2d start = new Pose2d(-36, -60, Math.toRadians(90));
        waitForStart();

        Actions.runBlocking(new SequentialAction(
            driveTo(cell1), identifyAndDeliver(cell1),
            driveTo(cell2), identifyAndDeliver(cell2),
            driveTo(cell3), identifyAndDeliver(cell3),
            driveTo(parkPose)
        ));
    }
}
```

That's it — the same structure you built in Python, wearing its Java costume.

➡️ Solutions: [`solutions/10_solution.py`](../solutions/10_solution.py)

---

## Where to go next (real resources)

- **Juice's code:** `github.com/Juice-Robotics` — read `IntoTheDeep` now that you can.
- **Learn Java for FTC** (Alan Smith): the free book — do its on-robot exercises next.
- **Game Manual 0** (gm0.org): the community FTC programming guide.
- **CTRL+ALT+FTC** (ctrlaltftc.com): when you want the real PID/odometry math.
- **Official FTC SDK:** `github.com/FIRST-Tech-Challenge/FtcRobotController` — where real
  OpModes live.
