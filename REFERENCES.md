# References & Source Material

This course is built from real, open-source FTC code and books. We **link** to them here
instead of copying them in — open them on GitHub to read the originals.

## Team Juice (#16236) — the code this course teaches

- **GitHub org:** https://github.com/Juice-Robotics
- **Into the Deep (2024–25, current):** https://github.com/Juice-Robotics/IntoTheDeep
  — the robot this course is based on. Files referenced in the lessons:
  - `TeamCode/.../Robot.java` — mecanum `setDrivePower`, subsystems, the `Levels` state machine, presets
  - `TeamCode/.../util/control/PIDFController.java` — the PID controller you rebuild in Chapter 7
  - `TeamCode/.../subsystems/lift/Lift.java` — PID + feedforward in a real subsystem
  - `TeamCode/.../util/hardware/Motor.java`, `StepperServo.java` — hardware wrappers
  - `TeamCode/.../subsystems/claw/Claw.java` — `detectSample()` color logic (Chapter 5 fixes its unfinished version)
  - `TeamCode/.../teleop/TeleOpMainRed.java` — gamepad edge-detection + action queue (Chapter 6)
  - `TeamCode/.../auton/BucketSide.java` — RoadRunner autonomous (Chapter 9)
- **Older seasons:** CenterStage (2023–24) https://github.com/Juice-Robotics/CenterStageV2 ·
  PowerPlay (2022–23) https://github.com/Juice-Robotics/PowerPlay
- **Team site:** https://juicerobotics.org

> Tip: to read the team code locally, clone it next to this course (it is **not** included
> in this repo on purpose):
> ```bash
> git clone https://github.com/Juice-Robotics/IntoTheDeep.git
> ```

## Books & guides

- **Learn Java for FTC** — Alan Smith (free): https://github.com/alan412/LearnJavaForFTC
  (PDF: https://github.com/alan412/LearnJavaForFTC/blob/master/LearnJavaForFTC.pdf).
  The best true-beginner FTC Java book; has on-robot exercises to do after this course.
- **Game Manual 0 (gm0)** — community FTC guide: https://gm0.org ·
  repo https://github.com/gamemanual0/gm0
- **CTRL+ALT+FTC** — controls/PID/odometry math: https://www.ctrlaltftc.com
- **Official FTC SDK & sample OpModes:**
  https://github.com/FIRST-Tech-Challenge/FtcRobotController
- **RoadRunner** (autonomous motion library Juice uses):
  https://github.com/acmerobotics/road-runner
