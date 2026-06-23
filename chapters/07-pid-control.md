# Chapter 7 — PID Control

> Goal: build the single most important algorithm in competitive FTC, the one Juice uses
> to hold their lift at an exact height: the **PID controller**. You already met its "P"
> in Chapters 4 and 5. Now you build the whole thing — a real port of
> `util/control/PIDFController.java`.

## The problem PID solves

You want a mechanism to *go to a target and hold it*: a lift at 960 ticks, a heading at
90°, a distance at 12 inches. Bang-bang control ("full power until you pass it, then
off") overshoots and oscillates. PID makes a **smooth, accurate** approach by setting
power from the **error** in three smart ways.

```
error = target - current
```

| Term | Formula | What it does | Feels like |
|------|---------|--------------|------------|
| **P** proportional | `kp * error` | push harder the farther you are | a spring |
| **I** integral | `ki * sum_of_error_over_time` | erase small leftover error that P can't | stubbornness |
| **D** derivative | `kd * change_in_error` | brake as you approach, kill overshoot | a shock absorber |
| **F** feedforward | `kf * sign(error)` (or gravity) | constant push to beat friction/gravity | a helping hand |

Output = `P + I + D + F`. That's it. Juice's `Lift.java` literally does:

```java
double pid1 = controller1.calculate(motorPos, target);
double ff = f;                       // feedforward for gravity on the lift
power1 = (pid1 + ff) * voltageCompensation;
```

## Juice's real PIDF (your blueprint)

From `PIDFController.java`, the heart of `update(newInput, setPoint)`:

```java
error = setPoint - newInput;                  // (or norm(...) if rotational)
errorSum_ += (error * period);                // integral
derError = (error - lastError_) / period;     // derivative
double output = kp_*error + ki_*errorSum_ + kd_*derError + kf_*Math.signum(error);
lastError_ = error;
```

Two pro details Juice includes, which you'll also implement:
- **Reset the integral when error flips sign** (`if signum changed: errorSum_ = 0`) — stops
  "integral windup" from making the robot overshoot.
- **Time-based**: it multiplies/divides by the real elapsed `period`, so it behaves the
  same whether the loop is fast or slow.

## Tuning (the part that's an art)

You pick `kp, ki, kd, kf` by experiment, in this order:
1. Raise **P** until it reaches the target but oscillates a little.
2. Add **D** to damp the oscillation.
3. Add a tiny **I** only if it stops *just short* of the target.
4. Add **F** if gravity/friction pulls it off target at rest.

---

## Exercises

Use a simple "plant" to practice without a robot: a number `position` that moves toward
its target by the power you give it. The sim provides `PIDFController`, but in these
exercises **you write your own** and compare.

**1. P-only controller.** Write `p_control(error, kp)` returning `kp*error`. Simulate a
lift: `position` starts at 0, target 1000; each step `position += p_control(target-pos,
0.001) * 50`. Loop 100 times, print position every 20 steps. Does it reach 1000? Does it
overshoot?

**2. Feel the gain.** Repeat exercise 1 with `kp = 0.0005`, `0.001`, `0.005`. Describe
(comment) what too-low and too-high P feel like (slow vs. oscillating).

**3. Add D.** Extend to `pd_control(error, last_error, kp, kd, dt)`. Add D and re-run.
Show that a good D reduces overshoot compared to P-only.

**4. Build the class.** Write a `MyPIDF` class with `__init__(kp, ki, kd, kf)` and
`update(current, target)` that tracks `last_error`, `error_sum`, and `last_time` —
mirroring `PIDFController.java`. Return P+I+D+F.

**5. Integral windup reset.** Add the "reset `error_sum` when error changes sign" rule to
`MyPIDF`. Demonstrate with a target that the controller overshoots: show the integral
getting reset.

**6. Drive to a heading with YOUR PID.** Replace the hand-tuned `error*gain` turn from
Chapter 4 with `MyPIDF`. Turn to 90°. Tune kp/kd until it settles within 1° without
wild oscillation. Print the final heading.

**7. Lift to a height.** Model a lift: `ticks` moves toward a target by your PID's
output each loop. Use `MyPIDF` to drive it from 0 to 960 ticks (Juice's HIGH_RUNG
value!). Print ticks every 10 loops; show it settles near 960.

**8. Feedforward vs gravity.** Add a constant "gravity" that subtracts 5 ticks every
loop (the lift sags). Show that without `kf` the lift settles *below* target, and adding
`kf` (a constant up-push) fixes it. This is exactly why `Lift.java` adds `ff = f`.

**9. Compare to the real port.** Run the sim's built-in `PIDFController` (the faithful
Java port) and your `MyPIDF` on the same problem with the same gains. They should behave
almost identically. Print both final values.

**10. Tune Juice's real lift gains.** `Lift.java` uses `p=0.02, i=0.0, d=0.00045,
f=0.125`. Plug those into your controller for the 0→960 lift and see how it behaves.
Then try to beat it (faster settle, less overshoot) by adjusting d. Report your best
gains and why they're better. (This is the actual job of a Juice software member.)

## Java bridge

You're literally reimplementing Juice's file. Here's the core of your `update`, beside
theirs:

```java
public float update(double newInput, double setPoint) {
    long time = System.currentTimeMillis();
    long period = time - lastTime_;
    error = setPoint - newInput;
    if (Math.signum(lastError_) != Math.signum(error)) errorSum_ = 0; // anti-windup
    errorSum_ += error * period;
    derError = (error - lastError_) / period;
    double output = kp_*error + ki_*errorSum_ + kd_*derError + kf_*Math.signum(error);
    lastError_ = error;
    lastTime_ = time;
    return (float) output;
}
```

When you can read this file and explain every line, you understand the engine behind
every accurate FTC mechanism.

➡️ Solutions: [`solutions/07_solution.py`](../solutions/07_solution.py)
