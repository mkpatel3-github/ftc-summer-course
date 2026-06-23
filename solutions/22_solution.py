"""Chapter 22 solutions - The Tuning Workflow: @Config, Dashboard, and a Method."""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
from ftcsim import AsymmetricMotionProfile, PIDFController


def run_gains(kp, kv, dt=0.02):
    """One 'dashboard run': track the profile with these gains, return max error."""
    prof = AsymmetricMotionProfile(distance=1000, max_v=500, accel=1000, decel=1000)
    pid = PIDFController(kp, 0, 0, 0)
    pos, max_err, t = 0.0, 0.0, 0.0
    while t <= prof.total_time:
        target = prof.calculate(t)
        power = pid.update(pos, target, dt=dt) + kv * prof.velocity(t)
        pos += power * dt
        max_err = max(max_err, abs(target - pos))
        t += dt
    return max_err


def ex1():
    print("max error (kp=0.5, kv=0):", round(run_gains(0.5, 0), 2))


def ex2():
    best = None
    for kp in (0.1, 0.5, 1, 2, 5, 10):
        err = run_gains(kp, 0)
        print(f"kp={kp}: error={err:.2f}")
        if best is None or err < best[1]:
            best = (kp, err)
    print("best kp:", best[0], "error:", round(best[1], 2))


def ex3():
    for kp in (100, 105, 110):
        # track the trace to detect oscillation (sign flips in the error)
        prof = AsymmetricMotionProfile(1000, 500, 1000, 1000)
        pid = PIDFController(kp, 0, 0, 0)
        pos, t, flips, last_err = 0.0, 0.0, 0, 0.0
        while t <= prof.total_time:
            err = prof.calculate(t) - pos
            if last_err != 0 and (err > 0) != (last_err > 0):
                flips += 1
            last_err = err
            pos += pid.update(pos, prof.calculate(t), dt=0.02) * 0.02
            t += 0.02
        print(f"kp={kp}: error={run_gains(kp,0):.2f} sign-flips={flips}")
    # Past ~kp=100 the error stops shrinking and the sign flips repeatedly: that's
    # oscillation, and it blows up. Stop raising kP before the buzz starts.


def ex4():
    for kv in (0, 0.25, 0.5, 1.0, 1.5):
        print(f"kv={kv} (kp=0): error={run_gains(0, kv):.2f}")
    # kv=1.0 alone tracks almost perfectly with NO PID -- which is why you tune
    # feedforward first and let PID clean up only the small leftover error.


def ex5():
    # A gentle, SAFE kp far from the oscillation threshold (~100 from ex3).
    safe_kp = 5
    best_kv = 1.0                       # from the ex4 sweep
    print(f"kp={safe_kp} no FF: error={run_gains(safe_kp, 0):.2f}")
    print(f"kp={safe_kp} + FF(kv={best_kv}): error={run_gains(safe_kp, best_kv):.2f}")
    # A gentle kp alone tracks poorly; adding feedforward makes it track well, so
    # you NEVER have to crank kp up near instability. Tuning order: feedforward
    # (kV/kG) -> kP -> kD -> kI (only if needed).


def ex6():
    a = run_gains(0.5, 0)
    b = run_gains(2, 1.0)              # changed BOTH kp and kv
    print(f"before (kp=0.5,kv=0): {a:.2f}  after (kp=2,kv=1.0): {b:.2f}")
    print("better, but which change helped? unknown.")
    # Two variables moved at once -> the improvement can't be attributed. Single-
    # variable sweeps (ex2, ex4) tell you exactly which knob did the work.


def run_gains_scored(kp, kv, dt=0.02):
    prof = AsymmetricMotionProfile(1000, 500, 1000, 1000)
    pid = PIDFController(kp, 0, 0, 0)
    pos, max_err, t = 0.0, 0.0, 0.0
    settle_t = None
    band = 0.01 * prof.distance         # 1% of distance
    while t <= prof.total_time:
        target = prof.calculate(t)
        power = pid.update(pos, target, dt=dt) + kv * prof.velocity(t)
        pos += power * dt
        err = abs(target - pos)
        max_err = max(max_err, err)
        if err < band and settle_t is None and t > prof.t_accel:
            settle_t = t
        elif err >= band:
            settle_t = None             # left the band, reset
        t += dt
    return max_err, settle_t


def ex7():
    for kp in (1, 5, 20):
        me, st = run_gains_scored(kp, 0)
        print(f"kp={kp}: max_err={me:.2f} settle_t={st}")
    # "Better" is two numbers: a high kp may settle fast but with a big transient
    # error; you choose the trade-off your mechanism can tolerate.


def ex8():
    coarse = min(((kp, run_gains(kp, 0)) for kp in (1, 10, 100)), key=lambda x: x[1])
    # Fine sweep stays BELOW the ~100 oscillation threshold from ex3.
    fine_vals = [40, 50, 60, 75]
    fine = min(((kp, run_gains(kp, 0)) for kp in fine_vals), key=lambda x: x[1])
    print("coarse winner:", coarse[0], "refined best:", round(fine[0], 2),
          "error:", round(fine[1], 2))
    # Coarse-to-fine finds a good, STABLE gain in ~7 runs instead of a thousand.


def ex9():
    n = 6
    slow = n * 90
    fast = n * 5
    print(f"{n} values, build-deploy @90s: {slow}s ({slow/60:.1f} min)")
    print(f"{n} values, dashboard @5s: {fast}s")
    print(f"speedup: {slow/fast:.0f}x  <- this is why @Config exists")


def ex10():
    print("""TUNING PLAYBOOK (profiled mechanism, from scratch):
  1. FEEDFORWARD FIRST. PID off (kp=0). Raise kV until the mechanism roughly
     keeps up with the profile on its own. Add kG for an arm (gravity).
     Watch: does it track the profile's velocity? Move on when 'close'.
  2. kP NEXT. One variable at a time. Raise kP until the leftover error is small
     and response is crisp. Watch: max tracking error. STOP before it buzzes.
  3. kD TO DAMP. Add a little to kill the overshoot/oscillation kP introduced.
     Watch: does the overshoot disappear without making it sluggish?
  4. kI LAST, SPARINGLY. Only if a steady-state error refuses to die.
     Watch: does the final resting error go to zero? Too much = slow wobble.
  RULES: change ONE constant per run; measure (max error + settling time), don't
  eyeball; keep the value that minimized the score; use the dashboard so each try
  is 5s, not a 90s rebuild. DONE when target and actual graphs overlap.""")


if __name__ == "__main__":
    for name in ["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10"]:
        print("\n===", name, "===")
        globals()[name]()
