"""Chapter 15 solutions - Command-Based Programming."""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
from ftcsim import (Robot, Command, InstantCommand, SequentialCommand,
                    ParallelCommand, SleepCommand, CommandScheduler)


class DriveForward(Command):
    def __init__(self, robot, seconds):
        self.robot, self.seconds, self.t = robot, seconds, 0.0

    def init(self):
        self.robot.set_drive_power(0, 1.0, 0)

    def update(self):
        self.t += 0.02
        return self.t >= self.seconds

    def end(self):
        self.robot.set_drive_power(0, 0, 0)


class Strafe(Command):
    def __init__(self, robot, seconds):
        self.robot, self.seconds, self.t = robot, seconds, 0.0

    def init(self):
        self.robot.set_drive_power(1.0, 0, 0)

    def update(self):
        self.t += 0.02
        return self.t >= self.seconds

    def end(self):
        self.robot.set_drive_power(0, 0, 0)


class Spin(Command):
    def __init__(self, robot, seconds):
        self.robot, self.seconds, self.t = robot, seconds, 0.0

    def init(self):
        self.robot.set_drive_power(0, 0, 0.5)

    def update(self):
        self.t += 0.02
        return self.t >= self.seconds

    def end(self):
        self.robot.set_drive_power(0, 0, 0)


class DriveToX(Command):
    def __init__(self, robot, target_x):
        self.robot, self.target_x = robot, target_x

    def init(self):
        self.robot.set_drive_power(0, 1.0, 0)

    def update(self):
        return self.robot.x >= self.target_x

    def end(self):
        self.robot.set_drive_power(0, 0, 0)


class LoopCommand(Command):
    def __init__(self, fn, times):
        self.fn, self.times, self.n = fn, times, 0

    def update(self):
        self.fn(self.n)
        self.n += 1
        return self.n >= self.times


def ex1():
    r = Robot()
    CommandScheduler().run(r, DriveForward(r, 1.0))
    print("after DriveForward:", r.pose_str())


def ex2():
    r = Robot()
    CommandScheduler().run(r, InstantCommand(lambda: print("CLAW OPEN")))


def ex3():
    r = Robot()
    seq = SequentialCommand(
        InstantCommand(lambda: print("start")),
        SleepCommand(0.5),
        InstantCommand(lambda: print("end")),
    )
    CommandScheduler().run(r, seq)


def ex4():
    r = Robot()
    seq = SequentialCommand(DriveForward(r, 1.0), Strafe(r, 1.0))
    CommandScheduler().run(r, seq)
    print("after sequential drive+strafe:", r.pose_str())


def ex5():
    r = Robot()
    par = ParallelCommand(DriveForward(r, 1.0), Spin(r, 1.0))
    CommandScheduler().run(r, par)
    # Driving forward WHILE spinning curls the path (the nose keeps turning), so
    # it traces an arc rather than a straight line -- heading ends ~90 and the
    # robot can loop back near the start. The point: both ran in the SAME second,
    # which a plain SequentialCommand could never do.
    print("after parallel drive+spin:", r.pose_str(),
          "-> heading changed while it was also driving (arc)")


def ex6():
    r = Robot()
    CommandScheduler().run(r, DriveToX(r, 30))
    print("stopped near target x=30:", r.pose_str())


def ex7():
    r = Robot()
    auto = SequentialCommand(
        DriveToX(r, 30),
        ParallelCommand(DriveForward(r, 0.3),
                        InstantCommand(lambda: print("LIFT UP"))),
        InstantCommand(lambda: print("SCORE")),
    )
    CommandScheduler().run(r, auto)
    print("mini-auto end:", r.pose_str())


def ex8():
    # Same command classes, two different routines -> no rewriting.
    rL = Robot()
    left = SequentialCommand(DriveForward(rL, 0.5), Strafe(rL, 1.0))
    CommandScheduler().run(rL, left)
    print("LEFT routine end: ", rL.pose_str())

    rR = Robot()
    right = SequentialCommand(DriveForward(rR, 1.0), Spin(rR, 0.5))
    CommandScheduler().run(rR, right)
    print("RIGHT routine end:", rR.pose_str())
    # vs copy-pasting loops: one bug fix in DriveForward fixes BOTH routines.


def ex9():
    r = Robot()
    countdown = LoopCommand(lambda n: print("countdown", 3 - n), times=3)
    CommandScheduler().run(r, countdown)


def ex10():
    print("""A simple enum state machine (Ch 8 Levels) is ENOUGH when one
subsystem moves between a few named presets and nothing else is happening at
the same time -- e.g. a lift that is GROUND / LOW / HIGH. Commands earn their
complexity when MULTIPLE subsystems must act together or overlap in time
(drive while raising the lift while running intake), or when you want to reuse
and recombine steps across many autos. Choose by counting how many things move
at once: one -> enum; several, composed -> commands.""")


if __name__ == "__main__":
    for name in ["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10"]:
        print("\n===", name, "===")
        globals()[name]()
