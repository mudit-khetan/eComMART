# Why Isolated Python Environments Matter

## Learning objectives

By the end of this lesson, you will be able to:

- Explain what a Python **package**, **dependency**, and **virtual environment** mean in everyday language.
- Describe why installing every package into one shared Python setup can cause problems.
- Explain how two eComMART projects can use different package versions without interfering with each other.
- Distinguish a virtual environment from a folder containing application code and from a SQLite database.
- Identify which tasks belong to this week's **core learning** and which are optional AI-related extensions.

## 1. Start with a familiar eComMART problem

Last week, you built an eComMART product catalog using Python functions and SQLite. You can add products, look up their details, and update stock in a database. Your program currently lives in one Python file, `05_Product_Catalog_App.py`.

Now imagine another developer joins the eComMART team. You send that person your Python file. They can open it, but a working application needs more than source code: it also needs a suitable Python installation and, when we start using external libraries, the right supporting packages.

At the same time, the eComMART inventory team asks for a separate **low-stock alert** tool. It will look at a quantity such as `4`, compare it with a minimum such as `10`, and prepare a message for staff. This small tool is the **new Instructor Demo** for Week 6. It does not replace your Week 5 catalog.

Both programs can run on the same computer. But what happens if, in the future, one project requires a newer version of a library and another project still needs an older version?

That is the problem virtual environments help solve.

## 2. First, understand three useful terms

### Python package

A **package** is Python code that someone has organized for reuse. Think of it as a toolbox: rather than writing everything yourself, you can install a toolbox that provides useful functions and classes.

Python already includes many useful tools in its **standard library**. For example, `sqlite3` lets your Week 5 program use a SQLite database. You do not need to install `sqlite3` with `pip` for a standard Python installation.

Other packages come from outside Python's standard library. For example, **pytest** is a third-party package that helps you check your program automatically. You already encountered it in Section 02 and will now learn how to install packages inside an isolated project environment correctly.

### Dependency

A **dependency** is something your program needs in order to run or perform a particular task. If you write tests using pytest, you need the pytest package installed to run those tests. That makes pytest a **testing dependency**.

Not every imported module requires a separate installation:

| Example | Where it comes from | Install with `pip`? |
|---|---|---|
| `sqlite3` | Python standard library | No |
| `os` | Python standard library | No |
| `venv` | Python standard library (included in typical Python 3 installations) | No separate pip install |
| `pytest` | Third-party package | Yes, for running pytest tests |

If Python cannot find a third-party package that code imports, you may see a `ModuleNotFoundError`. We will learn how to install packages in the third lesson of this folder.

### Version

A **version** is a label identifying a particular release of software. Packages change over time as developers fix bugs, improve features, or change behavior.

For example, imagine a *hypothetical* package called `shop-helper`:

- Project A was written for `shop-helper` version `1.0`.
- Project B was written for `shop-helper` version `2.0`.

These version numbers are for illustration, **not packages you need to install**. A change between releases might mean that the same code behaves differently. If every project shares the same package installation, upgrading for Project B could unexpectedly affect Project A.

## 3. The problem with one shared installation

Without a project-specific environment, a developer might install third-party packages into a shared Python installation. This can create several difficulties:

1. **Version conflicts.** Two projects may expect incompatible releases of a package.
2. **Unclear setup.** A project works on your machine because you installed something months ago, but the next developer does not know it is required.
3. **Accidental changes.** Installing or upgrading a package for one project can affect another project using that same installation.
4. **Harder troubleshooting.** When many unrelated packages share one environment, it is less obvious which packages belong to the application you are studying.

A virtual environment does not make software bug-free. It simply gives each project a more predictable place to manage its packages.

### Think about two eComMART projects

| Project | Purpose | Packages it might need |
|---|---|---|
| Week 5 product catalog | Save and retrieve products in SQLite | Python's built-in `sqlite3`; later, `pytest` for testing |
| Week 6 low-stock notifier | Check quantities and format alerts | Built-in Python features; `pytest` for testing; optional AI SDK later |

We want the ability to work on either project independently. A package used for an optional AI experiment should not become a requirement for simply opening the product catalog.

## 4. What is a virtual environment?

A **virtual environment**, often shortened to **venv**, is a project-specific Python environment. It provides its own Python command and a place to install packages used by that project, separate from packages installed in other environments.

You still use Python. You still write ordinary `.py` files. The difference is **which Python environment runs the code and where additional packages are installed**.

A helpful mental model is to imagine separate labeled toolboxes:

```text
Your computer
|
+-- Python 3 installation
|
+-- eComMART Week 5 catalog project
|   +-- 05_Product_Catalog_App.py
|   +-- .venv/   <- packages installed for THIS project
|
+-- eComMART Week 6 low-stock demo project
    +-- main.py
    +-- stock_alert.py
    +-- .venv/   <- packages installed for THIS project
```

