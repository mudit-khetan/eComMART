# Isolated AI Project Environments

## Lesson purpose

Earlier this week, you created a Python virtual environment so the packages for one eComMART project do not interfere with packages in another project. That same habit becomes even more important when an application later uses AI libraries.

In this lesson, you will make a small **local eComMART tool project** with its own `.venv`, verify which Python runs your program, and record the packages needed for testing. This is preparation for future agentic AI work — it does **not** connect to any model yet.

**Core for Week 6:** an isolated virtual environment, a reproducible dependency list, and a locally tested Python tool. **Optional/stretch:** keeping a separate environment for experiments with an AI SDK. No Anthropic account, real API key, paid service, internet-based inference, or live API call is required for any graded or required exercise.

## Learning objectives

By the end of this lesson, you will be able to:

- Explain why an AI-enabled project should have its own Python environment.
- Create and activate a new `.venv` on Windows, macOS, or Linux.
- Verify that commands refer to the intended Python installation.
- Install the local testing dependency with `pip` and record it in `requirements.txt`.
- Explain the difference between code, installed packages, dependency records, and configuration.
- Identify what **does not** belong in source control: `.venv` and real `.env` secrets.

## 1. Why AI projects especially need isolation

Imagine eComMART has three Python projects:

| Project | What it does | Packages it might need |
|---|---|---|
| Week 5 catalog | Store and retrieve products in SQLite | Python's built-in `sqlite3` |
| Week 6 low-stock notifier | Check quantities and run automated tests | `pytest`; `python-dotenv` when using a `.env` |
| Future AI assistant | Interpret requests and potentially use approved tools | An LLM provider SDK and other agent libraries **later** |

Packages are reusable code written by other developers. Different projects may need different versions of those packages. Installing all packages into one global Python installation can create conflicts and make it difficult to reproduce a working setup.

A **virtual environment** is a project-specific Python environment. It keeps that project's installed packages separate from most other projects. It does **not** by itself secure credentials, stop network access, or sandbox untrusted code. Those are different concerns.

### One project, one environment

```text
Your computer
|
+-- ecommart_catalog/          # Week 5 application, kept separate
|   +-- 05_Product_Catalog_App.py
|
+-- ecommart_tool_practice/    # Today's small practice project
|   +-- .venv/                 # Private Python environment
|   +-- stock_tool.py          # Ordinary Python logic
|   +-- test_stock_tool.py     # Local tests
|   +-- requirements.txt       # Dependency list
|   +-- .gitignore             # Files Git should ignore
|
+-- future_ai_assistant/       # Example only; not built in Week 6
    +-- .venv/                 # Could use different library versions
```

**Important continuity:** Do not turn your Week 5 catalog into the small demo project. Later, in the **independent challenge**, you will reorganize **your own Week 5 catalog** while preserving its features. This lesson is a small, separate setup exercise.

## 2. Guided setup — create a project folder

Create a folder named `ecommart_tool_practice`, open it in VS Code or your preferred editor, and open a terminal **inside that folder**.

You can check the current working folder with:

- **Windows PowerShell or Command Prompt:** `cd`
- **macOS or Linux:** `pwd`

Create the virtual environment:

| Terminal | Command |
|---|---|
| Windows (PowerShell or Command Prompt) | `py -m venv .venv` |
| macOS | `python3 -m venv .venv` |
| Linux | `python3 -m venv .venv` |

The command creates a `.venv` folder. This folder is generated on your computer; you do **not** need to share it with classmates.

### Activate it

