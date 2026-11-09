# API Key Configuration for Claude

## Lesson purpose

In the previous lesson, you learned that an SDK is a Python library that could help a future eComMART application use an external AI service. Such services normally need a credential (an API key) to identify an authorized account. Week 6 is about **how to keep configuration separate from code**, not about using a paid AI service.

**Important: Every student uses only a FAKE placeholder `ANTHROPIC_API_KEY` in `.env` this week. Do not create an Anthropic account, obtain or enter a real API key, add a payment method, or make any live API call for a required or graded Week 6 activity. There is no real API cost or signup requirement.**

**Core for Week 6:** configure and read at least one environment variable (for example `LOW_STOCK_THRESHOLD`) safely. **Optional/stretch:** add and locally validate a fake `ANTHROPIC_API_KEY` placeholder. The Anthropic SDK, real keys, network requests, and test mocking are **not required**.

## Learning objectives

By the end of this lesson, you will be able to:

- Describe what an API key does without confusing it with a Python package.
- Explain the roles of `.env`, `.env.example`, `.gitignore`, and `os.getenv()`.
- Configure a real *non-secret* application setting for eComMART.
- Add a clearly fake Anthropic key placeholder for optional practice.
- Check whether a key has been configured without displaying it.
- Tell the difference between **configured**, **valid**, and **actually connected**.
- Avoid committing secrets or sending live API requests.

## 1. eComMART's two kinds of settings

Imagine eComMART wants a stock alert when fewer than five items remain. That threshold is ordinary configuration. A future AI service, however, may require a secret credential.

| Setting | Example | Purpose | Required this week? |
|---|---|---|---|
| `LOW_STOCK_THRESHOLD` | `5` | Controls alert decisions | **Yes — use this as your one environment variable** |
| `ANTHROPIC_API_KEY` | `YOUR_PLACEHOLDER_KEY_HERE` | Illustrates where a future service key would go | **No — optional placeholder only** |

An **environment variable** is a named setting accessible to a running program. A `.env` file is a convenient local text file containing `NAME=value` lines. Python does not automatically load `.env`; a package such as `python-dotenv` can read it into the program's environment.

An API key is like a credential for a service, not a setting that makes Python smarter. **A made-up key can be read as text, but it cannot authorize a Claude request.**

## 2. The project files and their responsibilities

Use the earlier local practice project or a small new folder named `ecommart_config_practice`. This is not a refactor of your Week 5 catalog; that happens in the independent challenge.

```text
ecommart_config_practice/
├── .venv/                  # Generated environment; don't share
├── .env                    # Local settings; don't commit or submit
├── .env.example            # Safe template; share this
├── .gitignore              # Ignore private/generated files
├── config.py               # Reads and checks settings
├── check_config.py         # Local verification only
└── requirements.txt        # Python dependencies, NOT credentials
```

**Core dependencies:** `python-dotenv` for `.env` loading, and `pytest` for later tests. No `anthropic` package is necessary for this lesson.

From the project directory, create and activate a virtual environment if you do not already have one:

| System | Create | Activate |
|---|---|---|
| Windows PowerShell | `py -m venv .venv` | `.\.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `py -m venv .venv` | `.venv\Scripts\activate.bat` |
| macOS / Linux | `python3 -m venv .venv` | `source .venv/bin/activate` |

Run:

```bash
python -m pip install python-dotenv pytest
python -m pip freeze > requirements.txt
```

Open `requirements.txt` to confirm `python-dotenv` and `pytest` are listed. Your installed versions may vary. This file should **never** contain a real key or `.env` contents.

## 3. Create `.env` and the shareable template

Create `.env` next to `config.py`:

```dotenv
LOW_STOCK_THRESHOLD=5
# OPTIONAL fake example only. NOT a working Anthropic credential.
ANTHROPIC_API_KEY=YOUR_PLACEHOLDER_KEY_HERE
```

**Required work uses only `LOW_STOCK_THRESHOLD`.** Including the second line is optional learning practice. Use **exactly a placeholder**, never a real key in this course.

Create `.env.example`:

```dotenv
# Copy this file to .env and edit local settings.
LOW_STOCK_THRESHOLD=5
# OPTIONAL: placeholder only; no API usage in Week 6.
ANTHROPIC_API_KEY=YOUR_PLACEHOLDER_KEY_HERE
```

Create `.gitignore`:

```gitignore
.venv/
.env
__pycache__/
.pytest_cache/
*.pyc
```

`.gitignore` tells Git not to start tracking these files. **If a secret was previously committed, adding `.gitignore` does not erase it from history.** Never put real keys into classroom examples or screenshots.

## 4. Read the required threshold — core hands-on

Create `config.py`:

```python
import os

from dotenv import load_dotenv

load_dotenv()


def get_low_stock_threshold():
    """Read a whole-number stock threshold from local configuration."""
    text_value = os.getenv("LOW_STOCK_THRESHOLD", "5")

    try:
        threshold = int(text_value)
    except ValueError as error:
        raise ValueError("LOW_STOCK_THRESHOLD must be a whole number") from error

    if threshold < 0:
        raise ValueError("LOW_STOCK_THRESHOLD cannot be negative")

    return threshold
```

**Why each part matters:**

1. `load_dotenv()` loads settings from `.env` into the Python process if they are not already defined.
2. `os.getenv()` reads the named setting; `"5"` is a fallback if the variable is absent.
3. `int(...)` converts text (such as `"5"`) to an integer (`5`).
4. The error checks help prevent unclear or invalid configuration.

Create `check_config.py`:

```python
from config import get_low_stock_threshold

