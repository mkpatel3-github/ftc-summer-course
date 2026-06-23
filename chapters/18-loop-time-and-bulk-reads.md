# Chapter 18 — Loop Time & Bulk Reads

> Goal: make your robot's brain run faster — not by buying hardware, but by reading sensors
> smartly. This is the highest effort-to-impact trick in competitive FTC: a ~10-line change
> that can **double your loop frequency**. Every top team does it (ACME, Solvers, KookyBotz).

## Why loop time matters

A robot's code runs in a loop: read sensors → decide → move motors → repeat. How many times
per second that loop runs is your **loop frequency**. A PID controller (Chapter 7) reacts
*per loop*; field-centric driving recomputes *per loop*; odometry updates *per loop*. A slow
loop means a sluggish, jittery, less accurate robot. Fast loop = crisp control.

## The hidden cost: every read is a phone call

Here's the thing beginners miss: when you call `motor.getEncoderValue()`, the Control Hub
sends a request over a data bus to the motor controller and waits for the answer. That's a
**transaction** — and it takes real time (a few milliseconds). If your loop reads 4 drive
encoders + 2 lift encoders separately, that's **6 phone calls every loop**, and they add up
fast.

Our simulator counts these for you:

```python
from ftcsim import Robot, reset_hw_reads, hw_reads
robot = Robot()
reset_hw_reads()
robot.front_left.get_encoder_value()
robot.front_right.get_encoder_value()
print(hw_reads())   # -> 2 separate reads
```

## The fix: bulk reads

A REV hub can read **all** its sensors in **one** transaction — one phone call that returns
everything. You turn this on once and then refresh the cache once per loop:

```python
from ftcsim import LynxModule
robot.hub.set_bulk_caching_mode(LynxModule.MANUAL)
# ...each loop:
robot.hub.clear_bulk_cache()     # ONE bulk read refreshes the whole cache
fl = robot.front_left.get_encoder_value()   # free -- served from cache
fr = robot.front_right.get_encoder_value()  # free
# ...all 4 drive encoders cost a TOTAL of 1 read, not 4.
```

There are two modes, mirroring the real SDK:

- **AUTO** — the hub auto-bulk-reads; the first read of each loop is bulk, repeats are free.
  Simple, but a subtle gotcha: reading the *same* sensor twice can trigger a second bulk read.
- **MANUAL** — *you* call `clearBulkCache()` once at the top of the loop. Every read until
  the next clear is free. More control, no surprises — what most top teams use.

## Java bridge (the real 3 lines)

```java
// once, at init:
for (LynxModule hub : hardwareMap.getAll(LynxModule.class)) {
    hub.setBulkCachingMode(LynxModule.BulkCachingMode.MANUAL);
}
// top of every loop:
for (LynxModule hub : hardwareMap.getAll(LynxModule.class)) hub.clearBulkCache();
```

KookyBotz wire this into their loop as `robot.clearBulkCache(); robot.read(); ...`. That
brings us to the second half of this chapter: loop *structure*.

## The read → decide → write discipline

KookyBotz structure every loop in three clean phases:

1. **read** — pull *all* sensor values once (after one bulk clear), store them.
2. **periodic / decide** — do all your math on those stored values.
3. **write** — send *all* motor/servo commands once.

Why? It guarantees every calculation in one loop uses a **consistent snapshot** of the
world, and it makes the single-bulk-read optimization natural. Mixing reads and writes
randomly through the loop is how you accidentally read a sensor 3 times.

---

## Exercises

Use `from ftcsim import Robot, LynxModule, reset_hw_reads, hw_reads`. The robot's hub is
`robot.hub`. `reset_hw_reads()` zeroes the counter; `hw_reads()` returns it. Encoder reads
go through the counter unless the cache is serving them.

**1. Count a naive read.** Reset the counter, read all 4 drive encoders separately
(`front_left`, `front_right`, `back_left`, `back_right`), and print `hw_reads()`. (Expect 4.)

**2. Count a naive loop.** Reset, then in a `for` loop of 10 "loops" read all 4 encoders
each time. Print the total. (Expect 40 — this is what a slow robot does.)

**3. Turn on MANUAL caching.** Set `robot.hub.set_bulk_caching_mode(LynxModule.MANUAL)`.
Reset the counter. Call `robot.hub.clear_bulk_cache()` once, then read all 4 encoders. Print
`hw_reads()`. (Expect 1 — one bulk read served all four.)

**4. The big comparison.** Redo exercise 2 but with MANUAL caching and a
`clear_bulk_cache()` at the top of each of the 10 loops. Print the total and the speedup
factor vs exercise 2. (Expect 10 reads → 4× fewer.)

**5. Forgot to clear.** With MANUAL mode on, run 5 loops but *don't* call
`clear_bulk_cache()` at all (only once before the loop). Read an encoder each loop and watch
the value go **stale** (it never updates). In a comment: this is the #1 bulk-read bug —
explain it.

**6. AUTO mode.** Switch to `LynxModule.AUTO`, reset, and read the 4 encoders once. Compare
the read count to MANUAL. In a comment, state the trade-off between AUTO and MANUAL.

**7. read → decide → write.** Restructure a drive loop into three explicit phases per tick:
a `read()` that snapshots all 4 encoders into a dict, a `decide()` that computes the average,
and a `write()` that sets drive power. Run 25 loops driving forward; print the final average
tick count. Keep reads only in `read()`.

**8. Consistent snapshot.** Demonstrate the danger of reading mid-loop: in one version read
`front_left` at the start *and* end of the loop body and show they can differ (because
`robot.step` ran). Then show the read-phase version uses one consistent value. Explain why
that matters for a PID.

**9. Loop-time budget.** Pretend each real hardware read costs 2 ms. Compute and print the
estimated loop time (ms) and loop frequency (Hz) for: (a) 6 naive reads per loop, (b) 1 bulk
read per loop. (Just arithmetic: time = reads × 2 ms; Hz = 1000 / time.) Show the frequency
jump.

**10. Wire it into a real subsystem.** Take your Chapter 17 `RobotHardware` singleton and
add `clear_bulk_cache()`, `read()`, `periodic()`, `write()` methods. Write a `run_loop()`
that calls them in order each tick. In a comment, map each method to what KookyBotz's
`Duo.java` loop does (`scheduler.run(); robot.clearBulkCache(); robot.read();
robot.periodic(); robot.write();`).

## Java bridge

```java
// KookyBotz's real loop body (opmode/teleop/Duo.java), in spirit:
while (opModeIsActive()) {
    scheduler.run();          // run scheduled commands
    robot.clearBulkCache();   // ONE bulk read for the whole loop
    robot.read();             // snapshot every sensor
    robot.periodic();         // do all the math
    robot.write();            // send every motor/servo command once
}
```

That's the structure under nearly every high-level FTC codebase. You now know why it's shaped
that way.

➡️ Solutions: [`solutions/18_solution.py`](../solutions/18_solution.py)
