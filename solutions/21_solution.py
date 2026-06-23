"""Chapter 21 solutions - Sensor Fusion & the Kalman Filter."""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
from ftcsim import Robot, Field, KalmanFilter, run_for


class MyKalman:
    def __init__(self, q, r):
        self.Q, self.R = q, r
        self.x = 0.0
        self.p = 1.0

    def update(self, model_delta, measurement):
        self.x += model_delta          # predict
        self.p += self.Q
        k = self.p / (self.p + self.R)  # Kalman gain
        self.x += k * (measurement - self.x)   # correct toward sensor
        self.p *= (1 - k)
        return self.x


def ex1():
    mine = MyKalman(0.1, 2.0)
    print("MyKalman:", round(mine.update(5, 4), 4))
    ref = KalmanFilter(q=0.1, r=2.0)
    ref.set_state(0.0)
    print("sim KalmanFilter:", round(ref.update(model_delta=5, measurement=4), 4))
    # same Q/R, same math -> same number.


def ex2():
    big_r = MyKalman(0.1, 1000.0)       # trust sensor little
    small_r = MyKalman(0.1, 0.01)       # trust sensor a lot
    print("large R (stay smooth):", round(big_r.update(10, 0), 3))
    print("small R (snap to cam):", round(small_r.update(10, 0), 3))
    # Large R -> tiny gain -> output stays near the predicted 10 (odometry-like).
    # Small R -> gain ~1 -> output jumps to the measurement 0 (camera-like).


def ex3():
    kf = MyKalman(0.01, 1.0)
    readings = [48, 53, 49, 51, 47, 52, 50, 49, 51, 50]
    kf.x = readings[0]                  # seed at first reading so we SEE smoothing
    for m in readings:
        est = kf.update(0, m)           # model_delta=0: value isn't moving
        print(f"meas={m} -> estimate={est:.2f}")
    # the noisy inputs bounce 47..53 but the estimate stays near 50 and barely
    # moves -- the filter is smoothing.


def ex4():
    f = Field()
    r = Robot(field=f)
    r.odometry.drift_per_read = 0.05
    run_for(r, 2.0, lambda t: r.set_drive_power(0, 1.0, 0))
    odo_x = r.odometry.get_pose().x
    print(f"odometry x={odo_x:.2f}  true x={r.x:.2f}  drift={odo_x - r.x:.2f}")
    # accumulated drift makes odometry read too high.


def ex5():
    f = Field().add_standard_tags()
    r = Robot(field=f, start_x=10, start_y=10)
    r.camera.noise = 1.0
    for _ in range(5):
        print("camera x:", round(r.camera.localize().x, 3))
    # absolute (centered on truth 10) but jumps around each read.


def ex6():
    f = Field().add_standard_tags()
    r = Robot(field=f, start_x=10, start_y=10)
    r.odometry.drift_per_read = 0.05
    r.camera.noise = 1.0
    run_for(r, 1.0, lambda t: r.set_drive_power(0, 1.0, 0))

    kf = KalmanFilter(q=0.1, r=2.0)
    kf.set_state(r.odometry.get_pose().x)
    model_delta = 0.0                    # one step, no new motion this tick
    measurement = r.camera.localize().x
    print("fused x:", round(kf.update(model_delta, measurement), 3))


def ex7():
    f = Field().add_standard_tags()
    r = Robot(field=f)
    r.odometry.drift_per_read = 0.05
    r.camera.noise = 1.0

    kf = KalmanFilter(q=0.1, r=2.0)
    kf.set_state(0.0)
    last_x = r.odometry.get_pose().x
    state = {"last": last_x}

    def loop(t):
        cur = r.odometry.get_pose().x
        delta = cur - state["last"]
        state["last"] = cur
        meas = r.camera.localize().x
        kf.update(delta, meas)
        r.set_drive_power(0, 1.0, 0)

    run_for(r, 2.0, loop)
    print(f"fused x={kf.x:.2f}  odometry x={r.odometry.get_pose().x:.2f}  true x={r.x:.2f}")
    # fused is closer to true than the drifting odometry.


def _drive_and_fuse(q, r_noise):
    f = Field().add_standard_tags()
    r = Robot(field=f)
    r.odometry.drift_per_read = 0.05
    r.camera.noise = 1.0
    kf = KalmanFilter(q=q, r=r_noise)
    kf.set_state(0.0)
    state = {"last": r.odometry.get_pose().x}

    def loop(t):
        cur = r.odometry.get_pose().x
        delta = cur - state["last"]
        state["last"] = cur
        kf.update(delta, r.camera.localize().x)
        r.set_drive_power(0, 1.0, 0)

    run_for(r, 2.0, loop)
    return abs(kf.x - r.x)


def ex8():
    for label, q, rn in (("trust-camera", 1.0, 0.1),
                         ("trust-odometry", 0.001, 50.0),
                         ("balanced", 0.1, 2.0)):
        print(f"{label}: final error={_drive_and_fuse(q, rn):.3f}")
    # Q/R is to a Kalman filter what kP/kD is to a PID: knobs that trade
    # responsiveness against smoothness, tuned by watching the resulting error.
    # Balanced is usually smoothest AND accurate.


def ex9():
    f = Field()                          # NO tags placed for part of the drive
    r = Robot(field=f)
    r.odometry.drift_per_read = 0.05
    r.camera.noise = 1.0
    kf = KalmanFilter(q=0.1, r=2.0)
    kf.set_state(0.0)
    state = {"last": r.odometry.get_pose().x}

    def loop(t):
        cur = r.odometry.get_pose().x
        delta = cur - state["last"]
        state["last"] = cur
        # tag visible only in the middle third of the drive:
        if 0.7 < t < 1.3:
            f.april_tags = Field().add_standard_tags().april_tags
        else:
            f.april_tags = []
        meas = r.camera.localize()
        if meas is None:
            kf.x += delta                # predict only -- coast on odometry
            kf.p += kf.Q
        else:
            kf.update(delta, meas.x)
        r.set_drive_power(0, 1.0, 0)

    run_for(r, 2.0, loop)
    print(f"fused x after blackout+resnap={kf.x:.2f}  true x={r.x:.2f}")
    # during the blackout it coasts on odometry; when the tag returns it re-snaps.


def ex10():
    f = Field().add_standard_tags()
    r = Robot(field=f)
    r.odometry.drift_per_read = 0.05
    r.camera.noise = 1.0
    kfx = KalmanFilter(q=0.1, r=2.0); kfx.set_state(0.0)
    kfy = KalmanFilter(q=0.1, r=2.0); kfy.set_state(0.0)
    p0 = r.odometry.get_pose()
    state = {"lx": p0.x, "ly": p0.y}

    def loop(t):
        p = r.odometry.get_pose()
        dx, dy = p.x - state["lx"], p.y - state["ly"]
        state["lx"], state["ly"] = p.x, p.y
        cam = r.camera.localize()
        if cam is not None:
            kfx.update(dx, cam.x)
            kfy.update(dy, cam.y)
        # forward 1s, then strafe 1s
        if t < 1.0:
            r.set_drive_power(0, 1.0, 0)
        else:
            r.set_drive_power(1.0, 0, 0)

    run_for(r, 2.0, loop)
    print(f"fused (x,y)=({kfx.x:.1f},{kfy.x:.1f})  true (x,y)=({r.x:.1f},{r.y:.1f})")
    # Two independent 1-D filters compose a 2-D pose -- exactly j5155's
    # Vector2dKalmanFilter, and what keeps Juice's KalmanDrive honest all match.


if __name__ == "__main__":
    for name in ["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10"]:
        print("\n===", name, "===")
        globals()[name]()
