# Chapter 11 — Crossing to Java

> Goal: take the Python you've written all summer and turn it into the **real Java**
> that runs on Juice's Control Hub. Every chapter had a "Java bridge" box; this chapter
> makes the bridge a skill you can do on your own, line by line.

You already solved every hard problem — driving, PID, state machines, autonomous. The
*ideas* are done. What's left is **syntax**: the punctuation and rules Java wants that
Python doesn't. This is the easy part, but it's where beginners trip, so we drill it.

> 📄 Keep [`PYTHON-TO-JAVA.md`](../PYTHON-TO-JAVA.md) open beside you — it's the cheat
> sheet for everything below.

## The five differences that matter most

**1. Types.** Python figures out what a variable is. Java makes you say it up front.

```python
power = 0.75          # Python
```
```java
double power = 0.75;  // Java: "double" = a decimal number
```

Common Java types: `int` (whole number), `double` (decimal), `boolean` (true/false),
`String` (text). For a motor you'll see `DcMotor`, for the gyro `IMU`.

**2. Semicolons.** Every Java statement ends with `;`. Forgetting it is the #1 first error.

**3. Braces, not indentation.** Python uses spaces to group code. Java uses `{ }`.

```python
if x > 0:
    print("positive")
```
```java
if (x > 0) {
    System.out.println("positive");
}
```

Notice Java also puts the `if` condition in `( )`.

**4. camelCase.** Python likes `set_drive_power`. Java (and Juice) like `setDrivePower`.
Same name, different costume. Our simulator gave you *both* spellings all summer for this
exact moment.

**5. The OpMode wrapper.** A Python script just runs top-to-bottom. A real FTC program is
a **class** the robot controller calls. Your `loop` body goes inside
`while (opModeIsActive())`:

```java
@TeleOp(name = "My TeleOp")
public class MyTeleOp extends LinearOpMode {
    @Override
    public void runOpMode() {
        Robot robot = new Robot(hardwareMap);   // get the real motors
        waitForStart();                          // wait for the START button
        while (opModeIsActive()) {
            // ... your loop body goes here ...
        }
    }
}
```

`hardwareMap` is how the real robot hands you the motors you configured on the Driver
Station. In the sim you wrote `robot = Robot()`; on the robot it's
`robot = new Robot(hardwareMap)`.

## How to convert any function, in 4 steps

1. **Add types** to every variable and to the function signature.
2. **Add `;`** to the end of every statement.
3. **Replace `:` + indentation** with `{ }`.
4. **Rename** `snake_case` → `camelCase` and `print(...)` → `telemetry.addData(...)`.

That's it. The logic — the part that was actually hard — does not change.

---

## Exercises

For each one, write the Java in a **comment** (you can't run Java here — that's fine; the
goal is reading and writing it correctly). Check yourself against the solution.

**1. Type tags.** Convert these three Python lines to Java, with the right type and a
semicolon each: `wheels = 4`, `power = 0.6`, `name = "Juice"`.

**2. An if/else.** Convert this to Java (braces and parentheses):
`if speed > 1.0:` / `speed = 1.0` / `else:` / `speed = speed`. (This is clamping.)

**3. A for loop.** Python `for i in range(4):` printing `i`. Write the Java
`for (int i = 0; i < 4; i++) { ... }` version that does the same.

**4. A method signature.** Convert `def clamp(power):` that returns a clamped value into a
Java method header: `double clamp(double power) { ... }`. Write the whole method.

**5. The drive formula.** Take `wheel_powers(x, y, rx)` from Chapter 6 and write it in
Java: four `double` variables using Juice's exact formula, ending in semicolons.

**6. snake → camel.** Rename each to Java style: `set_drive_power`, `get_encoder_value`,
`reset_heading`, `left_stick_y`, `is_red_alliance`. (One of these stays the same in FTC —
which, and why? Hint: gamepad fields.)

**7. A telemetry block.** Convert a 3-line Python telemetry print (MODE, pose, loop) into
Java `telemetry.addData(...)` calls followed by `telemetry.update();`.

**8. Wrap a loop in an OpMode.** Take your Chapter 6 mini-TeleOp loop body and write the
full `runOpMode()` skeleton around it (class header, `waitForStart()`, the `while
(opModeIsActive())` loop). The loop body can stay as a `// ...` comment.

**9. A whole subsystem.** Convert your Chapter 8 `Lift` class (constructor + `set_target`
+ `update`) into a Java class sketch: `public class Lift { ... }` with typed fields and
methods. Logic in comments is fine; get the *shape* right.

**10. Spot the bugs.** Here is Java with **four** beginner mistakes. In a comment, list
each bug and the fix:
```java
public void drive(double x double y) {
    double power = x + y
    if power > 1 {
        power = 1;
    }
    telemetry.addData("power", power)
}
```

## Java bridge

This whole chapter *is* the Java bridge. Once you can do these ten, open Juice's real
`TeleOpMainRed.java` and `Lift.java` — you'll find they're just the Java versions of
things you already wrote. The mystery is gone.

➡️ Solutions: [`solutions/11_solution.py`](../solutions/11_solution.py)
