# Creating and Activating a Python Virtual Environment

## Learning objectives

By the end of this lesson, you will be able to:

- Check that Python 3 is available from your terminal.
- Open the correct project folder before running commands.
- Create a `.venv` environment using Python's built-in `venv` module.
- Activate and deactivate the environment on Windows, macOS, or Linux.
- Verify which Python interpreter is in use rather than relying only on the prompt display.
- Recognize and fix common beginner setup problems without changing system-wide settings unnecessarily.

## 1. Where we are in the eComMART story

In the previous lesson, you learned why separate projects benefit from separate Python environments. Now you will set one up yourself.

For this practice, we will use a **small disposable learning folder**, not your existing Week 5 product catalog. You do not need to change `05_Product_Catalog_App.py` or touch its SQLite database yet. Later, the instructor will use the same approach when building the new eComMART low-stock notifier, and your independent takeaway will apply it to your own Week 5 catalog.

**Core for Week 6:** these environment commands are part of the required work. **No API account, API key, Anthropic SDK, or paid service is needed.**

## 2. Know the parts of a terminal command

A **terminal** is an application where you type commands. In Visual Studio Code, you can open one from **Terminal → New Terminal**. You may also use PowerShell or Command Prompt on Windows, or Terminal on macOS and Linux.

You will see commands like this:

```bash
python -m venv .venv
```

Read it from left to right:

- `python` runs the Python interpreter (the program that executes Python code).
- `-m` tells Python to run a named module.
- `venv` is Python's built-in virtual-environment module.
- `.venv` is the name of the folder Python should create.

On Windows, `py` commonly launches Python 3; on macOS and Linux, `python3` is often the Python 3 command. This lesson shows the appropriate commands for each operating system.

**Do not type the leading `$`, `>`, or `(.venv)` if your terminal displays them as part of its prompt.** Type only the command itself.

## 3. Step 1 — Check Python 3

Open a terminal and enter the command for your operating system:

**Windows (PowerShell or Command Prompt):**

```powershell
py --version
```

If `py` is unavailable but Python is installed, try `python --version` instead.

**macOS or Linux:**

```bash
python3 --version
```

Expected result (your actual version may be different):

```text
Python 3.x.y
```

You need a working Python 3 installation with `venv`. If the command is not found, check the installation instructions provided for your computer before continuing. If your device is managed by an organization, ask your instructor or support team rather than installing software without permission.

**Remember:** `--version` reports a version; it does not create or change files.

## 4. Step 2 — Make and open a practice project folder

Choose a place on your computer where you can create files. In VS Code, you can create a folder using your file manager, then select **File → Open Folder** and open it. Name the folder:

```text
ecommart_venv_practice
```

Open **Terminal → New Terminal** while that folder is open. Before creating the environment, confirm your terminal is in the right folder.

**Windows (PowerShell or Command Prompt):**

```powershell
cd
```

`cd` without an argument behaves differently between shells, so for a reliable check use the following command in **PowerShell**:

```powershell
Get-Location
```

In **Command Prompt**, use:

```bat
cd
```

**macOS or Linux:**

```bash
pwd
```

The output should end with `ecommart_venv_practice` (the beginning of the path depends on where you created the folder). If not, open the correct folder in VS Code or navigate to it before continuing.

> **Why the folder matters:** `venv` creates `.venv` inside the directory from which you run the command. Running it from the wrong folder makes the environment difficult to find later.

## 5. Step 3 — Create `.venv`

Run **one** command for your operating system, from inside `ecommart_venv_practice`:

| Operating system | Command |
|---|---|
| Windows | `py -m venv .venv` |
| macOS | `python3 -m venv .venv` |
| Linux | `python3 -m venv .venv` |

If you confirmed that `python` works but `py` does not on Windows, you may use `python -m venv .venv`.

Usually a successful command displays **no message** and simply returns to the prompt. This is normal.

The folder should now look approximately like this:

```text
ecommart_venv_practice/
└── .venv/
    ├── ... environment files ...
    └── ... installed-package directory ...
```

The exact files inside `.venv` differ between Windows and macOS/Linux. You do not need to edit them yourself.

### Quick verification

In VS Code's file explorer, check that `.venv` appears inside your practice folder. If it is hidden, use your file explorer's option to display hidden files, or check in the terminal:

**Windows PowerShell:**

```powershell
Test-Path .venv
```

Expected result: `True`.

**macOS/Linux:**

```bash
ls -a
```

Expected result: the listing includes `.venv`.

## 6. Step 4 — Activate the environment

**Activation changes the Python commands used by the current terminal session.** It does not turn the environment into a running server or modify your database.

Choose the row that matches both your operating system **and your terminal**:

| Operating system / terminal | Activate `.venv` |
|---|---|
| Windows — PowerShell | `.\.venv\Scripts\Activate.ps1` |
| Windows — Command Prompt | `.venv\Scripts\activate.bat` |
| macOS — Terminal / zsh / bash | `source .venv/bin/activate` |
| Linux — bash / compatible shell | `source .venv/bin/activate` |

