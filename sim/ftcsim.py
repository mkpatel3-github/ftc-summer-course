"""
ftcsim - a tiny FTC robot simulator for the Juice Summer Course.

WHY THIS EXISTS
---------------
FTC robots run Java on an Android phone/Control Hub. You cannot run that code on
a laptop, and you will not have the robot for most of the summer. This file fakes
just enough of the real FTC world so you can write the SAME ideas in Python today,
see them work, and then translate them to Java for team 16236 "Juice" when the
season starts.

The class and method names here are chosen to MATCH the names in Juice's real
codebase (Motor, StepperServo, setSpeed/set_speed, getEncoderValue, IMU,
PIDFController, setDrivePower, telemetry...). Python uses snake_case by habit, so
each method has BOTH names (set_speed AND setSpeed) -- use whichever you like, and
notice how close the Java version will look.

Everything is "headless": there is no graphics window. The robot prints telemetry
to the screen, exactly like a real driver station. A simple physics model moves a
virtual robot around a 144 x 144 inch FTC field so that driving, gyro turns,
encoders, and sensors actually do something.

You do not need to read or understand this whole file to use it. Treat it like the
"FTC SDK": a black box you call into. Later chapters peek inside on purpose.
"""

import math
import time


# ---------------------------------------------------------------------------
# Telemetry: the robot's way of talking to you (like the Driver Station screen)
# ---------------------------------------------------------------------------
class Telemetry:
    """Mirrors FTC `telemetry.addData(...)` / `telemetry.update()`."""

    def __init__(self):
        self._lines = []

    def add_data(self, caption, value):
        self._lines.append(f"{caption}: {value}")

    # Java spelling, so your Python looks like the real thing:
    addData = add_data

    def update(self):
        print("---- TELEMETRY ----")
        for line in self._lines:
            print(line)
        print("-------------------")
        self._lines = []


# ---------------------------------------------------------------------------
# The field: a flat 144" x 144" square. Origin (0,0) is the center, matching
# RoadRunner / Juice autonomous poses (e.g. Pose2d(-30, -60, ...) in BucketSide).
# +x is to the right, +y is "up" the field, heading is in DEGREES, 0 = +x axis.
# ---------------------------------------------------------------------------
FIELD_HALF = 72.0  # inches from center to wall


class Field:
    """Holds anything in the world that sensors can detect."""

    def __init__(self):
        # A black "line" on the floor: a vertical stripe at x = line_x, some width.
        self.line_x = 0.0
        self.line_half_width = 1.0
        # A colored game element ("sample") the color sensor can see when close.
        self.sample_x = None
        self.sample_y = None
        self.sample_color = None  # "RED", "BLUE", or "YELLOW"
        # A wall/object straight ahead for the distance sensor (inches from center).
        self.front_wall_x = FIELD_HALF


# ---------------------------------------------------------------------------
# Motor: matches Juice util/hardware/Motor.java
#   setSpeed(power), getEncoderValue(), setTarget(ticks), resetEncoder()
# A real DC motor turns an encoder. We model: power -> wheel speed -> ticks.
# ---------------------------------------------------------------------------
TICKS_PER_INCH = 45.0  # made-up but consistent gearing for the sim


class Motor:
    def __init__(self, port, name, reverse=False):
        self.port = port
        self.name = name
        self.reverse = reverse
        self.speed = 0.0
        self._ticks = 0.0  # encoder count

    def set_speed(self, power):
        power = max(-1.0, min(1.0, power))  # clamp like a real motor controller
        self.speed = -power if self.reverse else power

    setSpeed = set_speed

    def get_encoder_value(self):
        return self._ticks

    getEncoderValue = get_encoder_value

    def reset_encoder(self):
        self._ticks = 0.0

    resetEncoder = reset_encoder

    # called by the physics engine each tick; not part of the real API
    def _advance(self, dt, max_in_per_s=40.0):
        distance_in = self.speed * max_in_per_s * dt
        self._ticks += distance_in * TICKS_PER_INCH


# ---------------------------------------------------------------------------
# StepperServo: matches Juice util/hardware/StepperServo.java
#   setAngle(deg), getAngle()  -- a servo holds an angle, it does not spin freely
# ---------------------------------------------------------------------------
class StepperServo:
    def __init__(self, port, name):
        self.port = port
        self.name = name
        self.angle = 0.0

    def set_angle(self, angle):
        self.angle = max(0.0, min(355.0, angle))

    setAngle = set_angle

    def get_angle(self):
        return self.angle

    getAngle = get_angle


