# Chapter 4 — The Gyro (IMU)

> Goal: the FTC version of the thing you loved in FLL — **gyro turns** and
> **gyro-straight driving**. The sensor is the **IMU** (Inertial Measurement Unit), a
> chip on the Control Hub that always knows which way the robot is pointing.

## Heading: the robot's compass

The IMU reports **heading** in degrees. We normalize it to the range −180 to +180:
- `0°` = pointing the way it started
- `+90°` = turned left a quarter turn
- `-90°` = turned right a quarter turn
- `180°` / `-180°` = backwards

Our sim's IMU matches the real FTC IMU idea:

```python
robot.imu.get_heading()    # current heading in degrees
robot.imu.reset_heading()  # call this at the start, "this is now 0"
```

## Problem 1: Turn to an exact angle

Same loop shape as encoders, but the sensor is heading instead of ticks:

```
while heading is not close enough to target:
    turn toward target
stop
```

The trick is **which way to turn**. If you want +90 and you're at 0, turn left
(`rx > 0`). If you're already at +100, you overshot — turn right (`rx < 0`). The clean
way: compute `error = target - heading`, turn in the *sign* of the error.

## Problem 2: Drive straight (gyro-straight)

A robot never drives perfectly straight — one side is always a hair stronger, so it
drifts. The fix is the heart of FLL/FTC autonomous: **measure heading error and correct
it while driving.**

```
target_heading = 0
while not far enough:
    error = target_heading - current_heading
    correction = error * small_gain      # e.g. 0.02
    set_drive_power(x=0, y=forward, rx=correction)
```

If the robot drifts right (heading goes negative), `error` becomes positive, `rx`
nudges it back left. This tiny `error * gain` idea is **proportional control** — the "P"
of the PID you'll formalize in Chapter 7.

## Angle wrap: the classic bug

Turning from +170° to −170° is only **20 degrees**, not 340. Juice handles this with a
`norm`/normalize function (see `PIDFController.norm` and `Robot.normalizeRadians`). You
must subtract angles *the smart way* so the robot turns the short direction.

---

## Exercises

**1. Read heading.** Reset heading, spin at `rx=0.4` for 0.5s, print the heading.

**2. Angle difference (naive).** Write `angle_error(target, current) = target - current`.
Test `angle_error(90, 0)` → 90. Then test `angle_error(-170, 170)` → −340. Note in a
comment why −340 is "wrong" for a robot (it would spin almost all the way around).

**3. Angle difference (smart).** Write `angle_wrap(error)` that maps any angle into
−180..180 (hint: `((error + 180) % 360) - 180`). Now `angle_wrap(angle_error(-170, 170))`
should give +20. Test several values.

**4. Turn to angle.** Write `turn_to(robot, target_deg)` using the loop pattern: while
the (wrapped) error is bigger than ~2°, turn in the sign of the error; then stop. Turn to
+90, print heading. Turn to −45, print heading.

**5. Turn both directions.** From heading 0, `turn_to(+90)`, then `turn_to(-90)`,
printing after each. Confirm it goes left then right (not the long way around).

**6. Proportional turn (smoother).** Improve `turn_to` so the turn power is
`error * gain` (try gain = 0.02), clamped to ±0.5. It should slow down as it approaches
the target instead of slamming on. Compare overshoot to exercise 4.

**7. Gyro-straight.** Write `drive_straight(robot, inches, power=0.5)` that drives
forward by *encoder distance* (Chapter 3) **and** corrects heading toward 0 each loop
using `rx = angle_wrap(0 - heading) * 0.03`. Drive 36 inches and print the final heading
(should stay near 0).

**8. Push test.** Our sim drives perfectly straight, so simulate a "push": inside the
loop, every 25 steps add a small heading disturbance with
`robot.heading += 5`. Run `drive_straight` with the correction ON, then with it OFF
(`rx=0`). Compare final headings. This is exactly why gyro-straight matters.

**9. Drive straight on a heading.** Generalize `drive_straight` to take a
`target_heading` argument so the robot can drive straight while *facing* +30°. Drive 24
inches on heading +30 and confirm it holds +30.

**10. Combine: an L-path.** Drive straight 24 inches on heading 0, `turn_to(90)`, then
drive straight 24 inches on heading 90. Print the pose. You just did encoder distance +
gyro turn + gyro-straight together — the backbone of a real autonomous.

## Java bridge

```java
// turn_to, real FTC style (IMU returns radians/degrees via getRobotYawPitchRollAngles)
public void turnTo(double targetDeg, double gain) {
    double error = angleWrap(targetDeg - getHeadingDeg());
    while (opModeIsActive() && Math.abs(error) > 2) {
        double power = Range.clip(error * gain, -0.5, 0.5);
        setDrivePower(0, 0, power);
        error = angleWrap(targetDeg - getHeadingDeg());
    }
    setDrivePower(0, 0, 0);
}

double angleWrap(double deg) {
    return ((deg + 180) % 360 + 360) % 360 - 180; // safe modulo
}
```

`error * gain` here is the same proportional idea you'll see as `kp * error` in
`PIDFController.java` (Chapter 7). You're already doing PID — just the "P" part.

➡️ Solutions: [`solutions/04_solution.py`](../solutions/04_solution.py)