The `.venv` folders are separate. Installing a package in the low-stock demo's environment does not install it into the catalog's environment.

**Important:** A virtual environment is not a complete copy of your computer or a separate operating system. It uses your existing Python installation and helps isolate project-level Python packages. It is also **not** a database: the SQLite file stores product data, while the virtual environment holds the Python setup used to run the program.

### Why is the folder called `.venv`?

The name `.venv` is a common convention, not a special Python keyword. We use it because another developer can quickly recognize it as a virtual-environment folder. The leading dot is simply part of the folder name. On some systems, dot-prefixed folders are hidden by default.

## 5. What an isolated setup looks like in practice

You will learn the exact commands in the next lesson. For now, understand the sequence:

```text
Open a project folder
        |
        v
Create a virtual environment (.venv)
        |
        v
Activate it in your terminal
        |
        v
Install project dependencies there
        |
        v
Run the project or its tests
```

**Create** means telling Python to set up the environment folder. **Activate** means adjusting the current terminal session so a command like `python` uses that environment's Python first. **Install** means adding a package to that environment, usually with a tool called `pip`.

You will eventually record the project's third-party dependencies in `requirements.txt` so someone else can install them, too. This is called **dependency management** and is covered in the next folder.

### A virtual environment is disposable; your source code is not

If `.venv` gets damaged, you can usually recreate it and reinstall the dependencies. You should **not** delete your Python source files or database while trying to fix an environment issue.

In a shared project, developers normally do not distribute their personal `.venv` folder. Instead, they share the source files and `requirements.txt`, and each developer creates a separate environment. Later we will also use `.gitignore` to explain why `.venv` and local secrets should not be committed to version control.

## 6. How this helps future agentic AI projects

In later weeks, eComMART may connect inventory functions to an **LLM** (a large language model, a system trained to work with language) or use an **agent** (a program that can decide when to call tools to complete a task). Libraries for AI services can introduce additional dependencies.

Those future experiments should have a predictable project setup. An isolated environment helps developers:

- Keep AI-related packages separate from unrelated Python applications.
- Recreate a known software setup when working with a teammate.
- Test ordinary business functions, like `stock < threshold`, before involving a language model.

**Core for Week 6:** creating and using a virtual environment and basic dependencies.

**Optional/stretch only:** installing or exploring an Anthropic SDK wrapper. **No Claude signup, real API key, paid usage, or live API call is required.** When later lessons demonstrate a key setting, use a placeholder value only.

## 7. Guided understanding check (no installation yet)

Consider these situations. Before looking at the answers, choose whether a separate virtual environment would help, and explain why.

**Situation A.** You install pytest for the low-stock demo, but do not want to change packages used by your Week 5 catalog.

**Situation B.** Two classmates have Python installed, but only one has the package needed to run the shared tests.

**Situation C.** The catalog's SQLite database needs to preserve product changes after the Python program closes.

### Check your reasoning

- **A:** Yes. Give each project its own `.venv` and install its test dependencies there.
- **B:** An isolated environment plus an accurate dependency list makes setup easier to reproduce. A virtual environment alone cannot tell another person which packages to install.
- **C:** A virtual environment is not the solution to data persistence. SQLite handles stored data; `.venv` handles the Python environment.

## 8. Try it yourself: classify the project files

Look at these example items and decide whether each belongs to **application code**, **project dependencies**, **project data**, or the **local environment**:

| Item | Your classification |
|---|---|
| `05_Product_Catalog_App.py` | ? |
| `.venv/` | ? |
| `ecommart.db` | ? |
| `requirements.txt` | ? |

<details>
<summary>Reveal the answer after you try</summary>

- `05_Product_Catalog_App.py`: application code.
- `.venv/`: local environment.
- `ecommart.db`: project data.
- `requirements.txt`: a dependency list (we will learn its format later).

</details>

## 9. Common misunderstandings

| Misunderstanding | What to remember |
|---|---|
| "A venv creates a whole new operating system." | No. It isolates Python's project environment, not the entire computer. |
| "Every imported Python module goes into `requirements.txt`." | No. Standard-library modules such as `sqlite3` are not pip dependencies. |
| "My `.venv` is the database." | No. The database stores product records; `.venv` holds Python environment files. |
| "A virtual environment automatically installs project dependencies." | No. You still install needed third-party packages. |
| "I need to configure a live AI service to learn venv." | No. All core Week 6 work can run locally without paid AI services. |

## 10. Lesson recap

A virtual environment gives a Python project its **own place to manage packages**. This reduces interference between projects and makes later troubleshooting easier. It does not replace source code, SQLite storage, or a dependency list.

You now know *why* we isolate Python environments. In the next lesson, you will **create, activate, verify, and deactivate** one on Windows, macOS, or Linux.

**Next:** `02_Creating_and_Activating_venv.md`
