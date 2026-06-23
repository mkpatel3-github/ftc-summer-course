# Juice Robotics (FTC #16236) — Summer Programming Course

A daily, do-it-yourself summer course that takes a 7th–9th grader who knows *a little*
Python and turns them into someone ready to read, write, and understand the real
robot code that team **Juice (#16236)** runs.

It is built from two things:

1. **Juice's own GitHub code** — the real robot from the 2024–25 *Into the Deep* season
   ([`Juice-Robotics/IntoTheDeep`](https://github.com/Juice-Robotics/IntoTheDeep)) plus
   older seasons. We teach the *exact* patterns the team uses: `Motor`, `StepperServo`,
   `setDrivePower`, `PIDFController`, the `Levels` state machine, RoadRunner autonomous,
   the gamepad action queue.
2. **The free open-source book *Learn Java for FTC* by Alan Smith**
   ([repo](https://github.com/alan412/LearnJavaForFTC)) and the community guide
   **Game Manual 0** ([gm0.org](https://gm0.org)). We follow their concept order.

> 📚 All source links (the team's files we reference, the books, the FTC SDK) are in
> **[`REFERENCES.md`](REFERENCES.md)**. Those repos are **not** bundled here — open them
> on GitHub, or clone them locally if you want to read along.

## The big idea: think in Python, ship in Java

You already know a little Python. FTC robots run **Java**. Instead of fighting Java
syntax on day one, every exercise asks you to:

1. **Solve the problem in Python first** using our tiny robot simulator (`sim/ftcsim.py`).
   No robot required — it runs on any laptop.
2. **Then translate the same idea to Java** using the "Java bridge" box in each chapter.

The simulator deliberately uses the **same method names as Juice's real Java code**
(`set_speed`/`setSpeed`, `getEncoderValue`, `setDrivePower`, `PIDFController`, `IMU`,
`telemetry.addData`). So when you switch to Java, it will feel like you already wrote it.

> 🔁 **Chapter 11** is a whole chapter on doing that switch, and
> **[`PYTHON-TO-JAVA.md`](PYTHON-TO-JAVA.md)** is a one-page cheat sheet you can keep open
> while you convert any exercise to real FTC Java.

## What you'll be able to do by season start

The same core skills your team builds every mission on — the FTC versions of the
FLL things you already did (gyro-straight, line following, using sensors):

- Drive a mecanum robot by power, and drive an **exact distance** with encoders.
- **Turn to an angle** and **drive perfectly straight** using the gyro/IMU (with PID).
- Follow a line and **detect game-piece color** with a color sensor.
- Drive a robot with a **gamepad** in TeleOp using Juice's real drive formula.
- Build a **PID controller** from scratch and use it to move a lift to a height.
- Organize a robot with **subsystems** and a **state machine** (Juice's `Levels`).
- Write an **autonomous** routine that sequences actions to score points.
- Take any new mission and break it into a plan you can code.

And the modern skills today's top teams (and Juice) actually run:

- **Convert your Python to real FTC Java** confidently, line by line.
- Drive **field-centric** so "forward" always means "away from the driver."
- Track a live **odometry pose** and drive to an **exact field position**.
- Use a camera + **AprilTags** to localize, and find game pieces by color.
- Organize a robot with **command-based programming** (Juice's `commands/`).
- Write **pose-based autonomous** the RoadRunner 1.0 / Pedro Pathing way.

## How to use this course (daily plan)

> **Students: read [`STUDENT-START-HERE.md`](STUDENT-START-HERE.md) first** — it walks you
> through installing Python and running your first exercise, step by step.

- **16 chapters, 10 exercises each = 160 exercises.** Do ~1 exercise per weekday.
  That's about 14 weeks of weekdays — a full summer, finishing before kickoff.
  Chapters 1–10 are the core; **11–16 are the modern upgrades** (Java conversion,
  field-centric driving, odometry, vision/AprilTags, command-based code, pose-based
  autonomous) that today's top teams — including Juice — actually run.
- Each chapter has: a **lesson** (`chapters/NN-name.md`), a **starter file you edit**
  (`chapters/NN_starter.py`), and an **answer key** (`solutions/NN_solution.py`).
  The starter files are generated from the lessons by `tools/make_starters.py`.
- **Rule:** try every exercise yourself first. Only open the solution after a real
  attempt. The whole point is *problem solving*, not copying.

### Setup (one time)

You only need Python 3 (no extra installs). Test it:

```bash
cd ftc-summer-course/sim
python ftcsim.py
# should print: After driving forward 2s: x=  72.0  y=   0.0  heading=   0.0
```

To run an exercise file, from the `ftc-summer-course` folder:

```bash
python chapters/02_starter.py
```

(Each starter file already knows how to find the simulator.)

## Chapter map

| #  | Chapter | Core concept | FLL/Juice connection |
|----|---------|--------------|----------------------|
| 1  | [Hello, Robot](chapters/01-hello-robot.md) | Python→Java thinking, telemetry, variables, types | The Driver Station screen |
| 2  | [Motors & Power](chapters/02-motors-and-power.md) | Motors, power −1..1, clamping, reverse | `Motor.java`, `setSpeed` |
| 3  | [Encoders & Distance](chapters/03-encoders-and-distance.md) | Encoders, ticks↔inches, drive exact distance | "Move forward N inches" |
| 4  | [The Gyro (IMU)](chapters/04-the-gyro-imu.md) | Heading, turn-to-angle, **gyro-straight** | The FLL gyro, but FTC |
| 5  | [Sensors & Line Following](chapters/05-sensors-and-line-following.md) | Color/distance sensors, line following, sample color | `Claw.detectSample()` |
| 6  | [Mecanum TeleOp](chapters/06-mecanum-teleop.md) | `setDrivePower(x,y,rx)`, gamepad, edge detection | `Robot.java`, `TeleOpMainRed` |
| 7  | [PID Control](chapters/07-pid-control.md) | Build a `PIDFController`, tune P/I/D/F | `PIDFController.java`, `Lift.java` |
| 8  | [Subsystems & State Machines](chapters/08-subsystems-and-state-machines.md) | Classes, encapsulation, the `Levels` enum, presets | Juice subsystem architecture |
| 9  | [Autonomous](chapters/09-autonomous.md) | Sequencing actions, dead reckoning, poses & paths | `BucketSide.java`, RoadRunner |
| 10 | [Capstone: Solve a Mission](chapters/10-capstone-mission.md) | Put it all together; a mission-solving method | A real season game |
| 11 | [Crossing to Java](chapters/11-crossing-to-java.md) | Convert your Python to real FTC Java, line by line | Every file Juice runs |
| 12 | [Field-Centric Driving](chapters/12-field-centric-driving.md) | Drive relative to the field using the IMU heading | Modern TeleOp upgrade |
| 13 | [Odometry & Pose](chapters/13-odometry-and-pose.md) | Always know your `(x, y, heading)`; Pinpoint/OTOS | `KalmanDrive.java` |
| 14 | [Vision & AprilTags](chapters/14-vision-and-apriltags.md) | Localize off field tags; find samples by color | `CVMaster.java`, Limelight |
| 15 | [Command-Based Programming](chapters/15-command-based-programming.md) | Compose behavior as Commands + a scheduler | Juice `commands/` folder |
| 16 | [Modern Autonomous: Paths](chapters/16-modern-autonomous-paths.md) | Drive to poses; RoadRunner 1.0 Actions / Pedro | `BucketSide.java` |

## A note to mentors / parents

Exercises are graded in difficulty inside each chapter (1–2 warm-up, 3–7 core,
8–10 stretch). A student who finishes through **Chapter 8** is genuinely TeleOp-ready;
**Chapters 9–10** (autonomous, poses, RoadRunner) complete the core. **Chapters 11–16**
are the modern-FTC upgrades — Python→Java conversion, field-centric driving, odometry,
vision/AprilTags, command-based programming, and pose-based autonomous — the things the
FLL-to-FTC jump doesn't cover but that every competitive team now uses. They're grounded
in Juice's real advanced files (`KalmanDrive.java`, `CVMaster.java`, the `commands/`
folder, `BucketSide.java`). The trig shows up in Chapters 7, 9, 12, and 13 — pair younger
students there. Everything runs offline in the simulator, so no Control Hub or robot is
needed until the team reconvenes. A student who only reaches Chapter 11 is already
season-ready; 12–16 make them *competitive*.

## Credits & source material

This course teaches *real* open-source work created by other people. The simulator and
exercises here are original, but the **concepts, code patterns, and book content are
theirs.** Full thanks and credit to:

- **Team Juice — FTC #16236** (Folsom, CA) — the robot code this entire course is built
  around. Lessons quote and explain their actual files (`Robot.java`, `PIDFController.java`,
  `Lift.java`, `Claw.java`, `TeleOpMainRed.java`, `BucketSide.java`, and the `Levels` state
  machine). Principal authors: **Siddharth Ray** (lead software, [@kidsonfilms-python-rules](https://github.com/kidsonfilms-python-rules))
  and **Hunter Tsai** (captain, [@huntertsai1](https://github.com/huntertsai1)).
  - Code: https://github.com/Juice-Robotics · Team: https://juicerobotics.org
- **Alan Smith** — author of the free book ***Learn Java for FTC***, whose beginner
  concept order shapes this course. https://github.com/alan412/LearnJavaForFTC
- **Game Manual 0 (gm0) contributors** — the community FTC guide. https://gm0.org ·
  https://github.com/gamemanual0/gm0
- **CTRL+ALT+FTC** — open-source FTC controls/PID/odometry guide. https://www.ctrlaltftc.com
- **ACME Robotics** — *RoadRunner*, the motion library Juice uses for autonomous.
  https://github.com/acmerobotics/road-runner
- **FIRST® Tech Challenge** — the official FTC SDK and sample OpModes.
  https://github.com/FIRST-Tech-Challenge/FtcRobotController

Those repositories are **not** copied into this project — we link to them so you read the
originals. A complete, file-by-file map of what each lesson references is in
**[`REFERENCES.md`](REFERENCES.md)**. All trademarks and code belong to their respective
owners; this course is an independent, educational companion and is not officially
affiliated with or endorsed by the above projects.

— Built for Juice Robotics #16236 · Folsom, CA · https://juicerobotics.org
