# Chapter 6 — Mecanum TeleOp

> Goal: drive the robot like a human driver does — with a **gamepad**, in a **TeleOp**
> loop, using Juice's *exact* `setDrivePower(x, y, rx)` formula. You'll also learn the
> "button edge detection" trick that `TeleOpMainRed.java` uses on every button.

## Mecanum wheels: drive in any direction

Juice uses **mecanum** wheels — they let the robot go forward/back, **strafe**
sideways, and spin, all at once. Three joystick inputs control everything:

- `x` = strafe (slide left/right)
- `y` = forward/back
- `rx` = rotate (spin)

The magic is mixing those three into four wheel powers. This is the real formula from
`Robot.java` (lines 676–702):

```java
double powerFrontLeft  = y + x + rx;
double powerFrontRight = y - x - rx;
double powerBackLeft   = (y - x + rx) * -1;
double powerBackRight  = (y + x - rx) * -1;
```

Each wheel gets a different **combination** of the three inputs. Then Juice normalizes
(Chapter 2 exercise 10) so no wheel exceeds 1.0. Our sim's `set_drive_power` is a
line-for-line port — you already used it; now you understand it.

## The TeleOp loop

A real TeleOp is one big `while` loop that runs ~50 times a second:

```java
while (opModeIsActive()) {
    double x  = -gamepad1.left_stick_x;
    double y  = -gamepad1.left_stick_y;
    double rx =  gamepad1.right_stick_x;
    robot.setDrivePower(-x, y, rx);
    // ...read buttons, run mechanisms...
    telemetry.update();
}
```

In the sim you supply gamepad inputs through a script (since there's no human). The
`run_for(robot, seconds, loop_fn)` helper *is* your `while` loop.

## Button edge detection (the `oldGamepad` trick)

Look at `TeleOpMainRed.java`:

```java
if (gamepad1.left_bumper && !oldGamepad.left_bumper) { ... }
...
oldGamepad.copy(gamepad1);
```

Why `&& !oldGamepad.left_bumper`? Because the loop runs 50×/sec. If you just checked
`if (left_bumper)`, holding the button for half a second would fire the action **25
times**. The trick: only act when the button is pressed **this loop but was NOT pressed
last loop** — i.e. on the *rising edge*. You'll build this; it's essential.

---

## Exercises

The `Gamepad` in the sim has fields `left_stick_x`, `left_stick_y`, `right_stick_x`,
and booleans like `a`, `left_bumper`. You set them, then drive.

**1. Joystick to motion.** Make a gamepad, set `left_stick_y = -1.0` (sticks are
inverted — up is negative!), and in a `run_for` loop call
`robot.set_drive_power(-gp.left_stick_x, -gp.left_stick_y, gp.right_stick_x)` for 1s.
Confirm the robot drove forward.

**2. Strafe with the stick.** Set `left_stick_x = 1.0` (and y=0, rx=0). Drive 1s. Which
field coordinate changed? (This is strafing.)

**3. Rotate with the stick.** Set `right_stick_x = 0.5`, drive 1s, print heading.

**4. Diagonal.** Set `left_stick_x` and `left_stick_y` both so the robot drives at a 45°
diagonal. Predict, then check the pose.

**5. Wheel-power inspector.** Write `wheel_powers(x, y, rx)` that returns the four
powers using Juice's exact formula. Print the powers for pure forward (0,1,0), pure
strafe (1,0,0), and pure spin (0,0,1). Notice which wheels flip sign.

**6. Edge detector.** Write a class or function that, given the current and previous
button state, returns True only on the rising edge. Simulate a button "held" for 5 loops
and show your detector fires exactly **once**.

**7. Button does a thing.** In a TeleOp loop, when `gamepad.a` goes from False→True,
toggle a `mode` variable between `"SAMPLE"` and `"SPECIMEN"` (like Juice's
`toggleGamepiece`). Script the gamepad so `a` is pressed on loops 10 and 30, and print
`mode` each time it changes. It should toggle twice, not 20 times.

**8. Full driver sim.** Combine: drive forward for the first second (stick), then strafe
right for the next second, then spin for the last second — all in one `run_for`. Use the
elapsed time `t` that `loop_fn` receives to decide which phase you're in. Print the pose
at the end.

**9. Slow mode.** Real drivers hold a bumper for precision ("slow mode"). When
`gamepad.right_bumper` is held, multiply all drive inputs by 0.3. Show the robot covers
less distance in 1s with slow mode on vs off.

**10. Mini TeleOp like Juice.** Write a loop that: reads the sticks for driving, uses
edge detection so `a` toggles scoring mode and `b` "ejects" (just print "EJECT"), and
every loop prints a 3-line telemetry (`MODE`, `pose`, `loop count`) in the style of
`TeleOpMainRed`. Run it for 2 seconds with a scripted gamepad. This is a real TeleOp in
miniature.

## Java bridge

```java
// Exercise 6/7 -- edge detection is THE TeleOp pattern:
Gamepad oldGamepad = new Gamepad();
while (opModeIsActive()) {
    if (gamepad1.a && !oldGamepad.a) {      // rising edge only
        mode = (mode == SAMPLE) ? SPECIMEN : SAMPLE;
    }
    double x  = -gamepad1.left_stick_x;
    double y  = -gamepad1.left_stick_y;
    double rx =  gamepad1.right_stick_x;
    robot.setDrivePower(-x, y, rx);
    oldGamepad.copy(gamepad1);              // remember for next loop
    telemetry.update();
}
```

This is essentially `TeleOpMainRed.java` with the mechanism buttons removed. You now
understand that whole file.

➡️ Solutions: [`solutions/06_solution.py`](../solutions/06_solution.py)
