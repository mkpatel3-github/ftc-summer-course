"""Chapter 19 solutions - Motion Profiling: Smooth, Fast, Repeatable."""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
from ftcsim import AsymmetricMotionProfile, PIDFController


def ex1():
    prof = AsymmetricMotionProfile(distance=1000, max_v=500, accel=1000, decel=1000)
    print("total_time:", round(prof.total_time, 3))
    print("calculate(0):", round(prof.calculate(0), 1))
    print("calculate(total_time):", round(prof.calculate(prof.total_time), 1))


def ex2():
    prof = AsymmetricMotionProfile(distance=1000, max_v=500, accel=1000, decel=1000)
    tt = prof.total_time
    for t in (0, 0.25 * tt, 0.5 * tt, 0.75 * tt, tt):
        print(f"t={t:.2f} -> pos={prof.calculate(t):.1f}")


def ex3():
    prof = AsymmetricMotionProfile(distance=1000, max_v=500, accel=1000, decel=1000)
    tt = prof.total_time
    for t in (0, 0.25 * tt, 0.5 * tt, 0.75 * tt, tt):
        print(f"t={t:.2f} -> vel={prof.velocity(t):.1f}")
    # ramps up to ~max_v, holds, ramps back to 0 -- the trapezoid.


def ex4():
    prof = AsymmetricMotionProfile(distance=50, max_v=500, accel=1000, decel=1000)
    print("total_time:", round(prof.total_time, 3), "peak_v:", round(prof.peak_v, 1))
    print("peak_v < max_v?", prof.peak_v < prof.max_v)
    # The move is so short the profile must start braking before it ever reaches
    # max_v -- accelerate then immediately decelerate. The trapezoid is a triangle.


def ex5():
    sym = AsymmetricMotionProfile(distance=1000, max_v=500, accel=1000, decel=1000)
    asym = AsymmetricMotionProfile(distance=1000, max_v=500, accel=1000, decel=2000)
    print("symmetric total_time:", round(sym.total_time, 3))
    print("brake-harder total_time:", round(asym.total_time, 3))
    # Brake harder than you launch when a heavy lift would tip the robot if it
    # accelerated fast, but you still want a quick, firm stop at the top.


def ex6():
    prof = AsymmetricMotionProfile(distance=1000, max_v=500, accel=1000, decel=1000)
    tt = prof.total_time
    steps = 20
    for i in range(steps + 1):
        t = tt * i / steps
        pos = prof.calculate(t)
        print("#" * int(pos / 20))   # S-curve: slow, fast, level off


def ex7():
    prof = AsymmetricMotionProfile(distance=1000, max_v=500, accel=1000, decel=1000)
    pid = PIDFController(8.0, 0, 0, 0)
    pos = 0.0
    dt = 0.02
    t = 0.0
    while t <= prof.total_time:
        target = prof.calculate(t)
        power = pid.update(pos, target, dt=dt)
        pos += power * dt
        t += dt
    print("lift ended at:", round(pos, 1), "(target 1000)")


def ex8():
    prof = AsymmetricMotionProfile(distance=1000, max_v=500, accel=1000, decel=1000)

    # (a) slam: full power until past target, then stop.
    pos, dt, t = 0.0, 0.02, 0.0
    slam_trace = []
    for _ in range(200):
        power = 1.0 if pos < 1000 else 0.0
        pos += power * 1500 * dt        # slam moves fast and overshoots
        slam_trace.append(pos)
        if power == 0.0:
            break
    print("slam near end:", [round(p) for p in slam_trace[-3:]], "(overshot)")

    # (b) profile + PID: eases in to the target.
    pid = PIDFController(8.0, 0, 0, 0)
    pos, t = 0.0, 0.0
    prof_trace = []
    while t <= prof.total_time:
        power = pid.update(pos, prof.calculate(t), dt=dt)
        pos += power * dt
        prof_trace.append(pos)
        t += dt
    print("profile near end:", [round(p) for p in prof_trace[-3:]], "(no overshoot)")
    # Slam blows past 1000 and slams to a stop; profile decelerates into it.


def ex9():
    prof = AsymmetricMotionProfile(distance=1000, max_v=500, accel=1000, decel=1000)
    dt = 0.02

    def run(kv):
        pid = PIDFController(8.0, 0, 0, 0)
        pos, t, max_err = 0.0, 0.0, 0.0
        while t <= prof.total_time:
            target = prof.calculate(t)
            power = pid.update(pos, target, dt=dt) + kv * prof.velocity(t)
            pos += power * dt
            max_err = max(max_err, abs(target - pos))
            t += dt
        return max_err

    print("max error no FF:", round(run(0.0), 2))
    print("max error with FF:", round(run(1.0), 2))
    # kV adds the baseline power needed to MOVE at the profile's speed, so the
    # PID only fixes the small leftover error instead of generating all the push.


class Globals:
    LIFT_GROUND = 0
    LIFT_LOW = 800
    LIFT_HIGH = 1600


class Lift:
    def __init__(self):
        self.position = 0.0

    def go_to(self, name):
        target = getattr(Globals, f"LIFT_{name}")
        prof = AsymmetricMotionProfile(
            distance=abs(target - self.position) or 1,
            max_v=1500, accel=4000, decel=4000)
        pid = PIDFController(8.0, 0, 0, 0)
        start = self.position
        sign = 1 if target >= start else -1
        pos, t, dt = 0.0, 0.0, 0.02
        while t <= prof.total_time:
            tgt = prof.calculate(t)
            power = pid.update(pos, tgt, dt=dt)
            pos += power * dt
            t += dt
        self.position = start + sign * pos
        return self.position


def ex10():
    lift = Lift()
    for preset in ("GROUND", "HIGH", "LOW"):
        landed = lift.go_to(preset)
        print(f"{preset}: landed at {landed:.0f}")


if __name__ == "__main__":
    for name in ["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10"]:
        print("\n===", name, "===")
        globals()[name]()
