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
  - `TeamCode/.../auton/BucketSide.java` — RoadRunner autonomous (Chapters 9 & 16)
  - `TeamCode/.../roadrunner/KalmanDrive.java` — Pinpoint odometry + Kalman fusion of
    odometry and a Limelight camera (Chapters 13 & 14). Credit: portions BSD-3 by j5155 /
    FTC 12087 Capital City Dynamics, portions MIT by goBILDA.
  - `TeamCode/.../subsystems/vision/CVMaster.java` — Limelight3A + VisionPortal,
    `ColorBlobLocatorProcessor` and an AprilTag pipeline (Chapter 14)
  - `TeamCode/.../commands/` — `CommandMaster.java`, and `commands/primitives/`
    (`InstantCommand`, `SequentialCommand`, `ParallelCommand`, `LoopCommand`,
    `SleepCommand`) — the command-based architecture (Chapter 15)
- **Older seasons:** CenterStage (2023–24) https://github.com/Juice-Robotics/CenterStageV2 ·
  PowerPlay (2022–23) https://github.com/Juice-Robotics/PowerPlay
- **Team site:** https://juicerobotics.org

> Tip: to read the team code locally, clone it next to this course (it is **not** included
> in this repo on purpose):
> ```bash
> git clone https://github.com/Juice-Robotics/IntoTheDeep.git
> ```

## Top-team codebases — the pro-architecture chapters (17–25)

Chapters 17–25 teach patterns lifted straight from the public code of four widely studied
teams. Clone any of these to read the real Java the lessons point at:

- **ACME Robotics (#8367) — RoadRunner quickstart:**
  https://github.com/acmerobotics/road-runner-quickstart
  - `.../localization/Localizer.java` + `ThreeDeadWheelLocalizer`, `TwoDeadWheelLocalizer`,
    `OTOSLocalizer`, `PinpointLocalizer` — the swappable-localizer Strategy pattern (Chapter 20)
  - `.../tuning/` OpModes (`ManualFeedforwardTuner`, drive velocity/feedforward tuners) +
    `@Config` / FTC Dashboard — the live tuning workflow (Chapter 22)
- **Seattle Solvers (#23511) — Into the Deep:** https://github.com/FTC-23511/Into-the-Deep-2025
  - `.../hardware/Robot.java` — the `getInstance()` hardware singleton (Chapter 17)
  - `.../hardware/Globals.java` — every tunable number/enum in one constants file (Chapter 17)
  - SolversLib (their FTCLib fork): https://github.com/Pedro-Pathing/SolversLib
- **Capital City Dynamics / j5155 (#12087) — 2024:** https://github.com/jdhs-ftc/2024
  - `.../helpers/control/KalmanFilter.java` — the 1-D Kalman filter you rebuild (Chapter 21)
  - `.../AprilTagDrive.java` + OTOS instructions — odometry predict / AprilTag correct
  - `.../PosePatcher.java` (timestamped pose `TreeMap`) + `AprilTagDrive.updatePoseEstimate()`
    — back-date a late detection and roll it forward; latency-compensated relocalization
    (Chapter 23)
- **KookyBotz (#16379) — CenterStage:** https://github.com/KookyBotz/CenterStage
  - `.../opmode/teleop/Duo.java` — the `clearBulkCache(); read(); periodic(); write();`
    loop structure (Chapter 18)
  - `.../utils/AsymmetricMotionProfile.java`, `WActuatorGroup.java` — hand-written
    asymmetric profile + PID + feedforward (Chapter 19)
  - `.../commands/ClawToggleCommand.java` (nested `ConditionalCommand`) + `Solo.java` button
    bindings (`gamepadEx.getGamepadButton(...).whenPressed(...)`) — advanced command-based
    (Chapter 24)
  - `.../utils/GVFPathFollower.java` — guided-vector-field path following; the "pro" version
    of the pure pursuit you build (Chapter 25)

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
  https://github.com/acmerobotics/road-runner · docs https://rr.brott.dev

## Modern FTC tools & hardware (Chapters 12–16)

- **Pedro Pathing** — popular newer path follower: https://pedropathing.com ·
  https://github.com/Pedro-Pathing/PedroPathing
- **FTCLib / NextFTC / SolversLib** — command-based libraries:
  https://github.com/FTCLib/FTCLib · https://nextftc.dev ·
  https://github.com/Pedro-Pathing/SolversLib
- **VisionPortal & AprilTags** — built into the FTC SDK; concept guides at gm0.org and
  https://www.ctrlaltftc.com
- **goBILDA Pinpoint** odometry computer: https://www.gobilda.com (search "Pinpoint")
- **SparkFun OTOS** optical tracking sensor:
  https://www.sparkfun.com/products/24904
- **Limelight 3A** smart camera (used in Juice's `CVMaster.java`):
  https://limelightvision.io
