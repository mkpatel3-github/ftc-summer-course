# START HERE 👋 (read this first!)

Welcome to the Juice Robotics summer coding course! By the end you'll understand the
*real* code our FTC team (#16236) uses to win matches — and you'll be ready to write it
yourself. You only need a laptop. **No robot required.**

This page gets you from zero to writing your first robot code in about 15 minutes.

---

## Step 1 — Get Python (one time, ~5 min)

You write your code in **Python**. Check if you already have it. Open a terminal:

- **Windows:** press the Start key, type `cmd`, hit Enter.
- **Mac:** press Cmd+Space, type `terminal`, hit Enter.

Type this and press Enter:

```bash
python --version
```

- If you see something like `Python 3.11.5` → 🎉 you're done, skip to Step 2.
- If it says "not found" or shows version 2.something → go to **https://python.org/downloads**,
  download Python 3 (the big yellow button), and install it.
  **On Windows, CHECK THE BOX that says "Add Python to PATH"** during install — this is
  the #1 thing people forget. Then close and reopen the terminal and try again.

You do **not** need to install anything else. No pip, no libraries. Just Python 3.

## Step 2 — Get a code editor (one time, ~3 min)

You *can* use the **IDLE** editor that comes free with Python (search your computer for
"IDLE"). It's simple and totally fine for this course.

If you want the editor real programmers (and our team) use, install **VS Code** from
**https://code.visualstudio.com** — also free. Either is great. Pick one.

## Step 3 — Make sure the simulator works (~2 min)

Find this course folder on your computer. In the terminal, go into it. For example:

```bash
cd Documents/soham/ftc-summer-course
```

(Replace the path with wherever the folder actually is. Tip: you can type `cd ` with a
space, then drag the folder into the terminal window, then press Enter.)

Now run the simulator's self-test:

```bash
python sim/ftcsim.py
```

You should see exactly this:

```
After driving forward 2s: x=  72.0  y=   0.0  heading=   0.0
```

🎉 **That means a fake robot just drove forward in your computer.** You're ready.

---

## Step 4 — Do your first exercise

Here's the daily routine. You'll repeat it ~once per weekday.

**1. Read the lesson.** Open the chapter for today, starting with
`chapters/01-hello-robot.md`. Read it like a story — it explains the idea and shows you
real Juice robot code.

**2. Open the starter file.** Each chapter has a `chapters/NN_starter.py` file. That's
*your* workspace. Open `chapters/01_starter.py` in your editor. You'll see each exercise
written as a comment, with a spot that says:

```python
def exercise_1():
    # ---- YOUR CODE HERE ----
    pass
```

**3. Write your code.** Delete the `pass` and write your solution. Then, at the very
bottom of the file, **un-comment** the matching line (remove the `#`):

```python
if __name__ == "__main__":
    exercise_1()        # <- you removed the # in front of this
    # exercise_2()
```

**4. Run it** and see what happens:

```bash
python chapters/01_starter.py
```

**5. Got stuck for real?** Try for at least 10–15 minutes first — being stuck is how you
learn. Then you may peek at the answer key in `solutions/01_solution.py`. Read *why* it
works, then go back and finish your own version. **Copying without understanding cheats
only you** — the season is the real test.

---

## The plan for the summer 📅

- There are **16 chapters**, each with **10 exercises** = **160 little challenges**.
  Chapters 1–10 are the core skills; 11–16 are the "modern robot" upgrades (turning your
  Python into real Java, plus what the best teams do today).
- Do about **one exercise per weekday**. That's a whole summer, and you'll finish right
  around when the new FTC season starts. If you only get through Chapter 11, you're
  already ready — the rest makes you *competitive*.
- Some days an exercise is a 5-minute warm-up; some are a real puzzle. That's normal.
- The exercises in each chapter go easy → harder. Exercises **1–2** are warm-ups,
  **3–7** are the main idea, **8–10** are challenge/stretch. It's okay to come back to
  the last few.

### What you'll be able to do by the end

Drive a robot, make it go an exact distance, turn perfectly using the gyro (just like
"gyro-straight" in FLL!), follow a line, read colors, drive with a gamepad, build a PID
controller, organize a robot into subsystems, and write an autonomous program that scores
points on its own. That's real FTC programming.

---

## Tips & common problems 🛠️

- **"python: command not found"** → Python isn't installed or not "on PATH". Redo Step 1
  and check that box on Windows. Sometimes the command is `python3` instead of `python` —
  try that.
- **"ModuleNotFoundError: No module named 'ftcsim'"** → you're running the file from the
  wrong place. Always run from inside the `ftc-summer-course` folder, and run it as
  `python chapters/01_starter.py` (not from inside the `chapters` folder).
- **"IndentationError"** → in Python, spaces at the start of a line matter. Make sure your
  code lines under a `def` are indented the same amount (4 spaces is standard).
- **Nothing prints** → did you un-comment the `exercise_1()` line at the bottom and save
  the file before running?
- **It printed an error with red text** → read the LAST line of the error first; it
  usually tells you exactly what's wrong. Errors are normal. Every programmer reads
  errors all day.

## Want to see the real team code? 👀

It's right here on your computer (in the folder above this one):

- `IntoTheDeep/` — Juice's robot from the 2024–25 season.
- Every lesson has a **"Java bridge"** box showing how your Python turns into the Java the
  team actually runs. You'll be able to read the real files by the end!

Have fun. Break things. Ask questions. See you at kickoff. 🚀

— Juice Robotics #16236