On Windows, the PowerShell command uses backslashes and begins with `.\` to indicate a script in the current folder. On macOS and Linux, the command uses forward slashes.

**Example on Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Example on macOS/Linux:**

```bash
source .venv/bin/activate
```

Your prompt will commonly change from something like:

```text
ecommart_venv_practice>
```

to:

```text
(.venv) ecommart_venv_practice>
```

Seeing `(.venv)` is useful, but prompt customization may hide it. The next step confirms which Python interpreter the terminal actually uses.

## 7. Step 5 — Verify the active Python

While the environment is activated, run:

```bash
python -c "import sys; print(sys.executable)"
```

Here, `-c` tells Python to run the short Python statement inside the quotation marks. `sys.executable` tells you the path of the Python interpreter currently running.

Expected result: a path that includes **your practice folder's `.venv`**. For example:

**Windows (illustrative path):**

```text
C:\Users\Student\Projects\ecommart_venv_practice\.venv\Scripts\python.exe
```

**macOS/Linux (illustrative path):**

```text
/home/student/projects/ecommart_venv_practice/.venv/bin/python
```

Your real path will be different. What matters is the `.venv` portion and the location inside your practice project.

### Optional second check

You can also run:

```bash
python -m pip --version
```

This reports the version and location of `pip`, Python's package installer. Look for a path under `.venv`. If `pip` is missing, see the troubleshooting section; the next lesson will cover installing packages.

**Why use `python -m pip` instead of a bare `pip` command?** It explicitly uses the `pip` module belonging to the Python interpreter named by `python`. This helps prevent installing a package into the wrong Python installation.

## 8. Step 6 — Deactivate when you are finished

Type:

```bash
deactivate
```

This command works in the common activation shells shown above. The `(.venv)` indicator normally disappears. Your terminal's `python` command may now point back to another Python installation.

The `.venv` directory **still exists**; deactivation does not delete it. You can activate the same environment again whenever you return to the project.

### Check your understanding

| Action | Creates/deletes `.venv`? | Changes the current terminal's Python selection? |
|---|---|---|
| `python -m venv .venv` | Creates it | No activation by itself |
| Activate script | No | Yes |
| `deactivate` | No | Restores previous terminal setup |

## 9. Guided practice — repeat the full setup

Try these steps without copying an existing `.venv` from another project:

1. Open `ecommart_venv_practice` in VS Code.
2. Open a terminal **inside that folder**.
3. Confirm the Python 3 version using the command for your OS.
4. Create `.venv` if it does not exist. If it already exists from your first attempt, keep it; you do not need to recreate it.
5. Activate the environment using the command for your shell.
6. Run `python -c "import sys; print(sys.executable)"`.
7. Check that the reported interpreter path contains the practice folder's `.venv`.
8. Run `deactivate`, then activate the environment once more to practise returning to a project.

### Your expected evidence

When finished, you should be able to show:

- A local `ecommart_venv_practice/.venv/` folder.
- A terminal with the environment activated.
- An interpreter path pointing into that project's `.venv`.

You have not installed any extra third-party packages yet. That is intentional; the following lesson will introduce `pip`.

## 10. Common errors and how to fix them

### Error: `py` or `python3` is not recognized

**Likely cause:** Python 3 is not installed, is not accessible in your terminal, or the command differs on your system.

**What to do:** Check your Python installation, reopen the terminal, and rerun the version check. Windows users can try `python --version` if `py` is unavailable. On managed devices, ask your instructor or IT team to verify the setup.

### Error: `No module named venv` or an `ensurepip` error on Linux

**Likely cause:** The installed Python distribution does not include the required virtual-environment support package.

**What to do:** Follow the guidance shown by your operating system or Python distribution. Some Linux distributions provide a separately installed system package such as `python3-venv`. If you do not have permission to install system packages, ask your instructor or administrator. Do **not** try to fix this by randomly installing packages into the system Python.

### Error: PowerShell says script execution is disabled

**Likely cause:** Your PowerShell execution policy blocks activation scripts.

**Simple course workaround:** Open **Command Prompt** in the same project folder and use:

```bat
.venv\Scripts\activate.bat
```

You can also ask your organization's support team for its approved PowerShell procedure. Do not change machine-wide security policies just to finish this exercise.

### Error: terminal says activation script does not exist

**Likely cause:** You are not in the project folder, `.venv` was not created successfully, or you used a command for the wrong operating system/shell.

**What to do:** Verify the current folder, check that `.venv` exists, and match the activation command to your terminal.

### Error: the prompt does not show `(.venv)`

**Likely cause:** Some terminals or prompts do not display the environment name.

**What to do:** Use `python -c "import sys; print(sys.executable)"` to check. A path inside `.venv` is more reliable than the visual prompt.

### Error: activation succeeded, but VS Code runs a different Python

**Likely cause:** VS Code may have selected a different Python interpreter for its Run button or debugging tools.

**What to do:** In VS Code, use **Python: Select Interpreter** from the Command Palette and select the interpreter in your practice project's `.venv`. Then check the interpreter path again in the terminal. The terminal and editor may need separate selections.

## 11. Mini knowledge check

Try to answer before reading the explanations:

**Question 1:** If you deactivate `.venv`, will your Python files disappear?

**Answer:** No. Deactivation only changes the active terminal environment. It does not delete source code or the `.venv` directory.

**Question 2:** A teammate creates `.venv` on a Mac. Should they send that folder to a teammate using Windows?

**Answer:** No. Each teammate should create an environment on their own computer and later install the dependencies listed by the project. Environment folder contents can differ by operating system.

**Question 3:** Why do we check `sys.executable` after activation?

**Answer:** To verify that `python` is actually using the project's environment, rather than assuming activation succeeded because the prompt looks different.

## 12. Lesson recap

You can now create, activate, verify, and deactivate a Python virtual environment. The `.venv` folder remains in your project even after deactivation. Activating it prepares your terminal to use that project's Python and installed packages.

**Next:** `03_Installing_Dependencies_with_pip.md` — you will use the activated environment to install a third-party package, check where it was installed, and understand how projects record dependencies for other developers.

**Week 6 reminder:** The required work stays local and does not require a Claude account, a real API key, or any paid API call.
