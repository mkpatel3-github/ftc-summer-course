# Chapter 1 — Hello, Robot

> Goal: get comfortable running code, printing to the robot's screen (telemetry),
> and seeing how a Python idea you know maps to the Java idea you'll write for Juice.

## Why this matters on a real FTC robot

On the robot there is no `print()`. The way the robot "talks" to you is **telemetry** —
lines of text on the Driver Station phone. In Juice's real code you'll see this in
*every* OpMode, for example in `TeleOpMainRed.java`:

```java
telemetry.addData("MODE", robot.mode.toString());
telemetry.addData("state: ", robot.state);
telemetry.update();
```

`addData` queues a line; `update()` actually draws it. Our simulator has the exact same
two methods, so you learn the real habit from day one.

## Python you already know vs. Java you'll write

You know Python like this:

```python
speed = 0.5
name = "Juice"
print(speed)
```

The same three lines in Java look like this:

```java
double speed = 0.5;   // you must say the TYPE: double = a decimal number
String name = "Juice"; // String = text
telemetry.addData("speed", speed);
```

The **ideas are identical**. The differences to notice:
- Java makes you declare a **type** (`double`, `int`, `boolean`, `String`).
- Java lines end with a **semicolon** `;`.
- Java prints with `telemetry.addData(...)`, not `print(...)`.

That's the whole game this summer: *learn the idea in Python, add the Java "costume."*

### The Python ↔ Java cheat sheet (keep this handy)

| Idea | Python | Java (FTC) |
|------|--------|------------|
| whole number | `x = 5` | `int x = 5;` |
| decimal | `x = 0.5` | `double x = 0.5;` |
| text | `s = "hi"` | `String s = "hi";` |
| true/false | `b = True` | `boolean b = true;` |
| print | `print(x)` | `telemetry.addData("x", x); telemetry.update();` |
| comment | `# note` | `// note` |
| and / or / not | `and or not` | `&& \|\| !` |

## Using the simulator

Every exercise file starts with the same two lines so Python can find the simulator:

```python
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
from ftcsim import Robot, Field, Gamepad, run_for
```

Then you make a robot and use its `telemetry`:

```python
robot = Robot()
robot.telemetry.add_data("hello", "Juice 16236")
robot.telemetry.update()
```

---

## Exercises

Do these in order. For each, **write Python that runs**, then read the "Java bridge"
and write the same thing as Java in a comment or on paper.

**1. Hello Juice.** Print one telemetry line that says `Team: Juice 16236`. Run it.

**2. Three types.** Make three variables: an `int` for your favorite robot's wheel
count (4), a `double` for a motor power (0.75), and a `String` for the team name.
Print all three with telemetry, each on its own line.

**3. Java costume.** Take your three variables from #2 and write — in a comment —
what each line would look like in Java (with the type and semicolon). Don't run the
Java; just write it correctly.

**4. Math like Python.** A robot drives at `0.6` power for `3.0` seconds. Compute and
print `distance = power * 3.0` (just the number, units don't matter yet).

**5. Booleans.** Make a `boolean`-style variable `is_red_alliance = True`. Print a
telemetry line `Alliance: RED` if it's true and `Alliance: BLUE` if false. (Use an
`if`/`else`.)

**6. The update() trap.** Add three telemetry lines but call `update()` only once at
the end. Then write a second version that calls `update()` after each line. Run both.
In a comment, explain what `update()` actually does (hint: it's like pressing "send").

**7. Average.** A motor's encoder reads 1800 ticks; another reads 1810. Print the
average. Then in a comment, note: in Java `(1800 + 1810) / 2` using `int` gives a
*surprising* answer — what is it and why? (This is the famous integer-division gotcha.)

**8. Rounding telemetry.** Real telemetry of a `double` is ugly (`6.000000001`). Print
a power value of `2/3` rounded to 2 decimals. (Python: `round(x, 2)`.)

**9. A status line like Juice.** Recreate the *style* of `TeleOpMainRed`'s telemetry:
print four lines — `MODE`, `COLOR`, `CLIMB`, `state` — with any sensible made-up values.
Make it look like a real driver station screen.

**10. Mini design.** In plain English (a comment block), list every piece of
information *you* would want on your driver station during a match, and why. No code —
this is the "think like a programmer" muscle. Compare your list to the four lines Juice
actually shows.

## Java bridge (read after you finish)

Here is exercise 1 and 5, fully translated, so you see where you're headed:

```java
// Exercise 1
telemetry.addData("Team", "Juice 16236");
telemetry.update();

// Exercise 5
boolean isRedAlliance = true;
if (isRedAlliance) {
    telemetry.addData("Alliance", "RED");
} else {
    telemetry.addData("Alliance", "BLUE");
}
telemetry.update();
```

Notice: `if (...) { } else { }` with **braces**, condition in **parentheses**. That's
the only real syntax difference from Python's `if:` / `else:`.

➡️ Solutions: [`solutions/01_solution.py`](../solutions/01_solution.py)
