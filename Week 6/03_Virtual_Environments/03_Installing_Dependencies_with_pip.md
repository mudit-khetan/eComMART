# Installing Dependencies with pip

## Lesson purpose

You created and activated a private Python environment in the previous lesson. It is ready to use, but it does not yet contain the extra tools we will need for Week 6. In this lesson, you will install a real package, check that it reached the **right environment**, and learn how to remove it when necessary.

The goal is not to memorize terminal commands. It is to understand what each command changes and how to confirm that it worked.

## Learning objectives

By the end of this lesson, you will be able to:

- Explain the difference between a Python module, a third-party package, and a dependency.
- Describe what `pip` does and why the active virtual environment matters.
- Install, inspect, and uninstall a package using `python -m pip`.
- Distinguish packages built into Python from packages that must be installed.
- Check package installation without changing your Week 5 catalog.
- Troubleshoot common installation mistakes.

## 1. The eComMART story: adding a tool without breaking another project

The Week 5 eComMART product catalog uses **`sqlite3`**, which is included with standard Python installations. That is why you did not need to download a separate Python package to connect to SQLite.

In Week 6, the eComMART team wants to add **automated tests** to its small low-stock alert program. For that, we will use **`pytest`**. Unlike `sqlite3`, `pytest` is a **third-party package**: a tool maintained outside the Python standard library that we install separately.

We will install it in the practice folder's `.venv`. We will **not** change your existing Week 5 database or catalog application in this lesson.

**Core work:** learn `pip` and install `pytest`. **Optional/stretch:** installing an AI SDK comes later; no AI account, API key, or live AI request is needed here.

## 2. What are packages and dependencies?

A **module** is a Python file containing useful code that other files can import. A **package** groups related Python code for reuse. You studied modules and packages in Section 01; here we focus on installing third-party packages with pip.

A **dependency** is something your project needs in order to work. When your tests use `pytest`, then `pytest` is a development dependency of the project.

| Name | Meaning | eComMART example |
|---|---|---|
| Python standard library | Modules provided with standard Python | `sqlite3`, `os`, `pathlib` |
| Third-party package | Reusable code installed separately | `pytest` |
| `pip` | The program that installs Python packages | Installs `pytest` into `.venv` |
| Dependency | A package the project relies on | `pytest` to run tests |

A package may need **other packages** to run. `pip` normally installs those supporting dependencies as well. That is why installing one named package can produce several lines of installation output.

**Important:** An `import` statement does not automatically install a package. You install a missing third-party package with `pip` first; later you import or run it from Python.

## 3. Before you start: activate the practice environment

Use the same `ecommart_venv_practice/` folder created in `02_Creating_and_Activating_venv.md`. In your terminal, first open that folder. Activate its environment:

