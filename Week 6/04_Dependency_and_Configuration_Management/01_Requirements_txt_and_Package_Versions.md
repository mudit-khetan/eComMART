# requirements.txt and Package Versions

## Lesson purpose

Your `ecommart_venv_practice` environment can now run `pytest`. But imagine a second eComMART developer downloads your Python files onto another laptop. They will not automatically receive the extra packages you installed locally.

In this lesson, you will write a **`requirements.txt`** file: a simple, shareable list of the Python packages a project needs. Then you will create a clean environment and use the list to install the same package versions. This is the first step toward making your application easier for another person to run.

## Learning objectives

By the end of this lesson, you will be able to:

- Explain why virtual environments and `requirements.txt` solve different problems.
- Read the basic `package==version` format.
- Write and install from a short `requirements.txt` file.
- Explain the difference between exact pins and version ranges.
- Use `pip freeze` carefully without accidentally listing unrelated packages.
- Recognize why Python standard-library modules do not go in `requirements.txt`.
- Prepare a dependency file for the Week 6 low-stock demo and later Week 5 catalog challenge.

## 1. The eComMART problem: 'It works on my computer'

An eComMART developer has successfully installed `pytest` in the local `.venv`, but another developer receives only the `.py` files. They try to run the tests and get:

```text
No module named pytest
```

Nothing is wrong with the application logic. The second developer is missing a **dependency**.

The two pieces of setup information are different:

| Item | What it does | Do you share it with teammates? |
|---|---|---|
| `.venv/` | Stores installed packages and Python environment files on **your** machine | **No** — teammates create their own |
| `requirements.txt` | Lists packages and versions to install | **Yes** — it belongs with the project code |

A virtual environment gives packages an isolated home. A requirements file describes what needs to go into that home.

**Core for Week 6:** create and use `requirements.txt`. **Optional/stretch:** Anthropic SDK is not required for this lesson, the demo's core tests, or the graded work. No AI account or live API call is needed.

## 2. How to read requirements.txt

A requirements file is a **plain text file**, not a Python program. Each nonblank line normally names a package to install. For example:

```text
pytest==9.2.0
```

Read this as: 'Install `pytest`, specifically version `9.2.0`.'

- `pytest` is the package name.
- `==` means **exactly this version**.
- `9.2.0` is the requested version number.

Version numbers help distinguish releases. A new version might add functionality, change behavior, fix a bug, or drop support for an older Python version.

As verified from PyPI on **4 November 2026**, these example versions are real:

| Package | Verified version | Use in this course |
|---|---|---|
| `pytest` | `9.2.0` | **Core:** run automated tests |
| `python-dotenv` | `1.2.4` | **Core later:** load local `.env` settings in the demo |

Both releases require **Python 3.10 or later**. We will introduce `python-dotenv` in the configuration lesson; you do **not** need to use it yet to understand requirements files.

Official package pages: <https://pypi.org/project/pytest/> and <https://pypi.org/project/python-dotenv/>.

## 3. Step 1 — Create requirements.txt

Return to the **first** `ecommart_venv_practice` folder from the previous section. Open the folder in VS Code and activate its `.venv`.

Create a new text file named exactly:

```text
requirements.txt
```

Type this line and save:

```text
pytest==9.2.0
```

Your practice folder should resemble:

```text
ecommart_venv_practice/
├── .venv/                 # local; do not share
└── requirements.txt       # share with project code
```

**Common beginner mistake:** the name is `requirements.txt`, not `requirement.txt` or `requirements.txt.py`.

### Why only one line right now?

We are practicing how the file works. Do not add packages that this simple practice project does not need. The instructor's eComMART low-stock notifier will eventually use both `pytest` and `python-dotenv`, but that is a separate project with its own dependency file.

## 4. Step 2 — Install dependencies from the file

With `.venv` active and the terminal in the folder containing `requirements.txt`, run:

```bash
python -m pip install -r requirements.txt
```

The `-r` option means: **read package requirements from the named file**.

If you already installed `pytest 9.2.0` in the previous lesson, `pip` may display a message similar to:

```text
Requirement already satisfied: pytest==9.2.0 ...
```

That is fine: it confirms the requested package is already present. If the environment does not have the package, `pip` will install it.

Now verify:

```bash
python -m pytest --version
```

Expected:

```text
pytest 9.2.0
```

### What if the file cannot be found?

A message mentioning `No such file or directory: 'requirements.txt'` often means your terminal is in the wrong folder. Open the folder containing the file and rerun the command; do not create duplicate files in unrelated locations to silence the error.

## 5. Step 3 — Understand exact pins and version ranges

Two common ways to specify versions are:

| Entry | Meaning | Example situation |
|---|---|---|
| `pytest==9.2.0` | Install exactly version `9.2.0` | Repeating this week's training environment |
| `pytest>=9.2.0,<10` | Allow versions at least `9.2.0` but below `10` | A project that deliberately allows compatible upgrades |
| `pytest` | Let `pip` choose a suitable available version | Quick experimentation; less predictable over time |

For this beginner course, we will **pin versions** in the examples to make setup and troubleshooting more consistent. Pinning does not guarantee a package is secure forever or that a project works identically on every operating system; teams still check compatibility and update dependencies thoughtfully.

**Do not mix all three examples into the same file.** They are alternative ways to specify one package, not three lines students should copy together.

## 6. Step 4 — See what pip freeze does

Run this while your **practice `.venv` is active**:

