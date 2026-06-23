# Chapter 22 — The Tuning Workflow: @Config, Dashboard, and a Method

> Goal: stop guessing gains. Every controller you've built — PID (Ch 7), motion profile
> (Ch 19), feedforward — has numbers you must *tune*. Top teams don't tune by editing code,
> rebuilding, and redeploying for 90 seconds each try. They expose the numbers **live** with
> `@Config` + **FTC Dashboard** and follow a **repeatable method**. This chapter teaches that
> method on the controllers you already own.

## The slow way (what beginners do)

You set `kp = 0.01`, build, deploy (≈90s), watch the robot, decide it's too sloppy, set
`kp = 0.02`, build, deploy again... Ten tries is fifteen minutes of standing around. Worse,
you change *three* numbers at once, the robot gets better, and you have **no idea which
change helped**. That's not tuning — that's superstition.

## The fast way: live constants with @Config

ACME's RoadRunner quickstart and every serious team mark their tuning numbers with
`@Config`. That one annotation publishes the field to **FTC Dashboard** — a web page at
`192.168.43.1:8080/dash` — where you drag a slider and the robot's value changes **instantly,
no rebuild**. You watch a live graph of "target vs actual" and turn the knob until it tracks.

```java
@Config
public class DriveTuning {
    public static double KP = 0.01;   // <- editable LIVE in the dashboard
    public static double KV = 0.0002;
    public static double MAX_V = 2000;
}
```

The pattern: **one variable changes at a time, you watch one number (the error), you keep the
value that minimized it.** That's the whole game. Our sim has no web slider, but it has the
thing that *matters* — a fast loop that prints the error — so you can practice the method.

## A method, not magic

Here's the order top teams tune a profiled-PID lift (it generalizes):

1. **Feedforward first (kV, kG).** With PID off (kp=0), raise kV until the mechanism roughly
   keeps up with the profile on its own. Good FF means the PID barely has to work.
2. **kP next.** Bring up the proportional gain until the *remaining* error is small and the
   mechanism is responsive — but stop before it buzzes/oscillates.
3. **kD to damp.** Add a little derivative to kill the overshoot/oscillation kP introduced.
4. **kI last, sparingly.** Only if a steady-state error refuses to die. Too much kI = slow
   wind-up wobble.

You **measure** at each step — peak error, settling time — so "better" is a number, not a
vibe. That measurement loop is what you'll build here.

## The sim's tuning bench

You already have everything: a `PIDFController`, an `AsymmetricMotionProfile`, and a fast
deterministic loop. A "tuning run" is: simulate the mechanism tracking the profile with a
given set of gains, and return a *score* (e.g. max tracking error). Sweep one gain, keep the
best score. That's a dashboard session, in code:

```python
from ftcsim import AsymmetricMotionProfile, PIDFController

def run_gains(kp, kv, dt=0.02):
    prof = AsymmetricMotionProfile(distance=1000, max_v=500, accel=1000, decel=1000)
    pid = PIDFController(kp, 0, 0, 0)
    pos, max_err = 0.0, 0.0
    t = 0.0
    while t <= prof.total_time:
        target = prof.calculate(t)
        power = pid.update(pos, target, dt=dt) + kv * prof.velocity(t)
        pos += power * dt            # toy "plant": power moves the mechanism
        max_err = max(max_err, abs(target - pos))
        t += dt
    return max_err                   # lower = better tracking
```

Sweep `kp`, print the error for each, pick the minimum — that's exactly what dragging the
dashboard slider does, minus the standing around.

## Java bridge (ACME tuning OpModes + FTC Dashboard)

```java
@Config
public class ArmTuning {
    public static double kP = 0.01, kD = 0.0, kV = 0.0002, kG = 0.05;
}
// In the tuning OpMode, every loop:
double target = profile.calculate(timer.seconds()).x;
double ff = ArmTuning.kV * profile.velocity() + ArmTuning.kG * Math.cos(angle);
double power = pid.calculate(encoder.getPos(), target, ArmTuning.kP, ArmTuning.kD) + ff;
motor.setPower(power);
// Dashboard graphs target vs encoder.getPos(); you tune kP/kD live until they overlap.
```