| Operating system / terminal | Command |
|---|---|
| Windows PowerShell | `.\.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `.venv\Scripts\activate.bat` |
| macOS / Linux | `source .venv/bin/activate` |

Now verify that the Python interpreter belongs to the practice project:

```bash
python -c "import sys; print(sys.executable)"
```

**Expected:** the printed path contains `ecommart_venv_practice` and `.venv`.

If it does not, do not proceed with installation yet. Return to Lesson 02 and correct the environment selection.

### Why we will use `python -m pip`

You may see tutorials using only `pip install ...`. In this course, use:

```bash
python -m pip ...
```

This tells the **currently selected Python interpreter** to run its own `pip` module. It reduces the chance that an unrelated Python installation receives the package.

## 4. Step 1 — Check pip before installing anything

Run:

```bash
python -m pip --version
```

Expected output will resemble this (your version and file path will vary):

```text
pip X.Y from .../ecommart_venv_practice/.venv/.../site-packages/pip (python 3.x)
```

The important part is that the path points into **this project's `.venv`**. The numbers in this example are placeholders, not a required `pip` version.

If you see `No module named pip`, see the troubleshooting section rather than running random global installation commands.

## 5. Step 2 — Install pytest

Run the following command while `.venv` is active:

```bash
python -m pip install pytest==9.2.0
```

Read it piece by piece:

- `python -m pip`: use `pip` belonging to this environment's Python.
- `install`: download and install a package.
- `pytest`: the package name.
- `==9.2.0`: request this **exact version** so this lesson is repeatable.

As checked on **4 November 2026**, PyPI lists `pytest 9.2.0` (released 27 October 2026). This release requires **Python 3.10 or later**. If your Python is older, ask the instructor to help you use an appropriate supported Python installation; do not force an incompatible install.

Official source: <https://pypi.org/project/pytest/>

Your terminal may show download progress and several supporting packages. The exact output can differ. A successful installation finishes without an error and will typically include a success message naming `pytest`.

**Why pin a version now?** Repeating the same installation later is more predictable than silently accepting a future release. The next lesson will explain how to record package versions in `requirements.txt`.

## 6. Step 3 — Check that pytest is installed

Run:

```bash
python -m pip show pytest
```

Look for fields similar to:

```text
Name: pytest
Version: 9.2.0
Location: .../.venv/.../site-packages
```

The exact `Location` varies by operating system. Confirm it points to your practice environment.

Then run:

```bash
python -m pytest --version
```

Expected output:

```text
pytest 9.2.0
```

You wrote tests in Section 02. This command only verifies that pytest is installed in this particular virtual environment; it does not run those tests.

### Optional inspection: list installed packages

```bash
python -m pip list
```

You may see `pytest` and other packages installed to support it. Do not assume every listed package is something you need to import directly in application code.

## 7. Step 4 — See how an installed package differs from a standard-library module

Try these two short checks in the same activated terminal:

```bash
python -c "import sqlite3; print('sqlite3 is available')"
```

```bash
python -c "import pytest; print('pytest is available')"
```

Expected results:

```text
sqlite3 is available
pytest is available
```

Although both can be imported, they arrived differently: `sqlite3` came with standard Python, while `pytest` was installed with `pip`.

## 8. Guided practice — install into a second environment

This activity helps demonstrate isolation. Keep the first `.venv` intact.

1. Deactivate the current environment with `deactivate`.
2. Create a **second, empty** folder named `ecommart_second_practice` and open it in a new terminal.
3. Create another `.venv` using your operating system's command from Lesson 02.
4. Activate the second `.venv` and verify its interpreter path.
5. Run `python -m pip show pytest` **before** installing `pytest` here.
6. If it reports that the package was not found, that is the expected result for a fresh environment.
7. Install the same version with `python -m pip install pytest==9.2.0`.
8. Check `python -m pytest --version` again.

**Expected observation:** the second environment starts without `pytest`, even though it was installed in the first one. After you install it, each project has its own copy. This is the reason virtual environments help prevent project conflicts.

If the second environment already contains `pytest`, stop and verify you created and activated a genuinely new `.venv`; do not guess from the prompt alone.

## 9. Optional experiment — uninstall and reinstall (safe practice only)

Perform this **only** in `ecommart_second_practice`, not in a shared or production environment.

```bash
python -m pip uninstall pytest
```

When prompted, confirm the uninstall. Check:

```bash
python -m pip show pytest
```

Expected: `pytest` is not found. Now reinstall:

```bash
python -m pip install pytest==9.2.0
```

Installing or removing a test package does **not** delete the SQLite product data saved by the Week 5 application. Dependencies and persistent business data are different things.

## 10. Common errors and fixes

| Problem | Likely reason | What to do |
|---|---|---|
| `No module named pip` | `pip` is missing from this environment | Verify the active interpreter; ask for help restoring `pip` in this environment, for example using Python's supported `ensurepip` where available |
| `No matching distribution found` | Python version is incompatible, version is mistyped, or package index is inaccessible | Confirm `python --version`, spelling, and the version's PyPI requirements |
| `No module named pytest` after install | Package was installed into a different interpreter | Check `python -m pip show pytest` and `sys.executable` in the same terminal |
| Network, certificate, or proxy error | Package download is blocked | Check connectivity or ask the instructor/IT for an approved package source; do not disable certificate checks |
| Permission error | Attempting a global install or restricted folder | Activate the local `.venv` and retry without `sudo` or `--user` |
| VS Code still cannot find `pytest` | Editor uses a different interpreter | Use **Python: Select Interpreter** and choose the project's `.venv` |

**Security note:** Install packages from trusted sources and never paste an API key or password into a package-install command. Do not use `sudo pip install` for this exercise.

## 11. Quick knowledge check

**Question 1:** Why is `python -m pip install pytest==9.2.0` safer for this lesson than a bare `pip install pytest`?

**Answer:** It selects `pip` belonging to the active interpreter and requests a known version rather than whichever version happens to be newest.

**Question 2:** Do you need to put `sqlite3` into the project's `requirements.txt` later?

**Answer:** No. It is part of Python's standard library on standard installations. We record separately installed dependencies such as `pytest`.

**Question 3:** You installed `pytest` in Project A. Project B says `pytest` is missing. Is virtual environment isolation broken?

**Answer:** No. That is expected. Each project gets the packages installed into its own environment.

## 12. Lesson recap

You used `python -m pip` to install a third-party package, confirmed its version and installation path, and saw how a second environment starts independently. You are now ready to record dependencies in a file so another developer can set up the same project.

**Next:** `../04_Dependency_and_Configuration_Management/01_Requirements_txt_and_Package_Versions.md`
