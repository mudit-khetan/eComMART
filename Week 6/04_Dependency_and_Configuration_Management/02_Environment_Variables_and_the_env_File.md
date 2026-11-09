# Environment Variables and the .env File

## Lesson purpose

Last lesson, you created `requirements.txt` so another developer could install the same Python dependencies. There is still a second problem: two developers may run the **same code** but want different settings. One developer may keep the eComMART database in one folder, while another keeps it elsewhere.

In this lesson, you will move a setting **out of Python source code** and into a local configuration file. You will learn what an environment variable is, how a `.env` file helps during development, and how Python reads the value. This prepares you for the instructor's separate low-stock notifier and, later, your own Week 5 catalog restructuring challenge.

**Core for Week 6:** configure and read **one** environment variable. **Optional/stretch:** use additional variables or examine how a future AI application might configure an API key. **No real API key, signup, payment, or live AI call is required.**

## Learning objectives

By the end of this lesson, you will be able to:

- Explain the difference between a Python variable and an environment variable.
- Describe why changing settings without editing code is useful.
- Create a `.env` file with a simple `KEY=value` setting.
- Use `python-dotenv` to load that file and `os.getenv()` to read its value.
- Explain what `.env.example` and `.gitignore` are for.
- Verify a configured setting and troubleshoot a missing one.

## 1. The eComMART problem: the same program, different settings

Imagine the eComMART low-stock notifier needs a **stock threshold**. If stock is *less than* that threshold, the program should flag the product. During a practice run you might want the threshold to be 5, but another developer might want 10.

One approach is to hardcode it:

```python
LOW_STOCK_THRESHOLD = 5
```

That works, but now someone must edit Python code to change the setting. A configuration value keeps the logic stable while allowing each developer to choose a local setting.

| Term | Plain-language meaning | Example |
|---|---|---|
| Python variable | A name for a value used inside a running Python program | `threshold = 5` |
| Environment variable | A named setting provided to a running program from outside its code | `LOW_STOCK_THRESHOLD=5` |
| `.env` file | A local text file containing environment-variable-like `KEY=value` entries | `LOW_STOCK_THRESHOLD=5` |
| `python-dotenv` | A small installed package that reads `.env` entries into the program's environment | `load_dotenv()` |

**Important distinction:** Python does **not** automatically read a `.env` file. The `python-dotenv` package does that in our lesson. Some deployment platforms set real environment variables directly and do not need a `.env` file.

## 2. A first look at a .env file

A `.env` file is **plain text**. Its contents might be:

```dotenv
LOW_STOCK_THRESHOLD=5
```

Read this as: “Give the setting named `LOW_STOCK_THRESHOLD` the text value `5`.”

- The **name** is on the left of `=`.
- The **value** is on the right.
- This is configuration, **not Python code**. Do not write `LOW_STOCK_THRESHOLD = 5` in a Python file as a replacement for the `.env` step.
- Values read from environment variables are **strings** (text). If you need a number, convert it with `int()`.

We will use only this non-secret setting for the required activity. It does not require an account or network connection.

## 3. Step 1 — Set up a small practice folder

Keep your **Week 5 catalog unchanged** for now. Open your Week 6 practice folder `ecommart_venv_practice` from the earlier lessons, with its `.venv` activated. Your terminal should be in the folder containing `requirements.txt`.

The instructor's later low-stock notifier is a **different project** under `Examples/ecommart_notify/`. Today's practice is intentionally smaller.

Open `requirements.txt` and ensure it lists the dependencies required for this exercise:

```text
pytest==9.2.0
python-dotenv==1.2.4
```

These versions are the examples verified for this course on **4 November 2026**; both packages require Python 3.10 or later. If your Python version is older, update Python before following these exact pinned examples. `pytest` is for later testing; `python-dotenv` is what this lesson needs.

Install from the file:

```bash
python -m pip install -r requirements.txt
```

If Windows does not recognize `python` after activation, revisit `02_Creating_and_Activating_venv.md` and check which interpreter is active. Avoid installing into a different global environment by accident.