RoadRunner ships dedicated tuning OpModes (`ManualFeedforwardTuner`, `DriveVelocityTuner`,
etc.) that do exactly this for the drive base — sweep one constant, watch one graph.

---

## Exercises

Use `from ftcsim import AsymmetricMotionProfile, PIDFController`. Build the `run_gains` bench
from the lesson and use it to *measure* — every claim below should be backed by a printed
number, not a guess.

**1. Build the bench.** Write `run_gains(kp, kv)` from the lesson (profile distance=1000,
max_v=500, accel=decel=1000). Call it once with `kp=0.5, kv=0` and print the max tracking
error. This is your "one dashboard run".

**2. Sweep kP.** Call `run_gains` for `kp` in `[0.1, 0.5, 1, 2, 5, 10]` (kv=0). Print each
kp and its error. Identify the kp with the **lowest** error — that's what dragging the slider
finds for you.

**3. Too much kP.** Keep raising kp well past the best value from exercise 2 (try 100, 105,
110). Track the error's sign over time and count **sign flips**. Show that past a threshold
the error stops shrinking and starts **oscillating** (the sign flips repeatedly, the value
blows up). In a comment: this is why you stop *before* the buzz.

**4. Feedforward first.** Set kp=0 and sweep `kv` in `[0, 0.25, 0.5, 1.0, 1.5]`. Print the
error for each. Show a good kv alone (no PID!) already tracks the profile well — the reason
teams tune FF *before* PID. (For this plant the sweet spot is near kv=1.0.)

**5. FF + PID together.** PID alone can only track well by cranking kp dangerously high (near
the oscillation threshold from exercise 3). Show the better way: pick a **gentle, safe** kp
(e.g. 5) and compare its error *without* feedforward vs *with* your best kv from exercise 4.
Show FF makes the gentle kp track well — so you never have to live near instability. In a
comment, restate the tuning order (FF, then P, then D, then I).

**6. One variable at a time.** Demonstrate the cardinal rule: do a run where you change kp
**and** kv at once and it gets better — then argue (in a comment) why you can't tell which
one helped. Contrast with the single-variable sweeps above.

**7. Score, don't eyeball.** Extend the bench to also return **settling time** (first time
the error drops under 1% of distance and stays). Print both max-error and settling-time for
three kp values. Show "better" can be two numbers that trade off.

**8. A coarse-to-fine search.** Find the best kp in two passes: first a coarse sweep
(`[1, 10, 100]`), then a fine sweep around the coarse winner — staying **below** the
oscillation threshold (e.g. 40, 50, 60, 75). Print the refined best. This is how you tune fast
without testing a thousand values (and without blowing past the stability edge).

**9. Simulate the slow way's cost.** You have 6 candidate kp values. Print the wall-clock cost
of tuning them on a real robot at **90 s per build-deploy-test** vs. live on the dashboard at
**5 s per slider try**. (Just arithmetic.) Show why `@Config` exists.

**10. Write your tuning playbook.** In a comment block, write the step-by-step procedure your
team will follow to tune a new profiled mechanism from scratch: which constant first, what
you watch, when you move on, when you're done. Reference the order from the lesson and the
single-variable rule. This is the deliverable a top team actually keeps in their repo.

## Java bridge

```java
// RoadRunner's drive tuning, in spirit: expose the constant, graph the result, sweep.
@Config
public class MecanumDrive {
    public static double LATERAL_MULTIPLIER = 1.0;   // tune live on the dashboard
}
// ManualFeedforwardTuner runs the wheels at a profile and graphs target vs measured
// velocity; you drag kV/kS until the lines overlap. No rebuild between tries.
```

You now have the *method* that turns all the controllers in this course from "numbers I
copied" into "numbers I measured." That's the difference between a robot that sort-of works
and one that works every match.

➡️ Solutions: [`solutions/22_solution.py`](../solutions/22_solution.py)
