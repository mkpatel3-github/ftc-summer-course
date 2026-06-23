"""Chapter 25 solutions - Path Following: Pure Pursuit (and a peek at GVF)."""
import sys, os, math
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
from ftcsim import Robot, Path, PurePursuitFollower, run_for

CURVE = [(0, 0), (10, 0), (20, 10), (20, 20)]   # the L-ish curve reused below


def ex1():
    # Projection index advances as the robot moves along the path.
    path = Path([(0, 0), (5, 2), (10, 6), (15, 12), (20, 20)])
    r = Robot()
    r.x, r.y = 0, 0
    print("at start:", path.closest_point(r.x, r.y))
    r.x, r.y = 10, 6
    print("after moving:", path.closest_point(r.x, r.y))


def ex2():
    # The carrot slides forward along the path as the robot advances.
    path = Path([(0, 0), (5, 0), (10, 0), (15, 0), (20, 0), (25, 0), (30, 0)])
    r = Robot()
    for x in (0, 5, 10, 15):
        r.x = x
        print(f"robot x={x}: lookahead = {path.lookahead_point(r.x, r.y, 8.0)}")


def ex3():
    # Follow a straight line; arrive near (30, 0).
    path = Path([(0, 0), (30, 0)])
    r = Robot()
    follower = PurePursuitFollower(r, path, lookahead=8.0)
    going = [True]
    def loop(t):
        going[0] = follower.run()
    run_for(r, 5.0, loop)
    print(f"final ({r.x:.1f}, {r.y:.1f})  arrived={not going[0]}")


def ex4():
    # Follow the L-curve; arrive near (20, 20) without stopping at the corner.
    path = Path(CURVE)
    r = Robot()
    follower = PurePursuitFollower(r, path, lookahead=8.0)
    def loop(t):
        follower.run()
    run_for(r, 6.0, loop)
    print(f"final ({r.x:.1f}, {r.y:.1f})  (target ~20,20)")


def _track_curve(lookahead, seconds=6.0):
    """Run the curve; return (final_pose, list of off-path distances)."""
    path = Path(CURVE)
    r = Robot()
    follower = PurePursuitFollower(r, path, lookahead=lookahead)
    dists = []
    def loop(t):
        follower.run()
        dists.append(path.closest_point(r.x, r.y)[1])
    run_for(r, seconds, loop)
    return r, dists


def ex5():
    # Small lookahead -> the robot hugs the path tightly (low off-path distance).
    r, dists = _track_curve(lookahead=2.0)
    sample = dists[::15]
    print("off-path distance every ~15 loops:", [round(d, 1) for d in sample])
    print(f"final ({r.x:.1f}, {r.y:.1f})")
    # Carrot just ahead of the nose -> tight tracking. This sim has no momentum,
    # so it simply tracks closely. On a REAL robot, momentum means the robot
    # overshoots the close carrot and wobbles across the path -- which is why you
    # don't set lookahead too small on hardware.


def ex6():
    # Lookahead too big -> cuts the corner (large max off-path distance).
    _, small = _track_curve(lookahead=6.0)
    _, big = _track_curve(lookahead=20.0)
    print(f"max off-path: lookahead=6 -> {max(small):.1f}   "
          f"lookahead=20 -> {max(big):.1f}")
    # A big lookahead aims far down the path and drifts INSIDE the corner:
    # smooth, but it misses tight waypoints. Big = smooth but sloppy.


def ex7():
    # Tune the lookahead: total tracking error grows as lookahead grows.
    print(f"{'lookahead':>10}{'total_err':>12}")
    for la in (2, 6, 10, 16):
        path = Path(CURVE)
        r = Robot()
        follower = PurePursuitFollower(r, path, lookahead=la)
        total = [0.0]
        def loop(t):
            follower.run()
            total[0] += path.closest_point(r.x, r.y)[1]
        run_for(r, 6.0, loop)
        print(f"{la:>10}{total[0]:>12.1f}")
    # Smaller lookahead tracks tighter (lower error) here; bigger cuts corners.
    # You pick the value that trades accuracy against smoothness -- and on real
    # hardware you stay above the value where momentum starts a wobble. Same
    # tune-by-testing idea as a kP gain.


def ex8():
    # Use .run()'s return value as the loop condition; the follower stops itself.
    path = Path(CURVE)
    r = Robot()
    follower = PurePursuitFollower(r, path, lookahead=8.0, tol=2.0)
    loops = [0]
    def loop(t):
        if follower.run():
            loops[0] += 1
    run_for(r, 6.0, loop)
    end = path.end()
    dist = math.hypot(end[0] - r.x, end[1] - r.y)
    print(f"loops while running={loops[0]}  final dist to end={dist:.2f} (tol=2.0)")


def ex9():
    # A two-leg autonomous: follow path A, then path B from there.
    r = Robot()
    leg_a = Path([(0, 0), (10, 0), (20, 0)])
    fa = PurePursuitFollower(r, leg_a, lookahead=8.0)
    run_for(r, 4.0, lambda t: fa.run())
    print(f"after leg A: ({r.x:.1f}, {r.y:.1f})")
    leg_b = Path([(20, 0), (20, 10), (20, 20)])
    fb = PurePursuitFollower(r, leg_b, lookahead=8.0)
    run_for(r, 4.0, lambda t: fb.run())
    print(f"after leg B: ({r.x:.1f}, {r.y:.1f})")
    # Chaining segments == RoadRunner's .splineTo(...).splineTo(...).


def ex10():
    # Pure pursuit vs GVF: steering = go-along-path (tangent) + pull-onto-path (error).
    path = Path(CURVE)
    r = Robot()
    follower = PurePursuitFollower(r, path, lookahead=8.0)
    n = [0]
    def loop(t):
        i, err = path.closest_point(r.x, r.y)
        nxt = path.points[min(i + 1, len(path.points) - 1)]
        here = path.points[i]
        tangent = math.degrees(math.atan2(nxt[1] - here[1], nxt[0] - here[0]))
        if n[0] % 30 == 0:
            print(f"loop {n[0]:3d}: tangent={tangent:6.1f}deg  off-path err={err:.2f}")
        n[0] += 1
        follower.run()
    run_for(r, 6.0, loop)
    # tangent = the GVF "tangent" vector (direction the path heads here);
    # off-path err = the GVF "normal"/error vector (pull back onto the path).
    # Pure pursuit blends them implicitly by aiming at a lookahead point. GVF
    # adds curvature-limited speed: it slows down where the path bends hard.


if __name__ == "__main__":
    for name in ["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10"]:
        print("\n===", name, "===")
        globals()[name]()
