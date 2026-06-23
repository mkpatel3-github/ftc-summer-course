# Chapter 21 — Sensor Fusion & the Kalman Filter

> Goal: combine two imperfect position sources into one estimate that's better than either
> alone — a **smooth-but-drifting** odometry reading and a **jumpy-but-absolute** camera
> reading. You'll build the exact little **Kalman filter** that Capital City Dynamics
> (#12087, j5155) — the author of the localizer Juice itself uses — ships in `KalmanFilter.java`.

## Two sensors, opposite flaws

You've met both already:

- **Odometry** (Ch 13): updates every loop, beautifully smooth — but it **drifts**. Errors
  from wheel slip and bumps slowly pile up, so after 30 seconds it's confidently *wrong*.
- **Camera / AprilTags** (Ch 14): **absolute** — it tells you where you truly are, no drift —
  but it's **jumpy** (noisy each reading) and only works when a tag is visible.

What if you could get the smoothness of odometry **and** the no-drift truth of the camera?
That's **sensor fusion**, and the classic tool is the **Kalman filter**.

## The idea (no scary math)

A Kalman filter keeps a running **estimate** and, each step, does two things:

1. **Predict.** Move the estimate by however far odometry says you moved this step. (Trust
   your motion model.)
2. **Correct.** Nudge the estimate toward the camera's absolute reading — but only *partly*,
   weighted by how much you trust the sensor vs. the model.

That weight is the **Kalman gain** `K`. It comes from two numbers you choose:

- **Q** — process/model noise. Bigger Q = "trust the prediction less."
- **R** — measurement noise. Bigger R = "trust the camera less."

The whole filter is tiny — here it is, the same shape as j5155's Java:

```python
class MyKalman:
    def __init__(self, q, r):
        self.Q, self.R = q, r
        self.x = 0.0    # estimate
        self.p = 1.0    # uncertainty
    def update(self, model_delta, measurement):
        self.x += model_delta          # predict
        self.p += self.Q
        k = self.p / (self.p + self.R) # Kalman gain
        self.x += k * (measurement - self.x)   # correct toward sensor
        self.p *= (1 - k)
        return self.x
```

Big R → small gain → output stays smooth like odometry. Small R → big gain → output snaps to
the camera. You **tune** Q and R to taste — exactly like tuning a PID.

## Why this is the capstone of localization

This is what makes Juice's `KalmanDrive` work and why j5155's code is widely studied: the
robot trusts smooth odometry moment-to-moment, but the camera quietly erases drift whenever a
tag is in view. The result is a pose you can trust for a whole match. The sim ships a
reference `KalmanFilter` so you can check your version:

```python
from ftcsim import KalmanFilter
kf = KalmanFilter(q=0.1, r=2.0)
kf.set_state(0.0)
fused = kf.update(model_delta=5.0, measurement=4.0)
```

---

## Exercises

Use `from ftcsim import Robot, Field, KalmanFilter, run_for`. For a realistic setup, make
odometry drift and the camera noisy: `robot.odometry.drift_per_read = 0.05`,
`robot.camera.noise = 1.0`, and `field = Field().add_standard_tags()`.

**1. Build your own.** Write the `MyKalman` class from the lesson. Run `update(5, 4)` once
from a 0 start and print the result. Compare it to the sim's `KalmanFilter(q,r)` with the
same Q/R — they should match.

**2. Trust knobs.** With your filter, fuse the same inputs (`model_delta=10`, `measurement=0`)
twice: once with a **large R** (trust sensor little) and once with a **small R** (trust
sensor a lot). Print both outputs and explain the difference in a comment.

**3. Smooth a noisy signal.** Feed your filter a sequence of noisy measurements of a value
that's really 50 (e.g. 48, 53, 49, 51, 47...) with `model_delta=0` each step. Print the
estimate converging toward 50 and staying steady — the filter is smoothing.

**4. See the drift.** Drive forward 2s with `robot.odometry.drift_per_read = 0.05`. Print the
odometry pose's x vs the true `robot.x`. Show odometry now reads too high — that's
accumulated drift.

**5. See the noise.** With `robot.camera.noise = 1.0` and tags placed, read
`robot.camera.localize().x` five times without moving. Show it jumps around the true value —
absolute but jittery.

**6. Fuse x, one step.** Each loop you have: `model_delta` = how far odometry *says* x moved
this step, and `measurement` = the camera's x. Fuse them with a `KalmanFilter` for one step
and print the fused x. (You're combining exercises 4 and 5.)

**7. Fuse over a whole drive.** Drive forward 2s. Each loop, feed the Kalman filter the
odometry delta (predict) and the camera x (correct). Print, at the end, the fused x, the raw
odometry x, and the true x. Show fused is **closer to true** than drifting odometry.

**8. Tune Q and R.** Repeat exercise 7 with three (Q, R) settings: trust-camera-heavy,
trust-odometry-heavy, and balanced. Print the final error for each. Find the one that's
smoothest *and* accurate. In a comment, relate Q/R tuning to PID gain tuning.

**9. Camera drops out.** Realistic case: the camera only sees a tag for part of the drive.
When `localize()` returns `None`, skip the correct step (predict only). Show the fused
estimate coasts on odometry during the blackout and re-snaps when the tag reappears.

**10. Two-axis fusion.** Run two Kalman filters — one for x, one for y — to fuse a full 2D
position over a forward+strafe path. Print the fused (x, y) vs true (x, y). In a comment,
note this is exactly how j5155's `Vector2dKalmanFilter` composes two 1-D filters, and how
Juice's `KalmanDrive` keeps its pose honest all match.

## Java bridge (j5155 / Capital City Dynamics KalmanFilter.java)

```java
// predict with the motion model, correct with the absolute sensor:
public double update(double modelDelta, double measurement) {
    x += modelDelta;  p += Q;             // predict
    double k = p / (p + R);               // Kalman gain
    x += k * (measurement - x);  p *= (1 - k);   // correct
    return x;
}
```

In `AprilTagDrive.java` this runs every loop: odometry predicts, the AprilTag fix corrects,
and the robot's pose never drifts away. You've now built the heart of modern FTC localization.

➡️ Solutions: [`solutions/21_solution.py`](../solutions/21_solution.py)
