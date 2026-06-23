# Chapter 17 — Robot Architecture: One Home for Hardware

> Goal: stop scattering motor and servo setup all over your code. Learn the **hardware
> singleton** + **constants file** pattern that every top team uses (Seattle Solvers'
> `Robot.java` + `Globals.java`, KookyBotz's `RobotHardware.java`). This is the
> organization that keeps a complex robot from turning into spaghetti.

## The problem: hardware everywhere

Up to now each exercise made its own `Robot()` and poked at motors directly. On a real
robot with 4 drive motors, 2 lift motors, 5 servos, and 4 sensors, if every OpMode fetches
and configures all of that, you get:

- the same setup copy-pasted into TeleOp **and** every autonomous,
- a motor reversed in one file but not another (a brutal bug to find),
- "magic numbers" (servo positions, lift heights) sprinkled across dozens of files.

## Pattern 1: the hardware singleton

Top teams make **one** object that owns all the hardware, created once, shared everywhere.
Seattle Solvers call it `Robot.getInstance()`; KookyBotz call it `RobotHardware`. Every
subsystem and OpMode asks that one object for its motors. One place to configure, one place
to fix.

In Python a clean way to get "one shared instance" is a class method that caches it:

```python
class RobotHardware:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = RobotHardware()
        return cls._instance
```

Now `RobotHardware.get_instance()` always returns the *same* robot, no matter who asks.

## Pattern 2: the Globals constants file

Every tunable number lives in **one** file. Seattle Solvers' `Globals.java` holds slide
heights, servo positions, thresholds, and enums like `AllianceColor` and `RobotState`.
Nothing in the rest of the code is a bare number — it's a *named* constant:

```python
class Globals:
    LIFT_GROUND = 0
    LIFT_LOW = 800
    LIFT_HIGH = 1600
    CLAW_OPEN = 0.6
    CLAW_CLOSED = 0.2
    ALLIANCE = "RED"
```

Why this matters: when the lift gear ratio changes, you edit **one line**, not fifteen. And
`Globals.LIFT_HIGH` tells a reader what the number *means* — `1600` does not.

## Java bridge (Seattle Solvers' real pattern)

```java
public class Robot {
    private static Robot instance = null;
    public DcMotorEx leftFront, rightFront, leftBack, rightBack;

    public static Robot getInstance() {
        if (instance == null) instance = new Robot();
        return instance;
    }
    public void init(HardwareMap hardwareMap) {
        leftFront = hardwareMap.get(DcMotorEx.class, "leftFront");
        // ... all hardware, configured ONCE, right here ...
    }
}
```

```java
public class Globals {           // every magic number, named, in one file
    public static int LIFT_HIGH = 1600;
    public static double CLAW_OPEN = 0.6;
    public enum AllianceColor { RED, BLUE }
}
```

---

## Exercises

You'll build a small architecture and then use it. You can keep everything in one Python
file. The sim's `Robot` is your "hardware" — wrap it.

**1. A singleton.** Write a `RobotHardware` class with a `get_instance()` classmethod that
caches and returns one shared instance. Call it twice, store both, and prove they are the
**same object** (`a is b` is True).

**2. Own the hardware.** Give `RobotHardware` an `__init__` that creates a sim `Robot()`
and stores it as `self.robot`. Add a `drive(x, y, rx)` method that forwards to
`self.robot.set_drive_power(...)`. Drive forward 1s through the singleton; print the pose.

**3. A Globals file.** Make a `Globals` class with named constants: `LIFT_GROUND=0`,
`LIFT_LOW=800`, `LIFT_HIGH=1600`, `CLAW_OPEN=0.6`, `CLAW_CLOSED=0.2`. Print all five.

**4. Use the names, not the numbers.** Write a function `lift_preset(name)` that takes
`"GROUND"`, `"LOW"`, or `"HIGH"` and returns the matching `Globals` constant. Show that
changing `Globals.LIFT_HIGH` to a new value changes the result **without touching
`lift_preset`**. (This is the payoff of the pattern.)

**5. Enums in Globals.** Add an `ALLIANCE` constant and a helper `scoring_x()` that returns
a +x target for RED and a −x target for BLUE. Flip `Globals.ALLIANCE` and show the target
mirrors — one constant changes the whole robot's autonomous side.

**6. No more copy-paste.** Write two "OpModes" as functions — `teleop()` and `auton()` —
that **both** get the robot from `RobotHardware.get_instance()`. Show they share the same
hardware object (drive in one, read the pose in the other).

**7. Reverse once.** Add a `reverse_left_side()` method on `RobotHardware` that flips the
left motors' `reverse` flag. In a comment, explain why doing this in the singleton (instead
of in each OpMode) prevents the classic "works in TeleOp, broken in auto" bug.

**8. A subsystem reads from the singleton.** Write a `Lift` class whose constructor takes
the `RobotHardware` instance and uses `Globals` presets in a `go_to(name)` method. Notice
the `Lift` never touches `hardwareMap`/`Robot` directly — it goes through the singleton.

**9. Telemetry data class.** Solvers keep a `TelemetryData` holder. Make a small class that
stores the robot's `mode`, `alliance`, and `pose`, with a `show(telemetry)` method that
prints them. Use it from your `teleop()` function.

**10. Refactor a mess.** Below (write it first) is a "bad" version: a function that calls
`Robot()` itself and uses bare numbers `0.6`, `1600`. Refactor it to use
`RobotHardware.get_instance()` and `Globals`. In a comment, list every benefit you gained.

## Java bridge

```java
// In every OpMode -- TeleOp AND every Auto -- the SAME two lines:
Robot robot = Robot.getInstance();
robot.init(hardwareMap);
// ...then use robot.leftFront, Globals.LIFT_HIGH, etc. Configure once, use everywhere.
```

You've now built the backbone of a real competitive codebase. Open Seattle Solvers'
`hardware/Robot.java` and `hardware/Globals.java` — it's exactly this, scaled up.

➡️ Solutions: [`solutions/17_solution.py`](../solutions/17_solution.py)
