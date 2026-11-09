# Guided Practice — Virtual Environments and Dependencies

## Practice purpose

You have watched the instructor set up a separate eComMART low-stock notifier. Now you will repeat the most important setup steps yourself in a **small, disposable practice folder**. You will create a virtual environment, install dependencies, document versions, and verify that Python uses the correct environment.

This is guided practice: each task has a **reason**, a **command**, and an **expected check**. Try each step before reading the hints. It is OK to return to Lessons `03_Virtual_Environments/` and `04_Dependency_and_Configuration_Management/` when needed.

**Core:** creating a virtual environment and using `requirements.txt` is required Week 6 knowledge. **Optional/stretch:** reinstalling into a second environment, extra package inspection, or any Anthropic SDK work. There are **no live LLM calls, real API keys, account signups, or paid services** in this practice.

## Learning objectives

By the end, you should be able to:

- Create and activate `.venv` in the correct folder.
- Use `python -m pip` to install dependencies into **that** environment.
- Read and write `requirements.txt` with package versions.
- Verify installed packages and locate the Python executable.
- Explain why `.venv/` should stay local while `requirements.txt` is shared.
- Identify and fix common virtual environment setup problems.

## 1. The eComMART scenario

A second eComMART developer wants to try your low-stock alert work on their own computer. Sending your entire `.venv` folder would be slow and unreliable because virtual environments contain machine-specific paths and files. Instead, you give the developer your Python source and `requirements.txt`, and they create a fresh environment themselves.

In this activity you act as that **second developer**, preparing a clean workspace for a future EcomMART utility. This folder is **not** the Week 5 catalog and **not** the Instructor Demo folder, so you can experiment safely.

### What you will create

```text
ecommart_setup_practice/
├── .venv/                # created locally
└── requirements.txt      # saved text file
```

The folder name is only for this guided activity. The **required takeaway later** will apply the same setup skills to **your own Week 5 catalog**.

## 2. Before you start

Make sure:

- Python **3.10 or newer** is installed (the pinned practice dependencies require a compatible Python version).
- You can open a project folder and integrated terminal in VS Code or another editor.
- You have internet access **only to download Python packages from PyPI** on first install, unless the packages are already cached. This is **not** an AI/API connection and does not require an account.
- Your Week 5 catalog files are backed up or stored elsewhere; do not move or overwrite them.

Check Python:

| Operating system | Command |
|---|---|
| Windows | `py --version` |
| macOS/Linux | `python3 --version` |

Expected: `Python 3.x.x` where the version is at least 3.10. If you use more than one installed Python version, ask the instructor for help selecting a compatible one.

## 3. Task 1 — Make a clean practice folder

Create a new folder named `ecommart_setup_practice` somewhere in your personal workspace. In VS Code, choose **File → Open Folder** and open **that folder**. Then open **Terminal → New Terminal**.

Check your location:

| Terminal | Command |
|---|---|
| Windows PowerShell | `Get-Location` |
| Windows Command Prompt | `cd` |
| macOS/Linux | `pwd` |

**Expected:** the displayed path ends in `ecommart_setup_practice`.

**Why this matters:** Running setup commands in the wrong folder can put `.venv` and `requirements.txt` into an unrelated project. Always locate your terminal first.

**Your check:** Can you point to the empty practice folder in your editor's file explorer?

## 4. Task 2 — Create and activate a virtual environment

Run the appropriate command from your **practice folder**:

| Operating system | Create `.venv` |
|---|---|
| Windows | `py -m venv .venv` |
| macOS/Linux | `python3 -m venv .venv` |

What does that command mean? `-m venv` starts Python's built-in virtual-environment creator; `.venv` is the name of the folder it creates.

Next, activate the environment in your current terminal:

