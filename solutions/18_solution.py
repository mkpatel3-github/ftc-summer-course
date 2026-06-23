"""Chapter 18 solutions - Loop Time & Bulk Reads."""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
from ftcsim import Robot, LynxModule, reset_hw_reads, hw_reads


def _encoders(r):
    return (r.front_left, r.front_right, r.back_left, r.back_right)


def ex1():
    r = Robot()
    reset_hw_reads()
    for m in _encoders(r):
        m.get_encoder_value()
    print("naive single reads:", hw_reads())   # 4


def ex2():
    r = Robot()
    reset_hw_reads()
    for _ in range(10):
        for m in _encoders(r):
            m.get_encoder_value()
    print("naive loop reads:", hw_reads())      # 40


def ex3():
    r = Robot()
    r.hub.set_bulk_caching_mode(LynxModule.MANUAL)
    reset_hw_reads()
    r.hub.clear_bulk_cache()
    for m in _encoders(r):
        m.get_encoder_value()
    print("manual one-clear reads:", hw_reads())  # 1


def ex4():
    r = Robot()
    r.hub.set_bulk_caching_mode(LynxModule.MANUAL)
    reset_hw_reads()
    for _ in range(10):
        r.hub.clear_bulk_cache()
        for m in _encoders(r):
            m.get_encoder_value()
    total = hw_reads()
    print("manual loop reads:", total, "speedup vs 40:", 40 / total, "x")


def ex5():
    r = Robot()
    r.hub.set_bulk_caching_mode(LynxModule.MANUAL)
    r.hub.clear_bulk_cache()            # cleared ONCE before the loop
    for i in range(5):
        run_step(r)
        val = r.front_left.get_encoder_value()
        print(f"loop {i}: encoder={val:.1f} (STALE -- never refreshed)")
    # #1 bulk-read bug: in MANUAL mode the cache only updates on clear_bulk_cache.
    # Forget to clear at the top of each loop and every read returns the same old
    # snapshot forever -- your PID reacts to a frozen world.


def run_step(r):
    r.set_drive_power(0, 1.0, 0)
    r.step(0.02)


def ex6():
    r = Robot()
    r.hub.set_bulk_caching_mode(LynxModule.AUTO)
    reset_hw_reads()
    for m in _encoders(r):
        m.get_encoder_value()
    print("AUTO reads:", hw_reads())
    # AUTO auto-bulk-reads on the first read of a loop (simple, no clear call),
    # but reading the SAME sensor twice can trigger a second bulk read. MANUAL
    # needs the explicit clear but is fully predictable -- what top teams pick.


def ex7():
    r = Robot()
    r.hub.set_bulk_caching_mode(LynxModule.MANUAL)
    snapshot = {}

    def read():
        r.hub.clear_bulk_cache()
        snapshot["fl"] = r.front_left.get_encoder_value()
        snapshot["fr"] = r.front_right.get_encoder_value()
        snapshot["bl"] = r.back_left.get_encoder_value()
        snapshot["br"] = r.back_right.get_encoder_value()

    def decide():
        return sum(snapshot.values()) / 4.0

    def write():
        r.set_drive_power(0, 1.0, 0)

    avg = 0.0
    for _ in range(25):
        read()
        avg = decide()
        write()
        r.step(0.02)
    print("final avg ticks:", round(avg, 1))


def ex8():
    r = Robot()
    # Danger: read the same sensor at start and end of the loop body -- step()
    # ran in between, so they differ. A PID using both would mix two worlds.
    r.set_drive_power(0, 1.0, 0)
    start = r.front_left.get_encoder_value()
    r.step(0.02)
    end = r.front_left.get_encoder_value()
    print("mid-loop reads differ:", round(start, 1), "vs", round(end, 1))

    # Read-phase version: one consistent snapshot used for the whole loop.
    r.hub.set_bulk_caching_mode(LynxModule.MANUAL)
    r.hub.clear_bulk_cache()
    snap = r.front_left.get_encoder_value()
    use_a = snap
    use_b = snap
    print("snapshot consistent:", round(use_a, 1), "==", round(use_b, 1))
    # A PID must compare like-for-like; a value that changes mid-calc corrupts
    # the derivative term and makes the controller chase ghosts.


def ex9():
    cost_ms = 2
    for label, reads in (("6 naive", 6), ("1 bulk", 1)):
        ms = reads * cost_ms
        hz = 1000 / ms
        print(f"{label}: {ms} ms/loop -> {hz:.0f} Hz")


class RobotHardware:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = RobotHardware()
        return cls._instance

    def __init__(self):
        self.robot = Robot()
        self.robot.hub.set_bulk_caching_mode(LynxModule.MANUAL)
        self.snapshot = {}

    def clear_bulk_cache(self):
        self.robot.hub.clear_bulk_cache()

    def read(self):
        self.snapshot = {
            "fl": self.robot.front_left.get_encoder_value(),
            "fr": self.robot.front_right.get_encoder_value(),
        }

    def periodic(self):
        self.avg = sum(self.snapshot.values()) / len(self.snapshot)

    def write(self):
        self.robot.set_drive_power(0, 1.0, 0)

    def run_loop(self):
        self.clear_bulk_cache()
        self.read()
        self.periodic()
        self.write()
        self.robot.step(0.02)


def ex10():
    RobotHardware._instance = None      # fresh for this demo
    hw = RobotHardware.get_instance()
    for _ in range(20):
        hw.run_loop()
    print("subsystem avg ticks:", round(hw.avg, 1))
    # Maps to KookyBotz Duo.java: scheduler.run(); robot.clearBulkCache();
    # robot.read(); robot.periodic(); robot.write(). One bulk read, one
    # consistent snapshot, all writes batched at the end.


if __name__ == "__main__":
    for name in ["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10"]:
        print("\n===", name, "===")
        globals()[name]()
