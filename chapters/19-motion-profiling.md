# Chapter 19 — Motion Profiling: Smooth, Fast, Repeatable

> Goal: stop slamming mechanisms to full power and hoping. Generate a **motion profile** — a
> smooth plan of "where should I be at every instant" — and have your PID (Chapter 7) track
> it. This is how KookyBotz move a lift fast *and* land it gently, every single time.

## The problem with "just run the PID to the target"

In Chapter 7 your PID drove an error to zero. Point it at a far target and it commands huge
power instantly: the mechanism lurches, overshoots, maybe tips the robot, and slams to a
stop. A human driving a car doesn't floor it then brake at the wall — they **accelerate,
cruise, then ease off**. A motion profile makes the robot do the same.

## The trapezoid

A **trapezoidal profile** has three phases, named for the shape of its velocity-vs-time
graph:

```
velocity
  |      ____________            <- cruise at max_v
  |     /            \
  |    / accelerate   \ decelerate
  |   /                \
  |__/__________________\____ time
```

1. **Accelerate** at a fixed rate up to `max_v`.
2. **Cruise** at `max_v`.
3. **Decelerate** to a gentle stop exactly at the target.

If the move is short, you never reach `max_v` — the trapezoid becomes a **triangle** (speed
up, then immediately slow down). KookyBotz's `AsymmetricMotionProfile` even allows
*different* accelerate and decelerate rates (you can brake harder than you launch).

The profile answers one question: **"at time `t`, where should I be?"** That moving target
is the setpoint you feed your PID.

## Profile + PID + feedforward

The full pro stack (KookyBotz's `WActuatorGroup`) layers three ideas you now know:

1. **Profile** generates the target position (and velocity) for right now.
2. **PID** (Ch 7) corrects the error between target and actual.
3. **Feedforward** adds a baseline push: `kV * target_velocity` (and for an arm, a gravity
   term `kG * cos(angle)`) so the PID barely has to work.

Our sim gives you the profile so you can focus on using it:

```python
from ftcsim import AsymmetricMotionProfile
prof = AsymmetricMotionProfile(distance=1600, max_v=2000, accel=4000, decel=3000)
target_now = prof.calculate(t)     # where should the lift be at time t?
target_vel = prof.velocity(t)      # how fast should it be going (for feedforward)?
print(prof.total_time)             # how long the whole move takes
```

## Java bridge (KookyBotz's AsymmetricMotionProfile)

```java
profile = new AsymmetricMotionProfile(targetTicks,
              new ProfileConstraints(maxVel, accel, decel));
ProfileState state = profile.calculate(timer.seconds());
double power = pid.calculate(currentTicks, state.x)   // PID tracks the profile
             + kV * state.v;                          // + velocity feedforward
motor.setPower(power);
```

---

## Exercises

Use `from ftcsim import AsymmetricMotionProfile, PIDFController, Motor`. Build profiles and
read them with `calculate(t)` and `velocity(t)`; `total_time` is the duration.

**1. Make a profile.** Create `AsymmetricMotionProfile(distance=1000, max_v=500, accel=1000,
decel=1000)`. Print `total_time`, `calculate(0)`, and `calculate(total_time)`. Confirm it
starts at 0 and ends at 1000.

**2. Sample the curve.** Print `calculate(t)` for `t` = 0, 0.25, 0.5, 0.75, and `total_time`
of that profile. Confirm the position increases smoothly and lands on 1000.

**3. Velocity shape.** Print `velocity(t)` across the same times. Confirm it ramps up, holds
near `max_v`, then ramps down to 0 — the trapezoid.

**4. Triangle case.** Make a *short* move that never reaches cruise:
`AsymmetricMotionProfile(distance=50, max_v=500, accel=1000, decel=1000)`. Print `total_time`
and the peak velocity (`prof.peak_v`). Show `peak_v` is **less** than `max_v` — explain why
in a comment.

**5. Asymmetric.** Build two profiles for the same distance: one with `accel == decel`, one
that decelerates *twice* as hard as it accelerates. Print both `total_time`s and describe,
in a comment, when you'd want to brake harder than you launch.

**6. Plot it (ASCII).** For a profile, print one line per time step where the number of `#`
characters is proportional to `calculate(t)`. You should *see* the S-shaped position curve
rise and level off. (No libraries — just `"#" * int(pos / scale)`.)

**7. Track it with a PID.** Simulate a lift: a position variable starting at 0. Each step
`dt=0.02`, compute the profile target `calculate(t)`, run a `PIDFController` to get power,
and move the position by `power * step_size`. Show the lift follows the profile and ends
near the target. (Tune kp until it tracks.)

**8. Profile vs slam.** Compare two strategies to reach 1000: (a) "slam" = full power until
past target then stop, (b) profile + PID. Print the position trace of each near the end and
describe the overshoot difference in a comment.

**9. Add feedforward.** Extend exercise 7: add `kV * profile.velocity(t)` to the PID output.
Show the tracking error (target − actual) is **smaller** with feedforward than without.
Explain what `kV` is doing.

**10. Lift presets, profiled.** Combine with Chapter 17: write a `Lift` that, given a
`Globals` preset height, builds a profile from its current position to the target and tracks
it. Command it GROUND → HIGH → LOW and print where it lands each time. This is a real,
competition-grade lift.

## Java bridge

```java
// KookyBotz WActuatorGroup, in spirit -- profile + PID + gravity feedforward:
this.setMotionProfile(targetTicks, new ProfileConstraints(maxVel, accel, decel));
ProfileState s = profile.calculate(timer.seconds());
double ff = kV * s.v + kG * Math.cos(armAngleRadians);  // velocity + gravity FF
motor.setPower(pid.calculate(encoder.getCurrentPosition(), s.x) + ff);
```

➡️ Solutions: [`solutions/19_solution.py`](../solutions/19_solution.py)