| Terminal | Activation command |
|---|---|
| Windows PowerShell | `.\.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `.venv\Scripts\activate.bat` |
| macOS or Linux | `source .venv/bin/activate` |

After activation, many terminals show `(.venv)` before the prompt. If yours does not, check the interpreter rather than guessing.

**PowerShell note:** If activation is blocked by an execution-policy error, use Command Prompt and its activation command instead of casually changing system-wide security settings. For more detail, revisit `03_Virtual_Environments/02_Creating_and_Activating_venv.md`.

## 3. Verify the Python you are using

With `.venv` active, run:

```bash
python -c "import sys; print(sys.executable)"
```

**Expected result:** a path containing this project's `.venv` directory, such as:

```text
.../ecommart_tool_practice/.venv/bin/python
```

On Windows, the ending will look more like `.venv\Scripts\python.exe`. Your exact drive or home directory will differ.

Next run:

```bash
python -m pip --version
```

This should describe `pip` associated with the active environment. Using **`python -m pip`** tells the current Python interpreter to run its own package installer. This is clearer for beginners than assuming a standalone `pip` command always points to the right interpreter.

> **Remember:** `.venv` is a folder with a Python environment. It is not a Python file and should never be imported with `import .venv`.

## 4. Install only what the local project needs

For this project, the stock rule uses built-in Python functionality. We need `pytest` only because we will automate checks.

With the new environment active:

```bash
python -m pip install pytest
```

Then verify:

```bash
python -m pytest --version
```

**Expected result:** a line showing a pytest version, such as `pytest 9.x.x`. Your number may differ because releases change. This lesson does not depend on a particular patch version; the `requirements.txt` lesson explains how to record the exact version you actually installed.

Create a dependency file from the environment:

```bash
python -m pip freeze > requirements.txt
```

Open `requirements.txt`. It records the installed packages and versions. A `pip freeze` file may include helper dependencies installed alongside pytest; that is normal. **Do not copy a version number from an old lesson simply because it looks familiar.** Record the packages installed in your active environment.

### Why the record matters

Without `requirements.txt`, another student might not know what you installed. With it, they can create their own `.venv` and run:

```bash
python -m pip install -r requirements.txt
```

That recreates the recorded package versions as long as compatible packages are available for their Python version and platform. It does not transfer the original `.venv` folder or guarantee identical operating-system behavior.

### What about the Anthropic SDK?

**Optional/stretch only — do not install it for this exercise.** A later lesson introduces the Anthropic Python SDK as an example of an LLM-provider dependency. The core Week 6 notifier and your own catalog challenge do not need it, so it should not be added to this small project's `requirements.txt` just to make the project seem more AI-related.

## 5. Add the small Python tool and its test

Reuse the deterministic rule you learned in the previous lesson. Create `stock_tool.py`:

```python
# stock_tool.py

def is_low_stock(stock, threshold):
    if not isinstance(stock, int) or isinstance(stock, bool):
        raise ValueError("stock must be a whole number")
    if not isinstance(threshold, int) or isinstance(threshold, bool):
        raise ValueError("threshold must be a whole number")
    if stock < 0 or threshold < 0:
        raise ValueError("stock and threshold cannot be negative")
    return stock < threshold
```

Create `test_stock_tool.py`:

```python
# test_stock_tool.py
import pytest
from stock_tool import is_low_stock


def test_stock_below_threshold():
    # Arrange
    stock, threshold = 4, 10
    # Act
    result = is_low_stock(stock, threshold)
    # Assert
    assert result is True


def test_stock_at_threshold():
    assert is_low_stock(10, 10) is False


def test_negative_stock_is_rejected():
    with pytest.raises(ValueError):
        is_low_stock(-1, 10)
