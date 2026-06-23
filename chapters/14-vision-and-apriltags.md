# Chapter 14 — Vision & AprilTags

> Goal: let the robot *see*. Use a camera that detects **AprilTags** (the QR-code-looking
> markers on the FTC field) to figure out exactly where the robot is — and to find game
> pieces by color. This is Juice's `CVMaster.java` (Limelight3A + VisionPortal), made
> approachable.

## Two jobs a camera does in FTC

**1. Localization — "where am I?"** AprilTags sit at *known* spots on the field perimeter.
If the camera sees a tag and measures how far away it is, the robot can work backward to
its own position. This is more accurate than odometry and **doesn't drift**, which is why
Juice fuses the two (next chapter).

**2. Detection — "where's the game piece?"** A color/blob pipeline finds samples by color
(red/blue/yellow). Juice's `CVMaster.java` uses a `ColorBlobLocatorProcessor` for exactly
this, and you fixed the color logic by hand back in Chapter 5 — now a camera does it.

## The localization math (it's just subtraction)

If a tag is at field position `(tag_x, tag_y)` and the camera reports the tag is `(dx, dy)`
*away from the robot*, then:

```
robot_x = tag_x - dx
robot_y = tag_y - dy
```

That's it. Real cameras give range + bearing and you do a little trig, but the idea is
this subtraction. Our sim hands you the offset so you can focus on the concept:

```python
field = Field().add_standard_tags()      # puts tags on the 4 walls
robot = Robot(field=field, start_x=20, start_y=10)
pose = robot.camera.localize()           # -> Pose2d from the nearest visible tag
```

`robot.camera.get_detections()` returns a list of `(tag, dx, dy)` for every tag in range.
A tag too far away isn't seen — just like a real camera.

## Why teams love it

AprilTag localization is **absolute**: it tells you where you *are*, not where you *think*
you went. Combined with odometry's smooth, every-loop updates, you get the best of both —
that fusion is Juice's `KalmanDrive`. Modern tools: FTC's **VisionPortal** (built into the
SDK), **EasyOpenCV**, and the **Limelight 3A** smart camera (which Juice uses) with
**MegaTag2**.

---

## Exercises

Set up tags with `field = Field().add_standard_tags()` then `robot = Robot(field=field,
start_x=..., start_y=...)`. Use `robot.camera.localize()` and
`robot.camera.get_detections()`. Tag IDs are 11 (top), 12 (right), 13 (bottom), 14 (left).

**1. See a tag.** Put the robot near the right wall (`start_x=60, start_y=0`) and print
`robot.camera.get_detections()`. Confirm at least one tag is visible and print its id.

**2. Localize.** From the same spot, print `robot.camera.localize()`. Compare it to the
robot's true pose (`robot.get_pose()`). They should match (perfect sim camera).

**3. Out of range.** Put the robot at the center (`0,0`) with the camera's `max_range`
small: `robot.camera.max_range = 10`. Show `localize()` returns `None`. Explain in a
comment what your code should do when the camera sees nothing.

**4. Localize from the math yourself.** Don't call `localize()`. Get one detection
`(tag, dx, dy)` from `get_detections()` and compute `robot_x = tag.x - dx`,
`robot_y = tag.y - dy` by hand. Confirm it matches the true pose.

**5. Nearest tag wins.** Place the robot where two tags are in range (try `start_x=50,
start_y=50` with a large `max_range`). Print all detections and their distances, then show
`localize()` picked the closest one. Why prefer the closest? (Comment.)

**6. Camera vs odometry.** Drive forward 2s. Print both `robot.odometry.get_pose()` and
`robot.camera.localize()`. With a perfect sim they agree — in a comment, say which one you
trust more after a 30-second match, and why (drift!).

**7. Find the sample by color.** Reuse Chapter 5: place a colored sample on the field
(`field.sample_x`, `field.sample_y`, `field.sample_color`), drive over it, and use the
color sensor to report its color. In a comment, note that `CVMaster.java` does this with a
camera blob detector instead of a contact sensor — what's the advantage of seeing it from
far away?

**8. Re-localize after a "bump."** Drive forward 2s, then *teleport* the robot (simulate a
defender shoving it: set `robot.x += 8`). Show odometry still reports the old-ish path but
`camera.localize()` immediately reports the true, bumped position. This is the headline
benefit of vision.

**9. A vision-corrected stop.** Drive toward the right wall. Each loop, if a tag is
visible, use `camera.localize()` to check distance to `Pose2d(60, 0)`; stop within 2".
Print the final pose. (Vision closing the loop on position.)

**10. Design a vision plan.** In a comment block, write the plan Juice's `CVMaster` follows
at a high level: when to run the AprilTag pipeline (localization) vs the color-blob
pipeline (find sample), and why you wouldn't run heavy vision every single loop (hint:
loop time — Chapter 15). No code; this is real strategy.

## Java bridge (Juice's CVMaster idea)

```java
// VisionPortal with an AprilTag processor (SDK built-in):
AprilTagProcessor aprilTag = new AprilTagProcessor.Builder().build();
VisionPortal portal = new VisionPortal.Builder()
        .setCamera(hardwareMap.get(WebcamName.class, "Webcam 1"))
        .addProcessor(aprilTag)
        .build();

for (AprilTagDetection d : aprilTag.getDetections()) {
    if (d.metadata != null) {
        // d.ftcPose gives range/bearing; the SDK can return a field pose directly
        telemetry.addData("tag", d.id);
        telemetry.addData("x", d.robotPose.getPosition().x);
    }
}
```

Juice goes a step further with a **Limelight3A** (`CVMaster.java`) which runs the tag
pipeline on its own processor, freeing the Control Hub. Same concept, faster camera.

➡️ Solutions: [`solutions/14_solution.py`](../solutions/14_solution.py)