print("eComMART low-stock threshold:", get_low_stock_threshold())
```

Run:

```bash
python check_config.py
```

**Expected output:**

```text
eComMART low-stock threshold: 5
```

Change `LOW_STOCK_THRESHOLD=3` in `.env`, run the script again, and confirm it prints `3`. This demonstrates changing behavior **without editing Python source**.

**Troubleshooting note:** an already-set operating-system environment variable with the same name normally takes precedence over `.env` when using the default `load_dotenv()` behavior. If changing `.env` does not affect the output, inspect whether `LOW_STOCK_THRESHOLD` is set in the terminal or IDE environment.

## 5. Optional/stretch — check a fake key without exposing it

This next practice only confirms a placeholder was loaded. It does **not** validate a real credential and makes **no network request**.

Add the following to the end of `config.py`:

```python
def get_fake_key_configuration_status():
    """Report local placeholder status; never reveal a key's contents."""
    value = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if value == "YOUR_PLACEHOLDER_KEY_HERE":
        return "Fake training placeholder is configured (no API access)"
    if not value:
        return "No placeholder is configured (also fine for core work)"
    return "Unexpected value present; do not use or print it"
```

In a new file called `check_placeholder.py`, write:

```python
from config import get_fake_key_configuration_status

print(get_fake_key_configuration_status())
```

Run:

```bash
python check_placeholder.py
```

**Expected output when the fake placeholder is present:**

```text
Fake training placeholder is configured (no API access)
```

This status only says that the expected *fake string* was found. It does not prove that the key is real, valid, authorized, or that Claude has been contacted. If an unexpected value is present, stop, do not display it, and replace it with the fake placeholder for training.

> **Do not add an Anthropic client or `messages.create(...)` request here.** No SDK call is necessary, even for the optional placeholder exercise.

## 6. How this connects to a future Claude integration

In a future, separately authorized project, a developer might read `ANTHROPIC_API_KEY` into an SDK client. In Week 6, you need to understand only the **configuration pathway**:

```text
Local .env file
    |
    v
python-dotenv loads named settings
    |
    v
Python uses os.getenv("ANTHROPIC_API_KEY")
    |
    v
Week 6: check FAKE placeholder only -- STOP HERE
    |
    v
Future course topic: authorized API client and live calls (NOT this week)
```

**Three different questions:**

- **Configured?** Is a value present in local settings? You can check this without a network call.
- **Valid?** Would a service accept the value? A fake key cannot establish this; Week 6 does not test it.
- **Connected?** Has your application successfully contacted the service? Week 6 deliberately does **not** attempt this.

## 7. Common mistakes and troubleshooting

| Symptom | Likely reason | Solution |
|---|---|---|
| `ModuleNotFoundError: No module named 'dotenv'` | Package isn't installed in current venv | Activate `.venv`; run `python -m pip install python-dotenv` |
| Script prints `5` after editing `.env` to `3` | A shell/IDE variable may override `.env` | Check your environment; try a new clean terminal |
| `LOW_STOCK_THRESHOLD must be a whole number` | `.env` contains letters or a decimal | Use a whole number such as `5` |
| File is named `.env.txt` | Editor automatically added `.txt` | Rename it to exactly `.env` |
| Student commits `.env` | Private file not ignored, or already tracked | Stop sharing; ask instructor for secure cleanup guidance |
| Fake key fails authentication | Placeholders are not real credentials | **Do not try to authenticate. No API call is needed.** |
| `requirements.txt` contains a key | Confusing dependencies with configuration | Remove any credential; keep only package requirements |

## 8. Guided practice and quick checks

**Core practice (required, approximately 10–15 minutes):**

1. Create `.env` and set `LOW_STOCK_THRESHOLD=5`.
2. Use `load_dotenv()` and `os.getenv()` to load that value in Python.
3. Run the script and confirm the value is displayed as an integer.
4. Change the threshold to `3` without editing the Python code; run again.
5. Keep `.env` out of submissions and share `.env.example` instead.

**Optional/stretch:** add `ANTHROPIC_API_KEY=YOUR_PLACEHOLDER_KEY_HERE`, run the *local* status check, and explain why the result does not mean that any service is connected.

**Knowledge check:**

- **Q:** Is `.env` automatically loaded by Python? **A:** No; in this example `python-dotenv` loads it.
- **Q:** Should `ANTHROPIC_API_KEY` be copied into `requirements.txt`? **A:** No.
- **Q:** Is a fake key enough to run a Claude API call? **A:** No; and no such call is required this week.
- **Q:** What is the minimum required environment-variable work? **A:** Configure and read one local variable such as `LOW_STOCK_THRESHOLD`.

## 9. Recap and next steps

You have practiced separating eComMART settings from Python source code, safely documenting settings with `.env.example`, and verifying local configuration. You have **not** signed up for or called an AI service.

Next, `04_Testing_Deterministic_Tools_Before_Connecting_an_LLM.md` will show why deterministic stock-check functions should pass ordinary pytest tests **before** any future AI integration is considered.

### References

- Python `os.getenv()` documentation: <https://docs.python.org/3/library/os.html#os.getenv>
- `python-dotenv` documentation: <https://pypi.org/project/python-dotenv/>
- Anthropic Python SDK (future reference only): <https://github.com/anthropics/anthropic-sdk-python>