```

From the **`ecommart_tool_practice` project root**, run:

```bash
python -m pytest -q
```

**Expected result:** `3 passed`. All tests run locally; no key or internet request is involved. If a test fails, read the assertion and check that you used `<` instead of `<=` in the stock function.

## 6. Keep generated files and secrets out of Git

**Git** is a tool that records changes to project files; you encountered its role in team collaboration earlier in the course. Some files are meant to be shared, while others should stay local.

Create a `.gitignore` text file with:

```gitignore
.venv/
__pycache__/
.pytest_cache/
.env
```

| File or folder | Share in the project? | Why? |
|---|---|---|
| `stock_tool.py` | Yes | Contains the application logic |
| `test_stock_tool.py` | Yes | Shows how to verify the logic |
| `requirements.txt` | Yes | Records dependencies |
| `.gitignore` | Yes | Documents what should remain local |
| `.venv/` | No | Generated environment; rebuild from requirements |
| `.env` | No | May contain private configuration or secrets |
| `.env.example` | Yes, if used | Shows setting names with harmless placeholder values |

An `.env` file is a convenient local place for configuration values, but **it is not a security boundary**. Do not put real credentials in lesson files, screenshots, repositories, or test code. In Week 6, any Anthropic key mentioned in lessons should be a **clearly fake placeholder**, never a credential used for a live request.

**Important:** Adding `.env` to `.gitignore` does not remove a secret from Git if it was already committed. If a real secret is exposed, it must be revoked or rotated. That scenario is outside the required hands-on work.

## 7. Checkpoint — can another student reproduce it?

Your local project should now look like:

```text
ecommart_tool_practice/
├── .venv/                # generated locally, not shared
├── .gitignore
├── requirements.txt
├── stock_tool.py
└── test_stock_tool.py
```

To check that you understood the process, answer:

1. Which file records packages another student should install?
2. Which folder is created automatically by `python -m venv .venv`?
3. Which command checks the stock-rule tests?
4. Why do we use `python -m pip` instead of blindly trusting `pip`?
5. Does creating `.venv` automatically protect API credentials?

**Self-check:** (1) `requirements.txt`. (2) `.venv/`. (3) `python -m pytest -q` from the project root. (4) It uses the package installer for the selected Python interpreter. (5) No; secure configuration and access controls are separate responsibilities.

### Guided challenge — spot the environment mistake

A classmate activates the Week 6 project environment, changes directory to an unrelated project, and installs a package there without checking the interpreter. The current folder and the active environment are **different concepts**. Changing folders does not automatically change the active environment. Ask the classmate to run:

```bash
python -c "import sys; print(sys.executable)"
```

That confirms which Python is currently selected before any installation takes place.

## 8. Common mistakes and troubleshooting

| What you see | Likely cause | Fix |
|---|---|---|
| `python` command not found | Environment not active, or your system uses `python3` | Activate `.venv`; check Python installation and the earlier setup lesson |
| `No module named pytest` | Installed into a different Python environment | Check `sys.executable`; install with the selected `python -m pip` |
| `ERROR: file or directory not found: test_stock_tool.py` | Terminal in the wrong folder | Open the `ecommart_tool_practice` project root |
| Tests fail on equal stock | Business rule changed | Use `stock < threshold`, not `stock <= threshold` |
| `.venv` is accidentally shared | Virtual environment was treated like source code | Add `.venv/` to `.gitignore`; share `requirements.txt` |
| `requirements.txt` is empty | Package was installed elsewhere, or the wrong environment was active | Verify interpreter and pytest, then regenerate the dependency file |
| Worried about AI API charges | AI libraries were mentioned | No live API use or real key is required in this lesson or Week 6 required work |

## 9. Core versus optional/stretch

| Core — do this | Optional/stretch — only if curious |
|---|---|
| Create and activate `.venv` | Compare two different project environments |
| Verify the selected Python | Read about dependency conflicts in future AI packages |
| Install pytest and create `requirements.txt` | Experiment with SDK package installation in a separate environment later |
| Run the three local tests | Explore advanced dependency management tools later |
| Keep `.venv` and `.env` out of Git | Explore test mocking later |

The **required Week 6 takeaway** remains the same: restructure your **own Week 5 catalog** with a virtual environment, `requirements.txt`, at least one environment variable, suitable module separation, and **2–3 simple pytest tests**. This guided practice does not change the minimum or require an AI connection.

## Lesson recap

- Isolate each Python project so dependency changes are easier to understand and manage.
- Verify the actual interpreter before installing packages or running tests.
- Share source code and `requirements.txt`, **not** `.venv` or real `.env` credentials.
- Deterministic tool functions can be tested locally without an LLM.
- **Core:** working Python environment and tests. **Optional/stretch:** provider SDKs or other agent libraries later, never a paid or live API requirement this week.

**Next lesson:** `02_Managing_the_Anthropic_SDK_and_Agent_Dependencies.md` introduces how a future LLM SDK fits into dependency management. It is conceptual/optional, not a required signup or API activity.
