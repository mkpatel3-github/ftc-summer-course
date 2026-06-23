# Chapter 2 — Motors & Power

> Goal: make wheels spin. Understand motor **power** as a number from −1.0 to +1.0,
> why we **clamp** it, what **reverse** means, and how Juice's `setDrivePower` shares
> one power value across four wheels.

## The real code

Juice's `Motor.java` is tiny — read it:

```java
public void setSpeed(float speed) {
    this.speed = speed;
    motor.setPower(speed);
}
```

A motor's power is just a number:
- `1.0` = full speed forward
- `0.0` = stop
- `-1.0` = full speed backward
- `0.5` = half speed forward

If you give it `2.0`, the real motor can't go to 200% — it just does its max. Good code
**clamps** the value into −1..1 so the math elsewhere stays sane. Our sim's `Motor.set_speed`
clamps for you (look at `sim/ftcsim.py`), exactly like a real motor controller.

### Reverse

Two motors on opposite sides of a robot face *opposite* directions. To make the robot
go straight, one side must be **reversed**. Juice does this in the `Motor` constructor:

```java
if (reverse) { motor.setDirection(DcMotor.Direction.REVERSE); }
```

In the sim: `Motor(port, name, reverse=True)`.

### One number, four wheels (a peek ahead)

In `Robot.java`, driving forward sends the *same* `y` value to all wheels; turning sends
`rx` with **opposite signs** left vs. right. You'll build the full formula in Chapter 6.
For now, just feel how power numbers combine.

## Using motors in the sim

```python
from ftcsim import Robot
robot = Robot()
robot.front_left.set_speed(0.5)   # spin one wheel at half power
robot.step(0.02)                  # advance physics 0.02s
print(robot.front_left.get_encoder_value())
```

To actually move the *whole robot* a known amount, use `set_drive_power(x, y, rx)` and
`run_for` (a helper that loops `step` for you):

```python
from ftcsim import Robot, run_for
robot = Robot()
run_for(robot, 2.0, lambda t: robot.set_drive_power(0, 1.0, 0))  # forward 2s
print(robot.pose_str())
```

---

## Exercises

**1. Spin one wheel.** Set `front_left` to power `0.5`, step the sim 50 times, and print
the wheel's encoder value. (Just see a number grow.)

**2. Clamp it.** Set a wheel to power `2.0`. Print `robot.front_left.speed`. What number
did it actually store? Explain in a comment why it's not `2.0`.

**3. Forward and back.** Drive the robot forward at full power for 1 second, print the
pose, then backward for 1 second, and print again. Did `x` (or `y`) return near start?
(Use `set_drive_power(0, 1.0, 0)` then `(0, -1.0, 0)`.)

**4. Half vs full.** Drive forward at `0.5` for 2s and at `1.0` for 1s. Compare the
distance traveled (print both poses). Should they be similar — why or why not?

**5. The reverse flag.** Make two motors, one `reverse=False` and one `reverse=True`.
Give both `set_speed(0.5)`. Print both `.speed` values. Explain what reverse did.

**6. A `drive_power` helper.** Write a Python function `drive(robot, power, seconds)`
that drives straight at `power` for `seconds` using `run_for`. Use it to drive forward
1.5s. (You're packaging a behavior into a function — this is what `Motor` methods do.)

**7. Strafe.** Mecanum wheels can slide sideways. Drive with `set_drive_power(1.0, 0, 0)`
(that's the `x`/strafe input) for 1 second and print the pose. Which coordinate changed?

**8. Spin in place.** Drive with `set_drive_power(0, 0, 0.5)` for 1 second. Print the
heading. How many degrees did it turn? Now do `rx = -0.5` and confirm it turns the other
way.

**9. Clamp helper (write it yourself).** Without using the sim's clamp, write your own
Python function `clamp(value, lo=-1.0, hi=1.0)` that returns the value limited to the
range. Test it on `2.0`, `-3.0`, and `0.4`. (This exact idea appears all over robot code.)

**10. Normalize four powers (Juice's real trick).** In `Robot.java`, after computing four
wheel powers, Juice finds the biggest absolute value; if it's over 1.0, it divides *all
four* by that max so the ratios stay the same but nothing exceeds 1.0. Write a Python
function `normalize([fl, fr, bl, br])` that does this and return the new list. Test it on
`[1.5, -0.5, 1.0, 0.2]`. Compare your code to lines 682–696 of `Robot.java`.

## Java bridge

```java
// Exercise 6 idea: a method that drives straight for a time.
// (Real robots loop until a timer; here's the shape.)
public void drive(double power, double seconds) {
    ElapsedTime timer = new ElapsedTime();
    while (timer.seconds() < seconds) {
        setDrivePower(0, power, 0);
    }
    setDrivePower(0, 0, 0); // always stop at the end!
}

// Exercise 9: clamp -- Java has no built-in, you write it (or use Math.max/min):
double clamp(double v, double lo, double hi) {
    return Math.max(lo, Math.min(hi, v));
}
```

The Python `lambda t: robot.set_drive_power(...)` you pass to `run_for` is standing in
for the **body of the `while (opModeIsActive())` loop** you'll write in real Java.

➡️ Solutions: [`solutions/02_solution.py`](../solutions/02_solution.py)