# ---------------------------------------------------------------------------
# IMU / gyro: matches the idea of FTC's IMU. Reports robot heading in degrees.
# This is the sensor behind "gyro straight" and "turn to angle".
# ---------------------------------------------------------------------------
class IMU:
    def __init__(self, robot):
        self._robot = robot

    def get_heading(self):
        """Heading in degrees, normalized to (-180, 180]."""
        h = self._robot.heading
        h = (h + 180) % 360 - 180
        return h

    getHeading = get_heading

    def reset_heading(self):
        self._robot.heading = 0.0

    resetHeading = reset_heading


# ---------------------------------------------------------------------------
# ColorSensor: matches the REV color sensor Juice uses in Claw.detectSample().
# Reports red/green/blue (0..1) and distance. Only "sees" a sample when the robot
# is right on top of it.
# ---------------------------------------------------------------------------
class ColorSensor:
    def __init__(self, robot, field):
        self._robot = robot
        self._field = field

    def _near_sample(self):
        f = self._field
        if f.sample_x is None:
            return False
        d = math.hypot(self._robot.x - f.sample_x, self._robot.y - f.sample_y)
        return d < 4.0

    def red(self):
        if self._near_sample() and self._field.sample_color in ("RED", "YELLOW"):
            return 0.9
        return 0.05

    def green(self):
        if self._near_sample() and self._field.sample_color == "YELLOW":
            return 0.9
        return 0.05

    def blue(self):
        if self._near_sample() and self._field.sample_color in ("BLUE",):
            return 0.9
        return 0.05

    def get_distance(self):
        """mm to nearest object the sensor is pointed at (the floor/sample)."""
        return 2.0 if self._near_sample() else 50.0

    getDistance = get_distance


# ---------------------------------------------------------------------------
# DistanceSensor: forward-facing, for "drive until wall" / wall following.
# ---------------------------------------------------------------------------
class DistanceSensor:
    def __init__(self, robot, field):
        self._robot = robot
        self._field = field

    def get_distance(self):
        """Inches to the wall straight ahead (very simplified: uses +x wall)."""
        return max(0.0, self._field.front_wall_x - self._robot.x)

    getDistance = get_distance


# ---------------------------------------------------------------------------
# Gamepad: in real FTC a human drives. Here you give it a SCRIPT of inputs so a
# TeleOp loop can run automatically in the sim. Fields mirror FTC's gamepad1.
# ---------------------------------------------------------------------------
class Gamepad:
    def __init__(self):
        self.left_stick_x = 0.0
        self.left_stick_y = 0.0
        self.right_stick_x = 0.0
        self.a = self.b = self.x = self.y = False
        self.left_bumper = self.right_bumper = False
        self.dpad_up = self.dpad_down = self.dpad_left = self.dpad_right = False

    def copy(self, other):
        self.__dict__.update(other.__dict__)


# ---------------------------------------------------------------------------
# PIDFController: a faithful port of Juice util/control/PIDFController.java.
# You will rebuild this yourself in Chapter 7; it lives here so earlier chapters
# can use it as a black box.
# ---------------------------------------------------------------------------
class PIDFController:
    def __init__(self, kp, ki, kd, kf, rot=False):
        self.kp, self.ki, self.kd, self.kf = kp, ki, kd, kf
        self.rot = rot
        self._last_error = 0.0
        self._error_sum = 0.0
        self._last_time = time.time()
        self._first = True
        self.error = 0.0

    def update(self, new_input, set_point, dt=None):
        # dt: if given, use this fixed time step (deterministic, good for the
        # simulator). If None, use real wall-clock time like the real robot.
        if dt is not None:
            period = dt
        else:
            now = time.time()
            period = max(1e-3, now - self._last_time)
            self._last_time = now
        if self.rot:
            self.error = math.atan2(
                math.sin(math.radians(set_point - new_input)),
                math.cos(math.radians(set_point - new_input)),
            )
            self.error = math.degrees(self.error)
        else:
            self.error = set_point - new_input
        if math.copysign(1, self._last_error) != math.copysign(1, self.error):
            self._error_sum = 0.0
        self._error_sum += self.error * period
        # On the very first call there is no previous error to compare against,
        # so the derivative is undefined -- treat it as 0 (a real robot has the
        # same problem on loop #1).
        der_error = 0.0 if self._first else (self.error - self._last_error) / period
        self._first = False
        output = (self.kp * self.error + self.ki * self._error_sum
                  + self.kd * der_error + self.kf * math.copysign(1, self.error))
        self._last_error = self.error
        return output


