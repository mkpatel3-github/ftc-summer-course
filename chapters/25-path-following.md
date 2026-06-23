# Chapter 25 — Path Following: Pure Pursuit (and a Peek at GVF)

> Goal: stop driving to *one* pose and start following a *whole path*. You'll build pure
> pursuit — "always steer toward a point a little way ahead of you on the path" — the simplest
> follower that real robots actually use. Then we'll show how KookyBotz's `GVFPathFollower`
> takes the same idea further. This is the last localization-and-motion piece: you can now
> *find* where you are (Ch 19–23) and *drive a curve* to where you want to be.

## From "drive to a pose" to "follow a path"

In Chapter 16 you used `DriveToPoseAction`: aim at a single target and stop. That's great for
one waypoint. But a real autonomous routine isn't one point — it's a **path**: leave the wall,
curve around the truss, arrive at the basket facing the right way. If you chain a dozen
"drive to pose" calls, the robot stops dead at every waypoint — slow and jerky.

A **path follower** treats the waypoints as one continuous route and drives *through* them
without stopping. The question is: at any instant, which way should I steer?

## Pure pursuit: chase a carrot on a string

The trick is almost embarrassingly simple. Imagine a carrot dangling a fixed distance ahead of
you *on the path*. You always drive straight at the carrot. As you move, the carrot slides
forward along the path, so you naturally curve to follow it.

That fixed distance is the **lookahead**. Two steps each loop:

1. **Project** onto the path — find the waypoint nearest the robot. That's "where I am on the
   route."
2. **Look ahead** — walk forward along the path from that projection to the first point at least
   `lookahead` inches away. That's the carrot. Steer toward it.

```python
from ftcsim import Robot, Path, PurePursuitFollower, run_for

robot = Robot()
path = Path([(0, 0), (10, 0), (20, 10), (20, 20)])   # an L-ish curve
follower = PurePursuitFollower(robot, path, lookahead=8.0)

def loop(t):
    follower.run()      # steers toward the lookahead point; returns False when arrived
run_for(robot, 5.0, loop)
```

`follower.run()` does exactly the two steps above, converts the direction-to-carrot into
mecanum stick values (the same field→robot mapping as `DriveToPoseAction`), and returns `False`
once the robot is within `tol` of the path's end.

## The one knob that matters: lookahead distance

Lookahead is the whole personality of the follower:

- **Small** — the carrot sits just ahead of you, so you steer to hug the path *tightly*. Great
  accuracy. But on a *real* robot, momentum means you overshoot the close carrot and **wobble**
  back and forth across the path (oscillation) — the same instability a too-high `kp` causes.
- **Big** — the carrot is way down the road. You aim past the corners and cut them, drifting
  *inside* curves and missing tight waypoints. Smooth, but sloppy.
- **Just right** — close enough to track accurately, far enough that the path stays smooth.

So lookahead trades **accuracy vs. smoothness**, picked by testing — exactly like tuning `kp`
in Chapter 13. (Our sim has no momentum, so a tiny lookahead just tracks very tightly rather
than wobbling; we'll *demonstrate* the corner-cutting from a big lookahead, and you'll keep the
real-robot oscillation in mind as the reason not to go too small on actual hardware.)

## Java bridge — the same idea, the pro version (KookyBotz GVF)

Pure pursuit picks a *discrete waypoint* to chase. KookyBotz's `GVFPathFollower` ("Guided
Vector Field") does the continuous-math version: instead of one carrot, it builds a **vector
field** that points toward the path everywhere on the floor.

```java
// GVFPathFollower, in spirit:
// 1. Project the robot onto the spline (continuous, not a discrete waypoint).
Point projected = path.project(robotPose);
// 2. TANGENT vector: the direction the path is heading right here (drives you ALONG it).
Vector tangent = path.tangentAt(projected);
// 3. NORMAL vector: points from the robot back ONTO the path (corrects drift).
Vector normal  = path.errorVector(robotPose);   // robot -> nearest path point
// 4. Blend them: mostly follow the tangent, but bend toward the path by how far off you are.
Vector heading = tangent.plus(normal.times(kCorrection));
// 5. Curvature-limited speed: slow down where the path bends hard so you don't fly off.
double speed = maxSpeed / (1 + kCurvature * path.curvatureAt(projected));
drive.setVector(heading.normalize().times(speed));
```

Notice the shape is identical to pure pursuit — *project, then steer along the path while
correcting back onto it.* GVF just uses smooth tangent/normal vectors instead of a single
lookahead point, which lets it slow down for sharp curves (step 5). Pure pursuit is the version
you can build and debug in an afternoon; GVF is what you reach for when you need to scream
through a complex spline at full speed. **Same idea, more math.**

