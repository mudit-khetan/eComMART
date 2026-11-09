# Instructor Demo — Setting Up venv and requirements.txt

## Lesson purpose

In the previous demo lesson, eComMART's warehouse team requested a small tool that warns when a product's available stock falls below a reorder threshold. Before writing the alert rule, we need to give the new project a predictable place to run.

You will watch the instructor create a **fresh eComMART low-stock notifier project**, isolate its Python packages in `.venv`, install two small dependencies, and record them in `requirements.txt`. These habits make it much easier for a second developer to run the same project later.

**Keep the projects separate:** this is the **new Instructor Demo**, not a rewrite of your Week 5 `05_Product_Catalog_App.py`. You will organize **your own Week 5 catalog** in the independent challenge in `07_Practice_and_Review/`.

**Core:** a virtual environment, a dependency file, and working local commands. **Optional/stretch:** an Anthropic SDK integration will be discussed later, but is **not** installed for the core demo. No Anthropic signup, real API key, paid usage, or live LLM call is required for any Week 6 graded or required work.

## Learning objectives

By the end of this walkthrough, you should be able to:

- Create the correct demo project folder without overwriting your Week 5 files.
- Describe why `.venv/` is local to one project.
- Create and activate a virtual environment on Windows, macOS, or Linux.
- Install `pytest` and `python-dotenv` from a short dependency list.
- Verify which Python and package versions your active environment is using.
- Explain why the `.venv/` folder is **not** distributed, while `requirements.txt` **is**.

## 1. The eComMART setup problem

Imagine the instructor writes `main.py` today, then sends it to another eComMART developer. That developer has Python installed but does not know which extra packages are needed. The script may fail even if its stock-alert rule is correct.

We will use two tools together:

| Tool | Beginner meaning | eComMART use |
|---|---|---|
| `venv` | Creates a separate, local environment for one Python project | Keeps this demo's installed packages separate from other projects |
| `pip` | Installs Python packages | Installs our testing and `.env` helper packages |
| `requirements.txt` | Text file listing packages and versions | Lets another developer recreate the setup |

A virtual environment is **not** a second copy of your entire application. It is mainly a separate place for the Python interpreter setup and installed packages.

## 2. Starting folder: choose one location

In VS Code (or another editor), create a new folder named `ecommart_notify`. You may put it in your own practice workspace. The course reference code will later be supplied under `Week 6/Examples/ecommart_notify/`.

**Do not create `ecommart_notify` inside your Week 5 catalog folder, and do not rename your Week 5 catalog script.** For this demo, open **the `ecommart_notify` folder itself** in VS Code using **File → Open Folder**. Open the terminal in that folder.

Your starting layout is:

```text
ecommart_notify/
    # empty at first
```

To check where your terminal is:

| Terminal | Show current folder |
|---|---|
| Windows PowerShell | `Get-Location` |
| Windows Command Prompt | `cd` |
| macOS/Linux | `pwd` |

**Expected:** the location ends with `ecommart_notify`. If not, open the correct folder or use `cd` with the actual folder path on your computer. Avoid copying somebody else's absolute folder path.

## 3. Step 1 — Check Python

Use the command matching your system **before** creating the environment:

| System | Command |
|---|---|
| Windows | `py --version` |
| macOS/Linux | `python3 --version` |

**Expected:** a result beginning with `Python 3`, for example `Python 3.12.x`. For the pinned package versions in this demo, use **Python 3.10 or newer**. If the command says it cannot find Python, install an appropriate Python 3 version first and reopen the terminal.

> **Instructor interaction:** Ask learners: “If another developer has a different set of globally installed Python packages, will that automatically make our new project reliable?” **Answer:** No; that is one reason we use an isolated environment.

## 4. Step 2 — Create `.venv`

From inside `ecommart_notify/`, run **one** of the following commands:

| System | Create environment |
|---|---|
| Windows PowerShell or Command Prompt | `py -m venv .venv` |
| macOS/Linux | `python3 -m venv .venv` |

Let's decode the command:

- `py` or `python3`: starts Python.
- `-m venv`: tells Python to run its built-in virtual-environment tool.
- `.venv`: names the folder to create inside this project.

**Expected:** a new `.venv/` folder appears. The command may finish without printing any message; that is normal. You do not edit the files inside `.venv/` manually.

## 5. Step 3 — Activate the environment

Run the command for **your terminal**, from the `ecommart_notify/` folder:

