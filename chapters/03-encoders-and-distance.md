# Chapter 3 — Encoders & Distance

> Goal: drive an **exact distance**, not just "for a while." This is the FTC version of
> the very first thing you learned in FLL: *move forward N units*. The tool is the
> **encoder** — a sensor built into the motor that counts how far it has turned.

## What an encoder is

Every FTC motor counts **ticks** as it spins. Juice reads them in `Motor.java`:

```java
public float getEncoderValue() {
    return motor.getCurrentPosition();
}
public void resetEncoder() {
    motor.setMode(DcMotor.RunMode.STOP_AND_RESET_ENCODER);
    motor.setMode(DcMotor.RunMode.RUN_WITHOUT_ENCODER);
}
```

Ticks aren't inches. You convert with a constant. In our sim:

```
TICKS_PER_INCH = 45.0
inches  = ticks / 45.0
ticks   = inches * 45.0
```

On a real robot you *measure* this constant once (drive a known distance, read the
ticks, divide). The number depends on wheel size and gear ratio.

## The core pattern: "drive until far enough"

Driving for a fixed *time* is unreliable — a low battery goes slower. Driving by
*encoder distance* is reliable. The pattern:

```
reset encoder
target_ticks = inches_to_ticks(distance)
while encoder < target_ticks:
    drive forward
stop
```

That `while` loop with a sensor check is one of the most important shapes in all of
robotics. You'll use it for distance now, angles in Chapter 4, and PID in Chapter 7.

## In the sim

```python
from ftcsim import Robot
robot = Robot()
robot.front_left.reset_encoder()
while robot.front_left.get_encoder_value() < 10 * 45:  # 10 inches
    robot.set_drive_power(0, 0.5, 0)
    robot.step(0.02)
robot.set_drive_power(0, 0, 0)   # STOP
print(robot.pose_str())
```

> ⚠️ Always stop at the end. A loop that exits without stopping leaves the robot
> driving into a wall.

---

## Exercises

**1. Read ticks.** Reset `front_left`, drive forward 1s, print the encoder value. How
many inches is that (divide by 45)?

**2. Two conversion functions.** Write `inches_to_ticks(inches)` and
`ticks_to_inches(ticks)`. Test that converting 24 inches → ticks → inches gives back 24.

**3. Drive exactly 24 inches.** Use the while-loop pattern to drive forward until the
encoder shows 24 inches, then stop. Print the final pose — `x` should be near 24.

**4. A reusable `drive_inches`.** Wrap exercise 3 into a function
`drive_inches(robot, inches, power=0.5)`. Drive 12, then 36 inches with it.

**5. Backward by encoder.** Make `drive_inches` handle negative distances: if `inches`
is negative, drive at negative power and loop until the encoder drops below the target.
Test with `-12`.

**6. Why time is worse (experiment).** Drive 24 inches by *time* (guess the seconds at
0.5 power), then by *encoder*. Run each from the same start. Then imagine the battery is
weak: in the sim, lower the power to 0.3 and repeat both. Which method still ends at 24
inches? Explain in a comment.

**7. Square dance.** Make the robot trace a square: drive 24 inches, turn 90°
(`set_drive_power(0,0,0.5)` until `imu.get_heading()` reaches the next corner), repeat 4
times. (Reuse Chapter 4's turn idea early — or just turn by time for now.) Print the
pose after each side.

**8. Average the encoders.** A real robot reads *all four* wheel encoders and averages
them for a better distance estimate (one wheel can slip). Write
`average_distance_inches(robot)` that averages the four encoders and converts to inches.
Drive forward and print it.

**9. Slow down near the target (taste of PID).** Modify `drive_inches` so that when the
robot is within the last 6 inches, it uses lower power (e.g. 0.2) instead of full. Does
it overshoot less? This is the *intuition* behind the "P" in PID you'll build later.

**10. Mission math.** A game element is 30 inches forward and the robot must stop 4
inches short to avoid knocking it. Using only `drive_inches`, write code that ends with
the robot 26 inches forward. Then write (comment) what could still make it inaccurate on
a real field (wheel slip, bumps, battery) — and which sensor from later chapters fixes
heading drift.

## Java bridge

```java
// drive_inches in real FTC style:
public void driveInches(double inches, double power) {
    leftFront.resetEncoder();
    double targetTicks = inches * TICKS_PER_INCH;
    while (opModeIsActive() && leftFront.getEncoderValue() < targetTicks) {
        setDrivePower(0, power, 0);
    }
    setDrivePower(0, 0, 0);
}
```

`while (opModeIsActive() && ...)` is the FTC way to write the loop — it also stops if the
driver presses STOP. The rest is identical to your Python.

➡️ Solutions: [`solutions/03_solution.py`](../solutions/03_solution.py)