## 4. Step 2 — Create .env and .env.example

In `ecommart_venv_practice`, create a text file named **exactly** `.env` (the period at the beginning matters). Enter:

```dotenv
LOW_STOCK_THRESHOLD=5
```

Next, create `.env.example` with the same **safe demonstration value**:

```dotenv
LOW_STOCK_THRESHOLD=5
```

Why both files?

- `.env` is your **local working configuration**. Keep it out of version control, especially when later lessons introduce API-key placeholders or real configuration secrets in other contexts.
- `.env.example` is a **shareable template**. It shows another developer which settings to create without sharing any private values.

Create a `.gitignore` file, also in this folder, containing:

```gitignore
.venv/
.env
__pycache__/
.pytest_cache/
```

A `.gitignore` tells **Git**, a version-control tool used to track code changes, which untracked files or folders to leave out. It does **not** hide files from people who already have them, and it does not remove anything previously committed. Do not upload your local `.env` as part of a submission.

At this point, your folder looks like:

```text
ecommart_venv_practice/
├── .venv/                  # created locally; never submit
├── .env                    # your local configuration; never submit
├── .env.example            # safe template to share
├── .gitignore
└── requirements.txt
```

## 5. Step 3 — Read the setting in Python

Create `show_config.py` in the same folder:

```python
import os
from pathlib import Path

from dotenv import load_dotenv

# Locate .env beside this script, even if the terminal opens elsewhere.
project_folder = Path(__file__).resolve().parent
load_dotenv(project_folder / ".env")

# Environment-variable values arrive as text.
raw_threshold = os.getenv("LOW_STOCK_THRESHOLD", "5")
threshold = int(raw_threshold)

print(f"eComMART low-stock threshold: {threshold}")
```

Run from your practice folder with the virtual environment active:

```bash
python show_config.py
```

**Expected output:**

```text
eComMART low-stock threshold: 5
```

### Understand the new lines

- `import os` loads Python's built-in module for interacting with operating-system settings.
- `Path(__file__).resolve().parent` finds the folder where this script lives.
- `from dotenv import load_dotenv` imports a function from the installed `python-dotenv` package.
- `load_dotenv(project_folder / ".env")` reads entries from that file. By default, it does **not** overwrite an environment variable already set in the process.
- `os.getenv("LOW_STOCK_THRESHOLD", "5")` reads the setting. The second argument is a default **text** value used if the setting is missing.
- `int(raw_threshold)` converts the text into a whole number so comparison logic can later use it.

**Why use a default?** This is a beginner demonstration that still runs if the setting is absent. In a real project, some settings must be required, and then the program should report a clear error instead of silently choosing a value. We will return to validation in the configuration and testing lessons.

## 6. Step 4 — Change the setting without changing Python

1. Open `.env` and change `LOW_STOCK_THRESHOLD=5` to `LOW_STOCK_THRESHOLD=10`.
2. Save the `.env` file.
3. Run `python show_config.py` again in a **new Python process** (each terminal command above starts one).

**Expected output:**

```text
eComMART low-stock threshold: 10
```

You changed the program's behavior **without editing `show_config.py`**. That is the benefit of external configuration.

### What if the value is not a number?

Try changing the file temporarily to:

```dotenv
LOW_STOCK_THRESHOLD=ten
```

Run the script. You should see a `ValueError` because Python cannot turn the word `ten` into a whole number. Restore the value to `5` afterward.

**Learning point:** moving a setting out of code does not make the setting automatically valid. Programs still need to handle invalid configuration. You have already met this idea in Section 02 (Testing Fundamentals): a pytest test can check that an invalid setting raises the expected error. The Instructor Demo will revisit configuration validation.

## 7. Environment variables without a .env file

A `.env` file is one convenient **development** method, not the definition of an environment variable. You can also set a variable in a terminal for a running session.

**Windows PowerShell:**

```powershell
$env:LOW_STOCK_THRESHOLD = "8"
python show_config.py
```

**Windows Command Prompt:**

```cmd
set LOW_STOCK_THRESHOLD=8
python show_config.py
```