---

## Exercises

Use `from ftcsim import (Robot, Path, PurePursuitFollower, run_for)`. A `Path([(x,y), ...])`
holds waypoints; `path.closest_point(x, y)` returns `(index, distance)`, `path.lookahead_point(
x, y, lookahead)` returns the carrot `(x, y)`, and `path.end()` is the last point. A
`PurePursuitFollower(robot, path, lookahead=8.0, kp=0.08, tol=2.0)` has `.run()` which steers
one loop and returns `True` while going, `False` once arrived.

**1. Build a path, find the projection.** Make a `Path` with 4–5 waypoints in a gentle curve.
Put the robot at the start and print `path.closest_point(robot.x, robot.y)`. Move the robot a
few inches down the path by hand (`robot.x = ...`) and print it again. Show the projection
index advances as you move along the path.

**2. See the carrot move.** With the robot at the start, print `path.lookahead_point(robot.x,
robot.y, 8.0)`. Nudge the robot forward a few times and print the lookahead each time. Show the
carrot slides forward along the path as you advance. (This is pure pursuit's whole idea in one
print.)

**3. Follow a straight line.** Make a `Path` from `(0,0)` to `(30,0)`. Run a
`PurePursuitFollower` in a `run_for` loop until `.run()` returns `False`. Print the robot's
final `(x, y)`. Show it arrives near `(30, 0)`.

**4. Follow a curve.** Make an L-shaped path like `[(0,0),(10,0),(20,10),(20,20)]`. Follow it
and print the final pose. Show the robot ends near `(20, 20)` — it tracked the corner without
stopping at the middle waypoint.

**5. Small lookahead tracks tight.** Follow the curve from exercise 4 with `lookahead=2.0`.
Every few loops, print the robot's distance from the *nearest* path point
(`path.closest_point(...)[1]`). Show the distance stays small — the robot hugs the path
closely. In a comment, explain why a small lookahead tracks tightly here, *and* why on a real
robot (with momentum) too small a value would instead make it overshoot and wobble.

**6. Lookahead too big cuts corners.** Follow the same curve with `lookahead=20.0`. Track the
max distance the robot ever gets from the path. Show it drifts *inside* the corner (large max
distance) compared to a medium lookahead. In a comment: big lookahead = smooth but sloppy.

**7. Tune the lookahead.** Run the curve with `lookahead` = 2, 6, 10, 16. For each, record the
total path-tracking error (sum of `closest_point` distance each loop). Print a little table.
Show error grows as lookahead grows (corner-cutting). Pick the value that best trades accuracy
against smoothness — that's your tuned lookahead, same idea as tuning `kp`.

**8. Detect arrival.** Use the `.run()` return value as your loop condition: keep calling it
until it returns `False`, counting loops. Print the loop count and confirm the final distance to
`path.end()` is within `tol`. Show the follower stops itself — you don't hand-pick a timeout.

**9. A two-leg autonomous.** Chain two paths: follow path A to its end, then follow path B from
there (build a second `PurePursuitFollower`). Print the pose after each leg. This is how an auto
routine strings path segments — like RoadRunner's `.splineTo(...).splineTo(...)`.

**10. Pure pursuit vs. GVF, in your own words.** Follow a path and, each loop, print both the
**tangent direction** (angle from the current closest point to the *next* waypoint) and the
**error distance** (`closest_point` distance). Watch how the follower's steering is really
"go along the path (tangent) + pull back onto it (error)." In a comment, map your two numbers to
the `tangent` and `normal` vectors in the KookyBotz GVF bridge above, and say in one sentence
what GVF adds that pure pursuit doesn't (curvature-limited speed).

## Java bridge

```java
// A RoadRunner-style follower call, for contrast -- a whole trajectory, one await:
Actions.runBlocking(
    drive.actionBuilder(startPose)
         .splineTo(new Vector2d(20, 20), Math.toRadians(90))
         .splineTo(new Vector2d(40, 10), Math.toRadians(0))
         .build());
// Under the hood that's the same project-and-steer loop you just wrote -- RoadRunner
// uses a feedforward+feedback controller along the spline, KookyBotz uses GVF, you used
// pure pursuit. All three answer the same question: "which way do I steer right now?"
```

You've now built the full motion-and-localization stack: dead reckoning, vision, fusion,
latency-correct relocalization (Ch 19–23), declarative TeleOp (Ch 24), and path following
(this chapter). That's the architecture a top FTC team actually ships.

➡️ Solutions: [`solutions/25_solution.py`](../solutions/25_solution.py)
