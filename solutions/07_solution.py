"""Chapter 7 solutions - PID Control.

We use a fixed dt (not wall-clock) in MyPIDF so results are repeatable in print.
The real PIDFController uses wall-clock time; the math is identical.
"""
import sys, os, math
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
from ftcsim import Robot, PIDFController, run_for


def p_control(error, kp):
    return kp * error


def ex1():
    pos, target = 0.0, 1000.0
    for i in range(100):
        pos += p_control(target - pos, 0.001) * 50
        if i % 20 == 0:
            print(f"  step {i:3d}: pos={pos:7.1f}")
    print("final:", round(pos, 1))  # approaches 1000, little/no overshoot at low kp


def ex2():
    for kp in (0.0005, 0.001, 0.005):
        pos, target = 0.0, 1000.0
        for _ in range(100):
            pos += p_control(target - pos, kp) * 50
        print(f"kp={kp}: final={pos:8.1f}")
    # low kp -> slow, never quite arrives; high kp -> overshoots / oscillates.


def pd_control(error, last_error, kp, kd, dt):
    return kp * error + kd * (error - last_error) / dt


def ex3():
    for label, kd in (("P-only", 0.0), ("PD", 0.02)):
        pos, last_err, target, dt = 0.0, 0.0, 1000.0, 0.02
        peak = 0.0
        for _ in range(120):
            err = target - pos
            pos += pd_control(err, last_err, 0.004, kd, dt) * 50 * dt
            last_err = err
            peak = max(peak, pos)
        print(f"{label}: final={pos:7.1f} peak={peak:7.1f} overshoot={peak-target:6.1f}")


class MyPIDF:
    def __init__(self, kp, ki, kd, kf, dt=0.02):
        self.kp, self.ki, self.kd, self.kf = kp, ki, kd, kf
        self.dt = dt
        self.last_error = 0.0
        self.error_sum = 0.0
        self.reset_count = 0

    def update(self, current, target, anti_windup=False):
        error = target - current
        if anti_windup and math.copysign(1, self.last_error) != math.copysign(1, error):
            self.error_sum = 0.0
            self.reset_count += 1
        self.error_sum += error * self.dt
        der = (error - self.last_error) / self.dt
        out = (self.kp * error + self.ki * self.error_sum
               + self.kd * der + self.kf * math.copysign(1, error))
        self.last_error = error
        return out


def ex4():
    pid = MyPIDF(0.004, 0.0, 0.02, 0.0)
    pos, target = 0.0, 1000.0
    for _ in range(120):
        pos += pid.update(pos, target) * 50 * 0.02
    print("MyPIDF final:", round(pos, 1))


def ex5():
    pid = MyPIDF(0.02, 0.0008, 0.0, 0.0)
    pos, target = 0.0, 100.0
    for i in range(200):
        out = pid.update(pos, target, anti_windup=True)
        pos += out * 5 * 0.02
        if i == 100:
            target = 0.0  # flip target -> error changes sign -> integral resets
    print("final:", round(pos, 1), "| integral resets:", pid.reset_count)


def ex6():
    robot = Robot()
    pid = MyPIDF(0.03, 0.0, 0.004, 0.0)
    for _ in range(300):
        out = pid.update(robot.imu.get_heading(), 90.0)
        out = max(-0.6, min(0.6, out))
        robot.set_drive_power(0, 0, out)
        robot.step(0.02)
    robot.set_drive_power(0, 0, 0)
    print("heading settled:", round(robot.imu.get_heading(), 2))


def ex7():
    pid = MyPIDF(0.02, 0.0, 0.00045, 0.0)
    ticks, target = 0.0, 960.0
    for i in range(200):
        out = pid.update(ticks, target)
        ticks += out * 200 * 0.02   # motor moves proportional to power
        if i % 20 == 0:
            print(f"  loop {i:3d}: ticks={ticks:7.1f}")
    print("lift settled:", round(ticks, 1))


def ex8():
    for kf in (0.0, 0.125):
        pid = MyPIDF(0.02, 0.0, 0.00045, kf)
        ticks, target = 0.0, 960.0
        for _ in range(300):
            out = pid.update(ticks, target)
            ticks += out * 200 * 0.02
            ticks -= 5 * 0.02 * 200 * 0.0  # gravity applied below
            ticks -= 1.0                    # constant sag each loop
        print(f"kf={kf}: settled at {ticks:7.1f} (target 960)")
    # kf=0 settles below target; kf>0 pushes up to beat the sag.


def ex9():
    real = PIDFController(0.02, 0.0, 0.00045, 0.0, rot=False)
    mine = MyPIDF(0.02, 0.0, 0.00045, 0.0)
    rp = mp = 0.0
    for _ in range(150):
        rp += real.update(rp, 960.0, dt=0.02) * 200 * 0.02  # fixed dt -> deterministic
        mp += mine.update(mp, 960.0) * 200 * 0.02
    print("real port:", round(rp, 1), "| MyPIDF:", round(mp, 1))


def ex10():
    # Juice's real gains vs a hand-tuned improvement.
    def settle(kp, ki, kd, kf):
        pid = MyPIDF(kp, ki, kd, kf)
        ticks, peak = 0.0, 0.0
        for _ in range(200):
            ticks += pid.update(ticks, 960.0) * 200 * 0.02
            peak = max(peak, ticks)
        return ticks, peak - 960
    base = settle(0.02, 0.0, 0.00045, 0.125)
    tuned = settle(0.02, 0.0, 0.0012, 0.125)  # more D -> less overshoot
    print("Juice gains -> final %.1f overshoot %.1f" % base)
    print("more D      -> final %.1f overshoot %.1f" % tuned)
    # More derivative damps the approach: lower overshoot, still reaches target.


if __name__ == "__main__":
    for name in ["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10"]:
        print(name); globals()[name]()
