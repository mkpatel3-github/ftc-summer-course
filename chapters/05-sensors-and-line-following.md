# Chapter 5 — Sensors & Line Following

> Goal: react to the world. Use a **color sensor** to detect a game piece's color (just
> like Juice's `Claw.detectSample()`), a **distance sensor** to stop before a wall, and
> combine them into **line following** — another FLL favorite, now in FTC.

## Sensors are just functions that return numbers

A color sensor reports how much **red**, **green**, **blue** light it sees (each 0..1)
and how far away the surface is. In the sim:

```python
robot.color.red()        # 0..1
robot.color.green()
robot.color.blue()
robot.color.get_distance()   # mm to the surface
robot.distance.get_distance()  # inches to the wall ahead
```

## Juice's real color logic (and a real bug!)

Juice detects which "sample" is in the claw in `Claw.detectSample()`:

```java
float red = colorSensor.getNormalizedColors().red;
float blue = colorSensor.getNormalizedColors().blue;
float green = colorSensor.getNormalizedColors().green;
if (colorSensor.getNormalizedColors().blue > 0) {
    return SampleColors.BLUE;
} else if ()        // <-- this line is unfinished in their repo!
```

That `else if ()` is literally broken in their codebase (it was a work-in-progress
commit). **You are going to write the version that actually works.** This is real: even
good teams ship half-finished code, and reading/fixing it is a core skill.

The right idea: compare the channels. Whichever of red/green/blue is **largest** tells
you the color. Yellow is interesting — it's high red **and** high green, low blue.

## The decision pattern

Sensors feed `if/elif/else`. That's it. The whole skill is choosing good thresholds:

```
if blue is clearly the biggest:   return "BLUE"
elif red and green both high:      return "YELLOW"
elif red is the biggest:           return "RED"
else:                              return None   # nothing detected
```

## Line following intuition

A line follower rides the *edge* of a line: if the sensor sees dark, steer one way; if
it sees light, steer the other. It's the same `error → correction` idea as gyro-straight,
but the "error" comes from a light sensor instead of the gyro.

---

## Exercises

For sensor exercises, place a sample on the field first:

```python
from ftcsim import Robot, Field
f = Field(); f.sample_x = 10; f.sample_y = 0; f.sample_color = "BLUE"
robot = Robot(field=f)
```

**1. Read the sensor.** Put a BLUE sample at (10, 0). Drive the robot to it (forward) and
print `red()`, `green()`, `blue()` once it's on top. Note which channel is high.

**2. detect_color v1.** Write `detect_color(robot)` that returns `"BLUE"` if blue is the
biggest channel, else `None`. Test on a blue sample and on empty floor.

**3. Fix Juice's bug.** Extend `detect_color` to return `"RED"`, `"BLUE"`, or `"YELLOW"`
correctly: yellow = red high AND green high AND blue low; otherwise whichever of red/blue
is bigger. Test all three colors by changing `f.sample_color`.

**4. Alliance filter.** Write `should_keep(color, alliance)` — Juice keeps a sample if
it's YELLOW or matches the alliance color, else ejects it. Mirror the idea from
`Claw.smartStopDetect`: return `1` (keep), `-1` (eject), or `0` (nothing). Test for a RED
alliance seeing each color.

**5. Drive until you see it.** Write a loop that drives forward until `detect_color`
returns non-None, then stops. Print where it stopped. (Sensor-driven stopping — like
intaking until a game piece is detected.)

**6. Distance stop.** Using `robot.distance.get_distance()` (inches to the front wall),
drive forward until you're 12 inches from the wall, then stop. Print the final distance.

**7. Wall follow / approach (proportional).** Instead of a hard stop, slow down smoothly:
drive with `power = (distance - 12) * 0.05`, clamped to 0..0.6, until distance is ~12.
Compare the stopping smoothness to exercise 6.

**8. Line following — set up.** Our `Field` has a black line at `x = line_x`. Write a
helper `on_line(robot)` that returns True when the robot's `x` is within
`line_half_width` of `line_x`. (Pretend this is a downward light sensor reading dark.)

**9. Line following — follow it.** The line runs along x=0 up the field. Drive forward
(+y) while steering to keep `x` near 0: `rx`-style correction using
`error = 0 - robot.x`. Start the robot at x=4 and show it converges back toward x≈0 as it
drives up the field. (This is the same proportional-control shape again!)

**10. Mission: sort a sample.** Put a sample of a random color in front of the robot.
Drive to it, detect its color, decide keep/eject for the BLUE alliance, and print a
clear action line (`KEEP blue` or `EJECT red`). This mirrors exactly what Juice's
intake does during a match.

## Java bridge

```java
// detect_color, the version that FIXES Juice's broken else-if:
public SampleColors detectSample() {
    NormalizedRGBA c = colorSensor.getNormalizedColors();
    if (c.red > 0.5 && c.green > 0.5 && c.blue < 0.3) {
        return SampleColors.YELLOW;
    } else if (c.blue > c.red) {
        return SampleColors.BLUE;
    } else if (c.red > c.blue) {
        return SampleColors.RED;
    }
    return null;
}
```

Compare this to the unfinished `detectSample()` in
`subsystems/claw/Claw.java` — you've completed what their commit started.

➡️ Solutions: [`solutions/05_solution.py`](../solutions/05_solution.py)
