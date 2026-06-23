# Chapter 12 — Field-Centric Driving

> Goal: upgrade your TeleOp so "push the stick forward" always means "drive away from
> the driver" — no matter which way the robot is facing. This is the single most common
> modern upgrade top FTC teams add, and it's pure gyro math you already understand.

## The problem with robot-centric driving

In Chapter 6 you drove **robot-centric**: forward on the stick = toward the robot's
*nose*. That feels great until the robot spins around. Now its nose points back at you, so
"forward" drives it **toward** the driver. Rookie drivers fight this all match.

**Field-centric** (a.k.a. field-oriented) fixes it: forward on the stick = away from the
*driver*, always. The robot figures out "which way is forward for me right now" using the
**gyro/IMU heading** — the exact sensor you mastered in Chapter 4.

## The one idea: rotate the stick vector by −heading

The driver's stick gives a direction in the **field's** frame. The robot drives in **its
own** frame. To translate, you rotate the (x, y) stick vector by the *negative* of the
robot's heading:

```
x_robot = x*cos(-h) - y*sin(-h)
y_robot = x*sin(-h) + y*cos(-h)
```

Then you feed `x_robot, y_robot` into the same `setDrivePower` from Chapter 6. The turn
input `rx` is unchanged (spinning is spinning either way). That's the whole trick.

This is what gm0 and CTRL+ALT+FTC call "field-centric drive," and it's why modern robots
feel so easy to drive. Our sim has it built in:

```python
robot.set_drive_power_field_centric(x, y, rx)   # uses the IMU heading for you
```

## Java bridge (real FTC)

```java
double heading = imu.getRobotYawPitchRollAngles().getYaw(AngleUnit.RADIANS);
// rotate the stick vector by -heading
double rotX = x * Math.cos(-heading) - y * Math.sin(-heading);
double rotY = x * Math.sin(-heading) + y * Math.cos(-heading);
robot.setDrivePower(rotX, rotY, rx);
```

Most teams also add a **"reset heading"** button (driver presses it facing downfield) so
the IMU's zero matches the field. You'll build that too.

---

## Exercises

The sim gives you `robot.set_drive_power_field_centric(x, y, rx)` and, for comparison, the
plain `robot.set_drive_power(x, y, rx)` from Chapter 6. The robot's heading is
`robot.imu.get_heading()`.

**1. Same when facing forward.** With the robot at heading 0, drive `(x=0, y=1)`
field-centric for 1s, then reset and drive the same robot-centric. Show the final pose is
(about) the same — at heading 0 the two are identical.

**2. The spin test.** Turn the robot to heading 90 first (use `run_for` with `rx`). Then
drive `(0, 1)` *robot-centric* for 1s and print the pose. Notice it strafed sideways in
field terms — not what the driver wanted.

**3. Field-centric fixes it.** Same setup: turn to heading 90, then drive `(0, 1)`
*field-centric* for 1s. Show it moves in +y (downfield) like the driver intended, even
though the robot's nose points sideways.

**4. Write the rotation yourself.** Don't call the built-in. Write
`rotate_stick(x, y, heading_deg)` that returns `(x_robot, y_robot)` using the formula
above. Test it: at heading 90, `(0, 1)` should come out close to `(1, 0)` or `(-1, 0)`
(figure out the sign and explain it).

**5. Drive a square, field-centric.** Without ever turning the robot, drive a square:
+y 1s, +x 1s, −y 1s, −x 1s, all field-centric. The robot's heading should stay ~0 the
whole time while it traces a box. (Mecanum + field-centric = strafing a square.)

**6. Heading reset button.** Simulate the driver pressing a "reset heading" button: turn
the robot to 90, then call `robot.imu.reset_heading()`, then drive `(0,1)` field-centric.
After reset, "forward" should follow the robot's *current* nose. Explain in a comment when
a driver would press this.

**7. Compare distance.** For both modes, turn the robot 45° first, then drive `(0,1)` for
1s. Print both final poses side by side and describe the difference in plain English.

**8. Slow + field-centric.** Combine Chapter 6's slow mode (×0.3 on a bumper) with
field-centric driving. Show one second of normal vs slow covers different distance, both
field-centric.

**9. A full field-centric TeleOp.** Write a `run_for` loop with a scripted gamepad that:
reads sticks, drives field-centric, and resets heading when a button is pressed once
(edge-detected, Chapter 6). Print telemetry every 25 loops: heading + pose.

**10. Why not always field-centric?** In a comment, list two situations where a driver
might *prefer* robot-centric (hint: lining up to a wall/board, or if the IMU drifts), and
describe how a team lets the driver toggle between the two modes with one button.

## Java bridge

```java
// in your TeleOp loop:
if (gamepad1.options) {                 // "reset heading" button
    imu.resetYaw();
}
double heading = fieldCentric
    ? imu.getRobotYawPitchRollAngles().getYaw(AngleUnit.RADIANS)
    : 0.0;                              // heading 0 == robot-centric!
double rotX = x * Math.cos(-heading) - y * Math.sin(-heading);
double rotY = x * Math.sin(-heading) + y * Math.cos(-heading);
robot.setDrivePower(rotX, rotY, rx);
```

Notice the elegant trick: **robot-centric is just field-centric with heading forced to 0**.
One code path, one toggle.

➡️ Solutions: [`solutions/12_solution.py`](../solutions/12_solution.py)