| Terminal | Activate |
|---|---|
| Windows PowerShell | `.\.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `.venv\Scripts\activate.bat` |
| macOS/Linux bash/zsh | `source .venv/bin/activate` |

Many terminals show `(.venv)` at the beginning of the prompt. If yours does not, **verify instead of guessing**:

```bash
python -c "import sys; print(sys.executable); print(sys.prefix)"
```

**Expected:** both printed paths refer to the Python setup inside `ecommart_setup_practice/.venv` (exact paths vary). Your global Python folder should not be the active interpreter.

**If activation is blocked:** you can use the virtual environment directly without modifying system security settings:

| Terminal | Environment-specific Python |
|---|---|
| Windows PowerShell / Command Prompt | `.venv\Scripts\python.exe` |
| macOS/Linux | `.venv/bin/python` |

For example, on Windows run `.venv\Scripts\python.exe -m pip --version`; on macOS/Linux run `.venv/bin/python -m pip --version`. If you use this method, replace `python` with your environment-specific Python path in the remaining commands.

**Checkpoint 1:** Write down which terminal you use and which command successfully activated or accessed your `.venv`.

## 5. Task 3 — Create requirements.txt

Create a plain-text file named **exactly** `requirements.txt` in `ecommart_setup_practice/` with these two lines:

```text
python-dotenv==1.2.4
pytest==9.2.0
```

- `python-dotenv` will later help read settings from a local `.env` file.
- `pytest` will later run automated Python tests.
- `==` means **install this exact version** rather than any available version.
- These are **core Python learning dependencies**, not an LLM service. You do not need an Anthropic package here.

These versions match the earlier Week 6 setup lesson. The important practice is knowing how to **record and reproduce** the package versions selected for a project, not memorizing version numbers forever.

**Checkpoint 2:** Verify the file is named `requirements.txt`, not `requirements.txt.txt`, and sits beside `.venv/`.

## 6. Task 4 — Install into your own environment

With the environment active (or using its interpreter directly), run:

```bash
python -m pip install -r requirements.txt
```

Read the command:

- `python -m pip` uses pip through **this Python interpreter**.
- `install` downloads/installs the packages if necessary.
- `-r requirements.txt` tells pip to read package names and versions from the file.

Installation may produce many lines because the named packages can depend on other packages. These extra packages are called **transitive dependencies**. Do not copy every line of installation output into `requirements.txt` for this exercise.

Verify:

```bash
python -m pip show pytest
python -m pip show python-dotenv
python -m pytest --version
```

**Expected checks:** `pip show` includes the package names and versions; the final command reports `pytest 9.2.0` if installation succeeded. Exact installation paths and output formatting depend on the operating system.

**Important:** If you installed packages while the wrong environment was selected, create/activate the correct `.venv` and run the install command again. Avoid using `sudo pip install` or installing globally as a shortcut.

## 7. Task 5 — Prove isolation and understand what to share

First, check where pytest is installed:

```bash
python -m pip show pytest
```

Look for the `Location:` field. It should point to the environment's `site-packages` directory, which belongs to `.venv`.

Now imagine a teammate copies your project. Which items should they receive?

| Item | Share it? | Reason |
|---|---|---|
| `requirements.txt` | **Yes** | Lets teammates reinstall named dependencies |
| Your Python source files | **Yes**, when the project is ready | Contains the app behavior |
| `.venv/` | **No** | Local, machine-specific environment |
| `.env` with real secrets | **No** | Local/private configuration |
| `.env.example` with safe placeholder values | **Yes**, when used | Explains settings without exposing credentials |

You have **not** created `.env` in this practice: configuration is covered in the **next guided practice**. There is no key to set in today's task.

### Optional: see the packages pip installed

```bash
python -m pip list
```

This shows all installed packages, not just the two top-level entries in `requirements.txt`. You may also run `python -m pip freeze` to see a version-pinned inventory. For a beginner's small application, keep `requirements.txt` focused on the dependencies your project needs, according to the course instructions; do not blindly replace it with unrelated packages from a global environment.

## 8. Mini challenge — solve before opening the hint

A teammate runs:

```bash
python -m pytest --version
```

They get:

```text
No module named pytest
```

But the teammate says, “I already installed pytest yesterday!”

**Think:** Give two possible reasons and one verification command.

<details>
<summary>Hint and suggested answer (open after trying)</summary>

Possible reasons: pytest was installed in a different Python environment, or the new `.venv` has not had `requirements.txt` installed. Run `python -c "import sys; print(sys.executable)"` to see the interpreter, activate the intended `.venv`, then run `python -m pip install -r requirements.txt`.

</details>

## 9. Troubleshooting

| What you see | What it usually means | What to do |
|---|---|---|
| `py` or `python3` is not found | Python is not installed or not on the command path | Install Python 3.10+ and reopen the terminal; use the system-appropriate launcher |
| `No module named venv` | Python installation is missing venv support | Install the OS's Python venv component, then recreate the environment |
| PowerShell refuses `Activate.ps1` | A local script execution policy blocks activation | Use `.venv\Scripts\python.exe` directly, or follow your organization's approved PowerShell guidance |
| `No module named pip` | pip is missing from this interpreter | Verify the `.venv` interpreter and consult the instructor's Python installation guidance |
| `No module named pytest` | Wrong Python selected or requirements not installed | Verify `sys.executable`, activate `.venv`, reinstall with `python -m pip` |
| Package version cannot be installed | Incompatible Python version, restricted network, or unavailable package source | Confirm Python 3.10+, connectivity to your approved package index, and the pinned package versions |
| `.venv` appears in the wrong project | Terminal opened in the wrong folder | Return to the practice folder; create the environment there |
| A command works in one terminal but not another | Activation is terminal-session specific | Activate `.venv` separately in each terminal |

## 10. Knowledge check

Try answering without rereading the instructions:

1. Why do two Python projects benefit from **separate** virtual environments?
2. What does `-r requirements.txt` tell pip to do?
3. Which command shows the exact interpreter used by the current `python` command?
4. Why do we share `requirements.txt` but not `.venv/`?
5. If the terminal shows `(.venv)`, is that alone a complete verification? Why or why not?

**Expected understanding:** A virtual environment isolates installed packages, and a dependency file tells another developer how to recreate that setup. Verification is based on the interpreter and installed packages, not only on the prompt's appearance.

## 11. Completion checklist

- [ ] I created a separate `ecommart_setup_practice/` folder.
- [ ] I created `.venv` inside that folder.
- [ ] I activated the environment or used its interpreter directly.
- [ ] `sys.executable` points to my practice `.venv`.
- [ ] I created `requirements.txt` with the two pinned packages.
- [ ] I installed dependencies using `python -m pip install -r requirements.txt`.
- [ ] `python -m pytest --version` succeeds in this environment.
- [ ] I know why `.venv/` is local and `requirements.txt` is shareable.
- [ ] I did not use a real API key, Anthropic signup, paid API, or live LLM call.

**Next:** `02_Guided_Practice_Config_and_Project_Structure.md` will add environment-based configuration and practice separating responsibilities. After guided practice, the **required Independent Challenge** will apply Week 6 improvements to **your own Week 5 eComMART catalog**, with 2–3 simple pytest tests.