**macOS or Linux (bash/zsh):**

```bash
export LOW_STOCK_THRESHOLD=8
python show_config.py
```

**Expected output:** `eComMART low-stock threshold: 8`, even if `.env` says `5`, because `load_dotenv()` does not override an already-set environment variable by default.

To return to reading the `.env` value, open a **fresh terminal**, reactivate your `.venv`, and rerun the script. Do not worry if your terminal remembers the variable for the remainder of that session.

This terminal-based demonstration is **optional exploration**. The required task is simply to configure and read a value from `.env`.

## 8. How this connects to the rest of Week 6

**Instructor Demo — separate low-stock notifier:** It will load a setting such as `LOW_STOCK_THRESHOLD` using `config.py`. `stock_alert.py` will handle the business rule; `main.py` will coordinate them. Students will test the alert logic **locally**, without an LLM.

**Independent Challenge — your Week 5 catalog:** You will keep your catalog's functions and SQLite data while moving **at least one** hardcoded setting, such as the database file path, to a `.env` entry. The challenge will explicitly show how to avoid accidentally creating a new empty SQLite database when the path is wrong.

**Optional/stretch — Anthropic SDK:** A future AI tool might read `ANTHROPIC_API_KEY` from configuration. **For Week 6, students only configure a fake placeholder key if they explore that topic. Never enter a real key, register for an API account, or make a paid/live call for any required activity.**

## 9. Guided practice and verification

Do these steps without copying the finished code from above:

1. Explain what an environment variable is in one sentence.
2. Confirm `.venv` is active and `python-dotenv` is installed in the right environment.
3. Set `LOW_STOCK_THRESHOLD=7` in your local `.env`.
4. Run `show_config.py` and check that it prints `7`.
5. Verify that `.env.example` contains a safe sample value and `.gitignore` contains `.env`.
6. Change the `.env` value back to `5` for the next exercise.

**Success checklist**

- [ ] I can distinguish `.env` from a Python source file.
- [ ] I can explain why values from `os.getenv()` may need converting.
- [ ] I can change a local setting without editing Python logic.
- [ ] I know not to share or commit `.env`.
- [ ] I did not need an AI account or real API key.

## 10. Common mistakes and fixes

| What you see | Likely cause | What to check |
|---|---|---|
| `ModuleNotFoundError: No module named 'dotenv'` | `python-dotenv` not installed in the interpreter running the script | Activate `.venv`, then run `python -m pip install -r requirements.txt` |
| Setting always shows `5` | `.env` was not saved, the filename is wrong, or the setting is missing | Check `.env` is beside `show_config.py`, spelled exactly `.env` |
| Setting shows `8` even though `.env` says `5` | The terminal already supplied the environment variable | Open a new terminal, activate `.venv`, and retry |
| `ValueError: invalid literal for int()` | The setting is not a valid whole number | Replace `ten` with `10` or another whole number |
| `.env` appears in file-sharing or Git changes | `.gitignore` missing or file was previously tracked | Add `.env` to `.gitignore`; ask an instructor if already committed |

## 11. Knowledge check

1. Why might two eComMART developers want different values for `LOW_STOCK_THRESHOLD`?
2. Does Python automatically read `.env` without `python-dotenv` or similar setup?
3. Why do we use `int()` when reading a numeric setting?
4. Which file can safely demonstrate required variable names to a teammate: `.env` or `.env.example`?
5. If an existing system environment variable and `.env` disagree, which value does the code shown above normally use?

**Answers:** 1. They may have different local configurations; 2. No; 3. Environment settings are read as strings; 4. `.env.example`, with safe example values; 5. The already-set system environment variable.

## 12. Recap

A virtual environment isolates installed packages. A `requirements.txt` file lists what to install. An **environment variable** provides a setting without rewriting the Python program. A local `.env` file helps during development, and `.env.example` documents safe examples for teammates.

**Next:** `03_Avoiding_Hardcoded_Credentials_and_API_Keys.md` explains why configuration values containing secrets need extra care, even in a learning project.