```bash
python -m pip freeze
```

You will see lines of installed packages with versions. The list may contain `pytest` **and packages it uses internally**. The exact set can vary.

You can save that output to a file using:

```bash
python -m pip freeze > installed_packages.txt
```

Here `>` sends the terminal output into a text file rather than displaying it on screen. Open `installed_packages.txt` and compare it with the short `requirements.txt` you wrote.

### Why not always use `pip freeze > requirements.txt`?

You **can** generate a requirements file that way, and you will encounter this command in real projects:

```bash
python -m pip freeze > requirements.txt
```

But it records **everything currently installed in that environment**, including supporting dependencies and anything you installed for unrelated experiments. That can make a beginner project harder to understand and maintain.

**Course guidance:** For this small practice project, keep the hand-written `requirements.txt` containing `pytest==9.2.0`. For your Week 5 takeaway, creating the list manually or generating it with `pip freeze` is acceptable **if you review it, confirm it comes from your project's `.venv`, and remove unrelated packages**.

You should not include built-in `sqlite3`, `os`, or `pathlib` in requirements files.

## 7. Step 5 — Try a clean install as a teammate would

To prove the file is useful, do not rely only on your already-configured environment.

1. Make a new empty folder: `ecommart_requirements_check`.
2. Copy **only** `requirements.txt` from `ecommart_venv_practice` into it. Do **not** copy `.venv`.
3. Open the new folder in VS Code and open a terminal there.
4. Create its own `.venv` using the OS-specific command from Lesson 02.
5. Activate the new `.venv` and verify its interpreter path.
6. Run:

```bash
python -m pip install -r requirements.txt
```

7. Check:

```bash
python -m pytest --version
```

**Expected result:** the new environment reports `pytest 9.2.0`. You have reconstructed the required test dependency from the shareable text file.

This is a simplified version of how another developer can set up the same eComMART project on their own machine.

## 8. How this applies to the Week 6 low-stock demo

Later, the instructor's **fresh, separate** low-stock notifier will use this core dependency file:

```text
pytest==9.2.0
python-dotenv==1.2.4
```

- `pytest` runs local automated tests.
- `python-dotenv` loads settings from a local `.env` file when the app starts.

**Important:** Neither package needs a paid API or real key. The low-stock check itself is ordinary Python. The Anthropic SDK wrapper is **optional/stretch** and is not included in the core requirements above.

When you complete the independent challenge, you will instead create a `requirements.txt` for **your own Week 5 catalog**. It may have fewer or different dependencies depending on what your app uses. For example, SQLite itself uses Python's `sqlite3` standard-library module, so it does not require an extra `sqlite3` line.

## 9. Guided practice and verification

Without looking at the steps above, complete the following:

1. Open `ecommart_venv_practice` and activate its `.venv`.
2. Explain out loud what `pytest==9.2.0` means.
3. Confirm that the project's `requirements.txt` contains exactly that line.
4. Run `python -m pip install -r requirements.txt`.
5. Run `python -m pytest --version` and record the version reported.
6. Explain why your teammate needs the file but should **not** copy your `.venv` folder.

**Evidence of success:** you can show a saved `requirements.txt`, the successful install or already-satisfied message, and `pytest 9.2.0` reported in the active environment.

### Mini challenge

A learner writes this:

```text
sqlite3
pytest==9.2.0
```

What would you change?

**Suggested answer:** remove `sqlite3`, because it belongs to standard Python installations; keep the pinned third-party `pytest` requirement.

## 10. Troubleshooting

| Problem | Possible cause | Next step |
|---|---|---|
| `requirements.txt` not found | Terminal is in another directory | Open the folder containing the file |
| `Invalid requirement` | Typo, wrong punctuation, or extra text in a line | Compare against `pytest==9.2.0` exactly |
| Version cannot be installed | Incompatible Python or blocked package source | Check `python --version`; these examples require Python 3.10+ |
| `pytest` works in one terminal but not another | Different active environments | Verify `sys.executable` in both terminals |
| `pip freeze` lists unexpected packages | Environment contains previous experiments | Review the list rather than sharing it blindly |
| File is named `requirements.txt.txt` | Hidden file extensions on Windows | Enable extensions in the file manager and correct the name |

Do not use system-wide package installation or disable security settings to make the lesson work. Ask your instructor or IT team for help when network policies block approved package downloads.

## 11. Knowledge check

**Question 1:** Is `requirements.txt` a Python script that you run with `python requirements.txt`?

**Answer:** No. It is a text file read by `pip` using `python -m pip install -r requirements.txt`.

**Question 2:** Should two teammates copy the same `.venv` directory between Windows and macOS?

**Answer:** No. Each teammate creates a local environment and installs packages from the requirements file.

**Question 3:** Why might `pip freeze` list more packages than your one-line requirements file?

**Answer:** It lists all installed packages in the environment, including indirect dependencies installed to support `pytest`.

**Question 4:** Does putting `pytest` in a requirements file automatically test the catalog?

**Answer:** No. The file only describes the dependency; you still need to install it and write and run tests.

## 12. Lesson recap

A local `.venv` isolates installed packages, and `requirements.txt` records what another environment should install. You created a small pinned dependency list, installed from it, inspected installed packages, and repeated the process in a fresh environment.

Next, we will make the eComMART program more configurable by using **environment variables** and a local **`.env`** file rather than hardcoding settings inside Python code.

**Next:** `02_Environment_Variables_and_the_env_File.md`
