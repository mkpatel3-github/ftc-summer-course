# Python → Java Quick Reference

You wrote the ideas in Python. The robot runs Java. This page is the translation cheat
sheet. Keep it open while you do Chapter 11 — and when you write your first real OpMode.

## The 60-second summary

| Python | Java | Note |
|--------|------|------|
| `x = 5` | `int x = 5;` | say the type, end with `;` |
| `x = 0.5` | `double x = 0.5;` | decimals are `double` |
| `name = "Juice"` | `String name = "Juice";` | capital `S` |
| `ok = True` | `boolean ok = true;` | lowercase `true`/`false` |
| `if x > 0:` | `if (x > 0) {` | condition in `( )`, body in `{ }` |
| (indent) | `}` | close the block with a brace |
| `elif:` | `} else if (...) {` | |
| `else:` | `} else {` | |
| `for i in range(4):` | `for (int i = 0; i < 4; i++) {` | |
| `while running:` | `while (running) {` | |
| `def f(a, b):` | `returnType f(typeA a, typeB b) {` | types on every parameter |
| `return x` | `return x;` | |
| `# comment` | `// comment` | |
| `print(x)` | `telemetry.addData("x", x);` | then `telemetry.update();` |
| `and` / `or` / `not` | `&&` / `\|\|` / `!` | |
| `x ** 2` | `Math.pow(x, 2)` | |
| `abs(x)` | `Math.abs(x)` | |
| `math.sin(x)` | `Math.sin(x)` | Java radians, same as Python |
| `set_drive_power` | `setDrivePower` | snake_case → camelCase |

## Types you'll actually use

| Type | Holds | Example |
|------|-------|---------|
| `int` | whole number | `int ticks = 1800;` |
| `double` | decimal | `double power = 0.75;` |
| `boolean` | true/false | `boolean isRed = true;` |
| `String` | text | `String mode = "SAMPLE";` |
| `DcMotorEx` | a motor | from `hardwareMap` |
| `IMU` | the gyro | from `hardwareMap` |
| `Pose2d` | x, y, heading | RoadRunner / autonomous |

> **Integer division gotcha** (Chapter 1): in Java `(1800 + 1810) / 2` using `int` gives
> `1805`, but `7 / 2` gives `3`, not `3.5` — integer math throws away the remainder. Use a
> `double` if you want decimals: `(double)(a + b) / 2`.

## The shape of a real program (OpMode)

A Python script runs top to bottom. A real FTC program is a **class** the robot calls:

```java
@TeleOp(name = "My TeleOp")                // shows up on the Driver Station
public class MyTeleOp extends LinearOpMode {
    @Override
    public void runOpMode() {
        // 1. get hardware (replaces "robot = Robot()")
        Robot robot = new Robot(hardwareMap);

        // 2. wait for the human to press START
        waitForStart();

        // 3. your loop (this is run_for / the loop_fn body)
        while (opModeIsActive()) {
            double y  = -gamepad1.left_stick_y;
            double x  =  gamepad1.left_stick_x;
            double rx =  gamepad1.right_stick_x;
            robot.setDrivePower(x, y, rx);
            telemetry.addData("pose", robot.getPose());
            telemetry.update();
        }
    }
}
```

For **autonomous**, swap `@TeleOp` for `@Autonomous` and instead of a `while` loop you
usually run a sequence of actions once (Chapters 9, 16).

## `hardwareMap`: where the real motors come from

In the sim: `self.front_left = Motor(0, "leftFront")`.
On the robot the names come from the Driver Station config, and you fetch them:

```java
DcMotorEx frontLeft = hardwareMap.get(DcMotorEx.class, "leftFront");
```

The string `"leftFront"` must **exactly match** the name you typed in the robot config.
Wrong name = the classic "the robot does nothing and there's no error" bug.

## Things Python does that Java can't (and the fix)

| You wrote (Python) | Java needs |
|--------------------|------------|
| `nonlocal mode` (a closure) | make it a **field** of the class |
| a `lambda` for `run_for` | the **body of the `while` loop** |
| dynamic types (`x` is anything) | pick ONE type and keep it |
| `list` that grows freely | `ArrayList<Type>` or an array |
| f-string `f"x={x}"` | `"x=" + x` or `String.format(...)` |

## Don't forget

- **Every statement ends in `;`** — this is the most common first mistake.
- **Match every `{` with a `}`** — your editor highlights the pair; use it.
- **camelCase** for methods and variables, **CapitalCase** for class names.
- Gamepad fields like `left_stick_y` keep their snake_case in FTC — that's the SDK's
  spelling, not yours. Everything *you* name is camelCase.
- The logic you debugged in Python is correct. Converting is mechanical. If the Java
  "doesn't work," it's almost always a type, a brace, or a hardware name — not your idea.
