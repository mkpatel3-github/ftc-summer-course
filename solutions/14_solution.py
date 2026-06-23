"""Chapter 14 solutions - Vision & AprilTags."""
import sys, os, math
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
from ftcsim import Robot, Field, Pose2d, run_for


def ex1():
    field = Field().add_standard_tags()
    r = Robot(field=field, start_x=60, start_y=0)
    dets = r.camera.get_detections()
    print("visible tags:", [t.id for (t, dx, dy) in dets])


def ex2():
    field = Field().add_standard_tags()
    r = Robot(field=field, start_x=60, start_y=0)
    print("localize :", r.camera.localize())
    print("true pose:", r.get_pose())


def ex3():
    field = Field().add_standard_tags()
    r = Robot(field=field, start_x=0, start_y=0)
    r.camera.max_range = 10
    print("localize with tiny range:", r.camera.localize())
    # When the camera sees nothing, fall back to odometry for this loop and
    # keep driving; never blindly trust a None pose.


def ex4():
    field = Field().add_standard_tags()
    r = Robot(field=field, start_x=60, start_y=0)
    tag, dx, dy = r.camera.get_detections()[0]
    print(f"by hand: x={tag.x - dx:.1f}, y={tag.y - dy:.1f}")
    print("true   :", r.get_pose())


def ex5():
    field = Field().add_standard_tags()
    r = Robot(field=field, start_x=50, start_y=50)
    r.camera.max_range = 200
    for tag, dx, dy in r.camera.get_detections():
        print(f"tag {tag.id}: dist={math.hypot(dx, dy):.1f}")
    print("localize picked nearest ->", r.camera.localize())
    # Closest tag = biggest in frame = least angular error = most accurate.


def ex6():
    field = Field().add_standard_tags()
    r = Robot(field=field, start_x=0, start_y=0)
    r.camera.max_range = 200
    run_for(r, 2.0, lambda t: r.set_drive_power(0, 1, 0))
    print("odometry:", r.odometry.get_pose())
    print("camera  :", r.camera.localize())
    # After 30s odometry has drifted; the camera's absolute fix is trusted more.


def ex7():
    field = Field().add_standard_tags()
    field.sample_x, field.sample_y, field.sample_color = 30, 0, "BLUE"
    r = Robot(field=field, start_x=0, start_y=0)
    seen = [None]

    def loop(t):
        r.set_drive_power(0, 1, 0)  # forward (+x) toward the sample at (30,0)
        if r.color.blue() > 0.5:
            seen[0] = "BLUE"
        elif r.color.red() > 0.5:
            seen[0] = "RED"
    run_for(r, 1.0, loop)
    print("sample color read while driving over it:", seen[0])
    # A camera blob detector sees it from across the field, so you can plan a
    # path to it instead of having to already be on top of it.


def ex8():
    field = Field().add_standard_tags()
    r = Robot(field=field, start_x=0, start_y=0)
    r.camera.max_range = 200
    run_for(r, 1.0, lambda t: r.set_drive_power(0, 1, 0))
    before_odo = r.odometry.get_pose()
    r.x += 8  # a defender shoves the robot sideways in field x
    print("odometry (last good reading) :", before_odo)
    print("camera (sees true bumped pose):", r.camera.localize())


def ex9():
    field = Field().add_standard_tags()
    r = Robot(field=field, start_x=0, start_y=0)
    r.camera.max_range = 200
    target = Pose2d(60, 0, 0)

    def loop(t):
        loc = r.camera.localize()
        if loc and loc.distance_to(target) < 2.0:
            r.set_drive_power(0, 0, 0)
        else:
            r.set_drive_power(0, 1, 0)
    run_for(r, 3.0, loop)
    print("vision-stopped at:", r.camera.localize())


def ex10():
    print("""CVMaster plan (high level):
- During AUTON init / driving: run the AprilTag pipeline to localize and to
  re-seed odometry (kill drift) at key moments.
- When hunting a game piece: switch to the color-blob pipeline to find the
  sample's location, then drive to it.
- Don't run heavy vision EVERY loop: image processing is slow and would blow
  your loop time (Ch 15 -- bulk reads / fast loops). Sample vision a few times
  a second, fuse with fast odometry in between.""")


if __name__ == "__main__":
    for name in ["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10"]:
        print("\n===", name, "===")
        globals()[name]()
