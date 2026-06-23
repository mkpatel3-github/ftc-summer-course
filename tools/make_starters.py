"""Generate chapters/NN_starter.py from each lesson's '## Exercises' section.

Run from the ftc-summer-course folder:  python tools/make_starters.py
Re-run any time the lessons change; it overwrites the starter files.
"""
import os
import re
import glob

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTERS = os.path.join(HERE, "chapters")

HEADER = '''"""
{title}

This is YOUR workspace. Read the matching lesson first:
    chapters/{lesson}

Then solve each exercise below where it says  # ---- YOUR CODE HERE ----.
Run this file any time to see your output:
    python chapters/{starter}

Stuck? Try for real first, THEN peek at:
    solutions/{num}_solution.py
"""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "sim"))
# Everything from the simulator you might need:
from ftcsim import (Robot, Field, Gamepad, IMU, Motor, StepperServo,
                    PIDFController, run_for, Pose2d, AprilTag, Odometry, Camera,
                    Command, InstantCommand, SequentialCommand, ParallelCommand,
                    SleepCommand, CommandScheduler, DriveToPoseAction,
                    SequentialAction, run_action,
                    LynxModule, reset_hw_reads, hw_reads, KalmanFilter,
                    AsymmetricMotionProfile, Localizer, DriveEncoderLocalizer,
                    DeadWheelLocalizer, OTOSLocalizer)

print("Chapter {num} - delete this line and start coding your exercises!\\n")


'''

EXERCISE_TEMPLATE = '''# ===========================================================================
# Exercise {n}
# {prompt}
# ===========================================================================
def exercise_{n}():
    # ---- YOUR CODE HERE ----
    pass


'''

FOOTER = '''if __name__ == "__main__":
    # Uncomment each exercise as you finish it, then run this file.
    pass
{calls}
'''


def clean(text):
    """Turn lesson markdown into plain comment text."""
    text = text.replace("`", "").replace("**", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def wrap(text, width=74, indent="# "):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return ("\n" + indent).join(lines)


def parse_exercises(md):
    """Return list of exercise prompt strings 1..10 from the Exercises section."""
    # Grab text from the '## Exercises' heading to the next '## ' heading.
    m = re.search(r"##\s+Exercises\s*(.*?)(?:\n##\s|\Z)", md, re.S)
    body = m.group(1) if m else md
    # Split on bold-numbered markers like **3.** at the start of a line.
    parts = re.split(r"\n\*\*(\d+)\.", "\n" + body)
    # parts = ['', '1', ' prompt...', '2', ' prompt...', ...]
    out = {}
    for i in range(1, len(parts) - 1, 2):
        num = int(parts[i])
        prompt = clean(parts[i + 1])
        out[num] = prompt
    return [out[k] for k in sorted(out)]


def main():
    for md_path in sorted(glob.glob(os.path.join(CHAPTERS, "*.md"))):
        base = os.path.basename(md_path)
        num = base[:2]
        with open(md_path, encoding="utf-8") as f:
            md = f.read()
        title_match = re.search(r"#\s+(Chapter.*)", md)
        title = title_match.group(1).strip() if title_match else base
        prompts = parse_exercises(md)
        if len(prompts) != 10:
            print(f"WARNING {base}: found {len(prompts)} exercises (expected 10)")

        starter_name = f"{num}_starter.py"
        chunks = [HEADER.format(title=title, lesson=base, starter=starter_name, num=num)]
        for i, prompt in enumerate(prompts, 1):
            chunks.append(EXERCISE_TEMPLATE.format(n=i, prompt=wrap(prompt)))
        calls = "\n".join(f"    # exercise_{i}()" for i in range(1, len(prompts) + 1))
        chunks.append(FOOTER.format(calls=calls))

        out_path = os.path.join(CHAPTERS, starter_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("".join(chunks))
        print(f"wrote {out_path} ({len(prompts)} exercises)")


if __name__ == "__main__":
    main()