| Terminal | Activation command |
|---|---|
| Windows PowerShell | `.\.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `.venv\Scripts\activate.bat` |
| macOS/Linux bash/zsh | `source .venv/bin/activate` |

On many terminals, the prompt changes to begin with `(.venv)`. The prompt is a **hint**, not the only proof of activation. Verify using:

```bash
python -c "import sys; print(sys.prefix); print(sys.executable)"
```

**Expected:** the paths refer to the `.venv` folder within `ecommart_notify`. Exact paths differ by computer.

If PowerShell blocks the activation script, see **Troubleshooting** below. Avoid changing security settings globally just to complete this lesson. The alternative is to run the environment's Python executable directly (also shown below).

### If you cannot activate yet

The environment can still be used by calling its Python directly:

| Terminal | Verify environment Python without activation |
|---|---|
| Windows PowerShell / Command Prompt | `.venv\Scripts\python.exe --version` |
| macOS/Linux | `.venv/bin/python --version` |

If you use this alternative, substitute the same environment Python executable for `python` in all remaining commands. This prevents packages from accidentally being installed outside the demo environment.

## 6. Step 4 — Create requirements.txt

In the **root** of `ecommart_notify/`, create a new plain-text file named `requirements.txt`. Add exactly these **core** packages:

```text
python-dotenv==1.2.4
pytest==9.2.0
```

These package versions were checked against their official PyPI project pages for this Week 6 material (4 November 2026):

- `python-dotenv` loads settings from a local `.env` file in the next lesson.
- `pytest` runs our automated tests in the following demo lesson.

`==` means “install exactly this version.” A **dependency** is software our program relies on but that we did not write ourselves. The `os` module we will use later is part of Python's standard library and does **not** belong in `requirements.txt`.

**Why not add Anthropic here?** The core stock notifier and its tests must run without an LLM. The optional `anthropic_client.py` file will be clearly marked **stretch only**; it is not imported by the core program. Keeping `anthropic` out of the core requirements avoids unnecessary installation for beginners.

The folder now looks like:

```text
ecommart_notify/
├── .venv/               # made locally; do not share
└── requirements.txt     # share this file with the project
```

## 7. Step 5 — Install and verify the packages

With the environment activated (or using its Python executable as explained above), run:

```bash
python -m pip install -r requirements.txt
```

Read this as: “Use this Python interpreter to run pip, and install the package versions listed in `requirements.txt`.” The first install may show several dependency downloads; that is normal. These dependencies require an internet connection for the *initial installation*, but **not** a paid account or AI API connection. If packages are already cached, downloads may not occur.

Verify:

```bash
python -m pip show python-dotenv
python -m pytest --version
```

**Expected results:**

- The first command prints package information including `Name: python-dotenv` and `Version: 1.2.4`.
- The second prints `pytest 9.2.0`.

Exact terminal formatting may vary. If the versions differ, check the file contents, the activated interpreter, and whether installation completed successfully.

**Do not use `pip freeze` as the primary way to write this simple demo's requirements file.** It lists extra indirect dependencies as well. Our two-line file deliberately records the two top-level packages we chose. The earlier dependency lesson explains when `pip freeze` is useful.

## 8. Step 6 — Protect local-only files

The official distributed example's file plan does not include an additional `.gitignore`, but you should know the safe rule: **never share or commit your local `.venv/` or `.env` files**. If you later manage the project with Git, create a local `.gitignore` containing:

```gitignore
.venv/
.env
__pycache__/
.pytest_cache/
```

Do not add `.env` yet; the next demo lesson will create it. `requirements.txt` **should** be shared, and `.env.example` will be a safe template. The word “commit” means saving a set of changes in a version-control tool such as Git; Git itself is not required in this Week 6 demo.

## 9. Quick instructor check: does a second environment work?

Ask learners to identify the correct answer before showing it:

**Question:** A teammate receives `requirements.txt` but not your `.venv/`. What should they do?

1. Copy your `.venv/` folder from your machine.
2. Create their **own** virtual environment and run `python -m pip install -r requirements.txt`.
3. Put all dependencies inside `main.py`.

**Answer: 2.** Environment folders can contain machine-specific paths and executables. The shareable dependency list is what a teammate needs.

## 10. Troubleshooting

| What you see | Likely cause | Beginner-friendly fix |
|---|---|---|
| `python` or `py` not found | Python not installed or unavailable in this terminal | Confirm Python 3 installation; reopen terminal; retry correct OS command |
| `No module named venv` | Incomplete Python installation | Install the OS Python venv support package or a standard Python distribution, then retry |
| PowerShell says scripts are disabled | Local script execution policy prevents activation | Use `.venv\Scripts\python.exe` directly for package and program commands; do not modify system-wide policy |
| `Could not open requirements file` | Terminal in wrong folder or wrong filename | Confirm you are in `ecommart_notify` and the file is exactly `requirements.txt` |
| `No module named pytest` | Pytest installed for another Python interpreter or installation failed | Activate `.venv`, then run `python -m pip install -r requirements.txt` again |
| “No matching distribution” | Old Python or unsupported platform/version | Confirm Python is 3.10+ and inspect the package error; do not invent a package version |
| Editor cannot find installed packages | Editor selected a different Python interpreter | In VS Code, select the interpreter inside the project's `.venv/` |

## 11. Guided practice — 5-minute learner task

Without copying commands from another student's terminal:

1. Show the instructor where your new `ecommart_notify` folder is.
2. Point to `.venv/` and explain why you should not email that folder to a teammate.
3. Read both lines of `requirements.txt` aloud in plain English.
4. Run `python -m pytest --version` through the project environment.
5. Predict what another developer needs to recreate this environment.

**Self-check:** You can find `.venv/`, explain the purpose of the two packages, and run a command showing the selected pytest version. Your Week 5 catalog has not been changed.

## 12. Takeaway and next step

You have created an **isolated project**, a **reproducible dependency list**, and a **working local toolchain**. You have **not** made any LLM calls, and you have not changed the Week 5 catalog.

Next: `03_Refactoring_into_Modules_and_env_Config.md` will add `stock_alert.py`, `config.py`, `.env.example`, a local `.env`, and `main.py`. We will keep the business rule deterministic so that tests can verify it without the network.