# ---------------------------------------------------------------------------
# Robot: the heart of the sim. Holds 4 mecanum motors and exposes
# setDrivePower(x, y, rx) using the SAME formula as Juice Robot.java:676.
# Calling step() advances the physics by dt seconds and moves the robot.
# ---------------------------------------------------------------------------
class Robot:
    def __init__(self, field=None, start_x=0.0, start_y=0.0, start_heading=0.0):
        self.field = field or Field()
        self.x = start_x
        self.y = start_y
        self.heading = start_heading  # degrees

        self.front_left = Motor(0, "leftFront")
        self.front_right = Motor(1, "rightFront")
        self.back_left = Motor(2, "leftBack")
        self.back_right = Motor(3, "rightBack")

        self.imu = IMU(self)
        self.color = ColorSensor(self, self.field)
        self.distance = DistanceSensor(self, self.field)
        self.telemetry = Telemetry()

        self._fl = self._fr = self._bl = self._br = 0.0

    # --- exact port of Juice Robot.java setDrivePower ---
    def set_drive_power(self, x, y, rx):
        power_fl = y + x + rx
        power_fr = y - x - rx
        power_bl = (y - x + rx) * -1
        power_br = (y + x - rx) * -1
        biggest = max(abs(power_fl), abs(power_fr), abs(power_bl), abs(power_br), 1.0)
        self._fl = power_fl / biggest
        self._fr = power_fr / biggest
        self._bl = power_bl / biggest
        self._br = power_br / biggest
        self.front_left.set_speed(self._fl)
        self.front_right.set_speed(self._fr)
        self.back_left.set_speed(-self._bl)
        self.back_right.set_speed(-self._br)

    setDrivePower = set_drive_power

    def step(self, dt=0.02):
        """Advance the simulation by dt seconds. Call this inside your loop."""
        # Translate the 4 wheel powers into robot-frame motion (forward, strafe, turn)
        forward = (self._fl + self._fr - self._bl - self._br) / 4.0
        strafe = (self._fl - self._fr + self._bl - self._br) / 4.0
        turn = (self._fl - self._fr - self._bl + self._br) / 4.0

        max_lin = 40.0   # in/s at full power
        max_rot = 180.0  # deg/s at full power

        # Move in field frame using current heading
        h = math.radians(self.heading)
        dx_robot = forward * max_lin * dt
        dy_robot = strafe * max_lin * dt
        self.x += dx_robot * math.cos(h) - dy_robot * math.sin(h)
        self.y += dx_robot * math.sin(h) + dy_robot * math.cos(h)
        self.heading += turn * max_rot * dt

        # keep encoders in sync
        for m in (self.front_left, self.front_right, self.back_left, self.back_right):
            m._advance(dt)

        # keep the robot on the field
        self.x = max(-FIELD_HALF, min(FIELD_HALF, self.x))
        self.y = max(-FIELD_HALF, min(FIELD_HALF, self.y))

    def pose_str(self):
        return f"x={self.x:6.1f}  y={self.y:6.1f}  heading={self.imu.get_heading():6.1f}"


# ---------------------------------------------------------------------------
# A tiny helper so exercises can "run a TeleOp" for a fixed time without a robot.
# ---------------------------------------------------------------------------
def run_for(robot, seconds, loop_fn, dt=0.02, realtime=False):
    """Call loop_fn(t) repeatedly, stepping physics, until `seconds` elapse.

    loop_fn receives the elapsed time t (seconds) and should call
    robot.set_drive_power(...) / read sensors, like the body of opModeIsActive().
    """
    steps = int(seconds / dt)
    for i in range(steps):
        t = i * dt
        loop_fn(t)
        robot.step(dt)
        if realtime:
            time.sleep(dt)
    return robot


if __name__ == "__main__":
    # quick self-test: drive forward 2 seconds
    r = Robot()
    run_for(r, 2.0, lambda t: r.set_drive_power(0, 1.0, 0))
    print("After driving forward 2s:", r.pose_str())
