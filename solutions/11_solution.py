"""Chapter 11 solutions - Crossing to Java.

This chapter is about writing Java by hand, which you can't run here. So each
solution PRINTS the correct Java as text, and where there's runnable Python
(the logic you're converting) we run it too, to prove the idea still works.
"""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
from ftcsim import Robot, Gamepad, run_for


def ex1():
    print("int wheels = 4;")
    print('double power = 0.6;')
    print('String name = "Juice";')


def ex2():
    print("""if (speed > 1.0) {
    speed = 1.0;
} else {
    speed = speed;
}""")


def ex3():
    # The Python it mirrors:
    for i in range(4):
        print("python i =", i)
    print("""// Java:
for (int i = 0; i < 4; i++) {
    telemetry.addData("i", i);
}""")


def clamp(power):  # the Python logic we're converting
    return max(-1.0, min(1.0, power))


def ex4():
    print("python clamp(1.5) =", clamp(1.5), "| clamp(-2) =", clamp(-2))
    print("""// Java:
double clamp(double power) {
    if (power > 1.0)  return 1.0;
    if (power < -1.0) return -1.0;
    return power;
}""")


def wheel_powers(x, y, rx):
    fl = y + x + rx
    fr = y - x - rx
    bl = (y - x + rx) * -1
    br = (y + x - rx) * -1
    return [fl, fr, bl, br]


def ex5():
    print("python forward:", wheel_powers(0, 1, 0))
    print("""// Java (Juice's exact formula):
double powerFrontLeft  = y + x + rx;
double powerFrontRight = y - x - rx;
double powerBackLeft   = (y - x + rx) * -1;
double powerBackRight  = (y + x - rx) * -1;""")


def ex6():
    mapping = {
        "set_drive_power": "setDrivePower",
        "get_encoder_value": "getEncoderValue",
        "reset_heading": "resetHeading",
        "left_stick_y": "left_stick_y  (UNCHANGED -- it's an SDK gamepad field)",
        "is_red_alliance": "isRedAlliance",
    }
    for k, v in mapping.items():
        print(f"{k:20s} -> {v}")
    print("NOTE: gamepad fields keep snake_case because that's the FTC SDK's "
          "spelling, not something you named.")


def ex7():
    print("""telemetry.addData("MODE", mode);
telemetry.addData("pose", robot.getPose());
telemetry.addData("loop", loopCount);
telemetry.update();""")


def ex8():
    print("""@TeleOp(name = "Mini TeleOp")
public class MiniTeleOp extends LinearOpMode {
    @Override
    public void runOpMode() {
        Robot robot = new Robot(hardwareMap);
        Gamepad oldGamepad = new Gamepad();
        String mode = "SAMPLE";
        waitForStart();
        while (opModeIsActive()) {
            // ... edge-detect gamepad1.a to toggle mode ...
            // ... robot.setDrivePower(x, y, rx); ...
            // ... telemetry.update(); ...
            oldGamepad.copy(gamepad1);
        }
    }
}""")


def ex9():
    print("""public class Lift {
    private DcMotorEx motor;
    private PIDFController pidf;
    private int target = 0;

    public Lift(HardwareMap hardwareMap) {
        motor = hardwareMap.get(DcMotorEx.class, "lift");
        pidf  = new PIDFController(0.01, 0, 0.0005, 0.1);
    }

    public void setTarget(int ticks) { this.target = ticks; }

    public void update() {
        double power = pidf.update(motor.getCurrentPosition(), target);
        motor.setPower(power);
    }
}""")


def ex10():
    print("""Bug 1: missing comma between parameters -> drive(double x, double y)
Bug 2: missing semicolon after 'double power = x + y' -> add ;
Bug 3: if condition needs parentheses -> if (power > 1) {
Bug 4: missing semicolon after telemetry.addData(...) -> add ;
Fixed:
public void drive(double x, double y) {
    double power = x + y;
    if (power > 1) {
        power = 1;
    }
    telemetry.addData("power", power);
}""")


if __name__ == "__main__":
    for name in ["ex1","ex2","ex3","ex4","ex5","ex6","ex7","ex8","ex9","ex10"]:
        print("\n===", name, "===")
        globals()[name]()
