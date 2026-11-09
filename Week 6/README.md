# Week 6: Python Virtual Environments & Packaging + Testing

**Course:** AI Engineering Academy — eComMART AI Squad
**Focus:** Isolated Python environments, dependencies, configuration, project structure, and automated testing

## 1. Welcome to Week 6

In Week 5, you built an **eComMART B2B product catalog** using Python functions and an SQLite database. Your program can store products, look them up, and update inventory records. That is a meaningful achievement: you have an application that works with data that remains available after the program closes.

There is still a practical problem. The Week 5 catalog is contained in one Python file, `05_Product_Catalog_App.py`. Its database location is written directly in the code, and there is no dedicated list of packages, separate configuration file, or automated test suite.

Imagine that another eComMART developer wants to run your application on their computer. How will they know which packages to install? How can they change a setting without editing source code? How can they check that a small change has not broken a feature that worked yesterday?

This week, you will learn the tools Python developers use to answer those questions. You will first organize functions into modules and learn to test them, then create a **virtual environment** (a private place for one project's Python packages), record dependencies, and move settings outside the main code. The instructor demo brings all of these skills together.

**No real API cost or account signup is required for Week 6.** We will introduce the Anthropic SDK as an **optional/stretch** example of a package used with an AI service. Students will only use a **placeholder** Claude API key in `.env` when practicing key configuration. **No real key, paid account, or live Anthropic API call is required for any graded or required activity.**

## 2. What you will learn

By the end of Week 6, you should be able to:

- Explain why two Python projects may need separate virtual environments.
- Create and activate a virtual environment using Python's built-in `venv` tool.
- Install a third-party Python package with `pip` and understand what a dependency is.
- Use `requirements.txt` to record the packages a project needs, including version information.
- Explain what an environment variable is and how a `.env` file can hold local settings outside application code.
- Avoid writing credentials or API keys directly in Python source files.
- Separate a small application into Python modules and import functions from another file.
- Recognize the responsibilities of application logic, configuration, database access, and tests.
- Write and run 2–3 simple automated tests with `pytest`.
- Use **Arrange → Act → Assert** to explain how a test prepares input, runs code, and checks the result.
- Test a normal result and an error or boundary case, rather than checking only the easiest input.
- Explain why predictable, testable functions make useful building blocks for future AI agent tools.

You do **not** need to understand AI models or make an AI API request to complete the week's required work.

## 3. The eComMART scenario

Imagine eComMART is a B2B store that sells supplies and equipment to other businesses. Its product catalog already keeps track of information such as product names, prices, and quantities in stock.

The inventory team now wants a simple **low-stock alert**: when the available quantity falls below a chosen threshold, the program should produce a clear message so staff know which product needs attention.

For example:

| Product | Units in stock | Alert threshold | Expected result |
|---|---:|---:|---|
| Wireless Barcode Scanner | 4 | 10 | Low-stock alert |
| Thermal Label Roll | 120 | 10 | No alert |
| USB-C Docking Station | 8 | 10 | Low-stock alert |

Here, a threshold of `10` means that an alert is needed when the stock value is **less than 10**. The program can decide that using an ordinary Python function. It does not need AI to count items or compare numbers.

We will use this small **eComMART low-stock notifier** for the **Instructor Demo**. It is a **fresh, separate learning example**, not a replacement for the Week 5 product catalog. Keeping the live demo small lets you concentrate on project setup, configuration, and testing.

The **Takeaway Hands-on Exercise** brings the story back to your own work: you will restructure **your existing Week 5 catalog** without removing its add, view, update, or delete features.

### Core work versus optional/stretch work

| Core — required this week | Optional/stretch — not required |
|---|---|
| Create and activate a virtual environment | Explore the Anthropic SDK package |
| Create and use `requirements.txt` | Add a thin Claude client wrapper |
| Configure and read at least one environment variable | Experiment with more advanced package layouts |
| Separate code into small, understandable modules in the demo and practice | Add more tests or test mocking |
| Write and run 2–3 simple `pytest` tests | Connect to an LLM in a later course activity |

**Important:** The required low-stock checks and tests run locally. They must not depend on an internet connection, API response, real API key, or paid AI service.

## 4. How the learning path works

Work through the sections in order. The concepts are introduced before you need to apply them in the demo or independent challenge.

| Stage | What you will do | Why it matters |
|---|---|---|
| 1. Application organization | Learn modules, imports, and a simple folder structure | Keep code easier to find, reuse, and test |
| 2. Testing fundamentals | Write `pytest` tests using Arrange → Act → Assert | Check expected behavior repeatedly without manual guessing |
| 3. Virtual environments | Create and activate a private environment; install packages | Keep one project's dependencies separate from another's |
| 4. Dependencies and configuration | Work with `requirements.txt`, package versions, and environment variables | Make the project easier to set up and configure safely |
| 5. Preparing for agentic AI | Understand LLMs and tools; discuss optional SDK setup | Connect today's Python practices to later AI applications |
| 6. Instructor Demo | Build a small eComMART low-stock notifier | See the week's core skills work together |
| 7. Practice and review | Follow guided tasks, then improve your own Week 5 catalog | Apply the same skills to the ongoing eComMART application |

The learning materials support **self-paced study during the week** and a **2-hour virtual instructor session** focused on explanation, demonstration, questions, and interaction. The training follows a learn-by-doing approach, with approximately **70% active practice and interaction** and **30% instructor-led explanation** across the learning experience. The required takeaway challenge is completed at your own pace.

### 2-hour instructor-led webinar — suggested run of show

Complete the lesson reading and beginner exercises **self-paced before the virtual session**. During the session, participants do short, guided activities alongside instructor demonstrations. Times below total **120 minutes**: approximately **36 minutes of instructor explanation** and **84 minutes of learner interaction or hands-on practice**. A live demonstration counts as an interactive block here only when learners predict, try, inspect, or discuss its results; passive watching alone is not hands-on learning.

| Time | Segment | Format | Learner action / checkpoint |
|---|---|---|---|
| 00–08 (8 min) | EcomMART recap and week's goal | Explanation (8 min) | Identify the Week 5 single-file limitations |
| 08–23 (15 min) | Module separation | Interactive (15 min) | Predict which file owns a function; move one simple function |
| 23–31 (8 min) | Testing concepts and test design | Explanation (8 min) | Describe a normal and boundary case aloud |
| 31–51 (20 min) | pytest walkthrough | Interactive (20 min) | Write or repair a test; observe a deliberate failure then a pass |
| 51–59 (8 min) | Why isolation and configuration matter | Explanation (8 min) | Explain a version conflict and a hardcoded path |
| 59–79 (20 min) | `venv`, dependencies, and `.env` demo | Interactive (20 min) | Activate environment, check interpreter, edit a non-secret threshold |
| 79–87 (8 min) | Tool testing before LLMs | Explanation (8 min) | Identify deterministic vs. nondeterministic behavior |
| 87–108 (21 min) | Low-stock notifier demo and debugging | Interactive (21 min) | Run app, predict boundary behavior, run three pytest tests |
| 108–112 (4 min) | Explain the independent challenge | Explanation (4 min) | Confirm what is required versus stretch |
| 112–120 (8 min) | Challenge planning and Q&A | Interactive (8 min) | Choose a catalog function to move and 2–3 tests to write |

**Facilitator checkpoint:** Ask learners to show their current working directory before running `pytest`. For live demo tests, everyone should be inside `Examples/ecommart_notify/`, which contains `stock_alert.py`, `config.py`, and `requirements.txt`; run `python -m pytest -q` **there**. Running from the Week 6 top-level directory is not the documented path and may fail to import the example modules.

**After the webinar:** Students complete the required Week 5 catalog restructuring challenge at their own pace. Its scope is `.venv`, dependencies, one environment variable, readable module separation, and 2–3 passing tests; a real Anthropic key, API call, mocking, or framework integration is not required.

## 5. Tools and prerequisites

### You should already have

- **Python 3.10 or newer installed** on your computer for the supplied pinned example dependencies. Python must include `venv`. If you have an older version, update Python before using the supplied demo `requirements.txt`.
- **Completed Weeks 1–5**, including the Week 5 eComMART product catalog, or have its working files available to continue.
- A code editor, such as **Visual Studio Code**, and access to its terminal.
- Basic familiarity with variables, functions, dictionaries, file paths, and running a Python script.
- Introductory knowledge of SQLite and the Week 5 `products` table.

You do **not** need experience with virtual environments, packages, automated testing, agent frameworks, API accounts, or Anthropic.

### Check that Python works

Open a terminal. On **Windows**, try:

```powershell
py --version
```

On **macOS or Linux**, try:

```bash
python3 --version
```

You should see a Python 3 version. If the command is not recognized, check your Python installation before continuing. On Windows, `python --version` may work instead of `py --version`.

### Virtual environment quick reference

A virtual environment is commonly stored in a project folder named `.venv`. Create it **inside the project you are working on**, not once for every Python program on your computer. The commands below assume your terminal is already open in that project's folder.

| Operating system / terminal | Create `.venv` | Activate `.venv` |
|---|---|---|
| Windows — PowerShell | `py -m venv .venv` | `.\.venv\Scripts\Activate.ps1` |
| Windows — Command Prompt | `py -m venv .venv` | `.venv\Scripts\activate.bat` |
| macOS — Terminal | `python3 -m venv .venv` | `source .venv/bin/activate` |
| Linux — Terminal | `python3 -m venv .venv` | `source .venv/bin/activate` |

**How do you know activation worked?** Many terminals display `(.venv)` at the start of the prompt. If it does not appear, the activation may still have worked; later lessons will show how to check which Python interpreter is active.

After activation, use the environment's Python to install the packages listed in the project's `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

Run that installation command only in a folder that already contains the intended `requirements.txt` file. **For the supplied Instructor Demo, run `cd "Week 6/Examples/ecommart_notify"` from the directory that contains `Week 6/` (or navigate to that folder in your file explorer), then use `python -m pip install -r requirements.txt` and `python -m pytest -q` there.** Later lessons will show how to create it. When finished, type `deactivate` to leave the environment.

**Windows PowerShell note:** If the activation script is blocked by an execution-policy message, do not change system-wide security settings blindly. Use Command Prompt with the matching activation command, or follow the focused troubleshooting guidance in `03_Virtual_Environments/02_Creating_and_Activating_venv.md`.

### Early testing setup — a guided preview

Sections **01 and 02 come before the detailed lessons on virtual environments and pip**. You can learn the organizing concepts with Python's built-in features. In Section 02 you will need `pytest` and, for the configuration example, `python-dotenv`. The testing lesson includes a short, copy-and-pasteable setup bridge for beginners; Section 03 then teaches isolated environments thoroughly, and Section 04 explains dependency management and `.env` in depth. This intentional preview is not extra required work. **For these early activities, use a new `.venv` inside `separation_practice/` (not inside the Week 5 catalog or the Week 6 top-level folder).** If you already created it in Section 01, activate that same environment in Section 02; do not make a second one. See `02_Testing_Fundamentals/02_Pytest_Introduction_and_Arrange_Act_Assert.md` for the commands. You will learn the reasons behind these commands in Sections 03–04.

## 6. How to work through the materials

For each lesson:

1. Read the explanation before running the commands. New terms are introduced when you need them.
2. Follow each terminal command from the directory specified in the lesson.
3. Type or inspect the example code, then run it to observe the result.
4. Compare what happened with the expected output or verification step.
5. Complete the guided task before looking at a reference solution.
6. If a command fails, read the complete error message and check the troubleshooting guidance before trying unrelated fixes.
7. Complete the recap or knowledge check, then move to the next lesson.

**Two habits matter especially this week:** check which virtual environment is active, and check which folder the terminal is currently using. Many beginner setup errors come from installing packages into the wrong Python environment or running commands from the wrong folder.

## 7. Important conventions used throughout the week

- The ongoing application is the **eComMART product catalog** from Week 5. Keep your working copy; the independent challenge will use it.
- The **Instructor Demo** is a separate, smaller **eComMART low-stock notifier**.
- The demo's core alert logic uses plain Python functions so the behavior can be tested without an AI service.
- `.venv/` contains local environment files and should not be copied into a shared project submission.
- `requirements.txt` records third-party packages the project requires. Python's built-in modules, such as `os` and `sqlite3`, do not need to be installed with `pip`.
- `.env` stores local configuration values, and `.env.example` shows the names and safe example values that learners can copy. Do not share real secrets or commit a real `.env` file to version control.
- When the lessons introduce an API key, use a clearly fake placeholder value only. **A placeholder does not grant API access, and no live call is expected.**
- Tests will use `pytest`; test filenames start with `test_` so pytest can find them.
- **Core**, **Optional/stretch**, **Expected result**, and **Try it yourself** labels distinguish essential work from extra exploration.

### A preview of the testing idea

A test is a small piece of code that checks another piece of code. For example, if eComMART has 4 units of an item and the alert threshold is 10, a test can check that the result says the item is low in stock.

You will learn the three parts of a test:

1. **Arrange:** prepare the stock number and alert threshold.
2. **Act:** call the function that decides whether stock is low.
3. **Assert:** check that the returned answer matches the expected answer.

You will practise this with ordinary Python functions first. That is also a useful foundation for future *agent tools*: functions that an AI system may be allowed to call to perform a defined task.

## 8. Instructor Demo: build the eComMART low-stock notifier

The instructor will demonstrate how to turn a small Python program into a project that is easier to set up, understand, and test.

The demo builds these pieces incrementally:

1. Start with an isolated virtual environment and a dependency file.
2. Write a simple function that checks whether a product is below its alert threshold.
3. Format a readable message for low-stock products.
4. Move configuration into a dedicated module that can read an environment variable.
5. Keep the program's entry point, stock logic, configuration, and tests in separate files.
6. Run `pytest` to check normal behavior and selected error cases.

The runnable example will live in `Examples/ecommart_notify/`. Its required learning path works **offline** and without a Claude account.

**Optional/stretch only:** `anthropic_client.py` will illustrate where a thin Anthropic SDK wrapper could fit in a later AI-connected version. It is not part of the required execution path, required tests, or required student submission. Do not call the live API during this week's required activities.

## 9. Takeaway Hands-on Exercise: improve your Week 5 catalog

This is the **required self-paced assignment**, separate from the live low-stock notifier demo.

Open the **Week 5 catalog project you built yourself**, starting from `05_Product_Catalog_App.py`. Keep a backup of your working version before changing its organization. Your task is to improve how the existing program is set up and maintained, **not** to rebuild its database operations or add AI features.

By the end of the challenge, you should have:

1. Created and activated a virtual environment for your catalog project.
2. Created a `requirements.txt` that lists the third-party packages your project needs, including `pytest` for testing. Do not add built-in Python modules as dependencies.
3. Configured **at least one environment variable** through a local `.env` file (for example, the SQLite database file path), and changed the program to read it instead of hardcoding the value.
4. Split the application into small modules so configuration and database operations are no longer mixed into one large script.
5. Written and successfully run **2–3 simple pytest tests**, including at least one normal case and one error or boundary case.
6. Checked that the catalog's original add, view, update, and delete behavior still works and that it uses the intended SQLite database.

The lessons in `07_Practice_and_Review/` will walk you through the work. The emphasis is on understanding and verifying each small change, not creating an elaborate framework or writing dozens of tests.

**Not required:** a real Anthropic API key, SDK usage, a live API call, test mocking, complex packaging, or a complete rewrite into classes.

### Instructor assessment rubric (required takeaway)

Use this **10-point rubric** for the self-paced Week 5 catalog submission. Credit the learner's results rather than requiring the exact same filenames as the reference solution. The Week 6 minimum is unchanged.

| Criterion | Points | Evidence |
|---|---:|---|
| Virtual environment | 2 | Project-local `.venv` created and verified with the interpreter path |
| Dependency file | 2 | `requirements.txt` exists and supports installing the project's actual third-party dependencies |
| Environment configuration | 2 | At least one setting is read from an environment variable / local `.env`; `.env.example` shares a safe template |
| Modular organization and continuity | 2 | Application, configuration and database responsibilities separated; original catalog CRUD still works on training data |
| Automated tests | 2 | 2–3 meaningful passing pytest tests, including a normal and a boundary/error scenario |
| **Total** | **10** | **No AI account or live API work required** |

Do **not** grade optional SDK installation, real credentials, mocking, extra tests, or use of classes. Ask the learner to submit a safe project copy and a test-result screenshot or transcript, as explained in the challenge.

## 10. Folder guide

The Week 6 materials will be organized as follows:

```text
Week 6/
├── README.md
├── 01_Organizing_Python_Applications/
│   ├── 01_Modules_Packages_and_Import.md
│   ├── 02_Basic_Project_Structure.md
│   └── 03_Separating_Logic_Config_Database_and_Tests.md
├── 02_Testing_Fundamentals/
│   ├── 01_Why_Automated_Testing_Matters.md
│   ├── 02_Pytest_Introduction_and_Arrange_Act_Assert.md
│   └── 03_Testing_Functions_and_Error_Scenarios.md
├── 03_Virtual_Environments/
│   ├── 01_Why_Isolated_Environments_Matter.md
│   ├── 02_Creating_and_Activating_venv.md
│   └── 03_Installing_Dependencies_with_pip.md
├── 04_Dependency_and_Configuration_Management/
│   ├── 01_Requirements_txt_and_Package_Versions.md
│   ├── 02_Environment_Variables_and_the_env_File.md
│   └── 03_Avoiding_Hardcoded_Credentials_and_API_Keys.md
├── 05_Preparing_for_Agentic_AI_Development/
│   ├── 00_What_Is_an_Agent_Tool.md
│   ├── 01_Isolated_AI_Project_Environments.md
│   ├── 02_Managing_the_Anthropic_SDK_and_Agent_Dependencies.md
│   ├── 03_API_Key_Configuration_for_Claude.md
│   └── 04_Testing_Deterministic_Tools_Before_Connecting_an_LLM.md
├── 06_Building_the_eComMART_Mini_Project/
│   ├── 01_Project_Overview_and_Goals.md
│   ├── 02_Setting_Up_venv_and_requirements_txt.md
│   ├── 03_Refactoring_into_Modules_and_env_Config.md
│   └── 04_Writing_Pytest_Tests_for_the_Project.md
├── 07_Practice_and_Review/
│   ├── 01_Guided_Practice_venv_and_Dependencies.md
│   ├── 02_Guided_Practice_Config_and_Project_Structure.md
│   ├── 03_Independent_Challenge_Restructure_Your_Week5_Catalog.md
│   └── solutions.md
└── Examples/
    ├── 00_START_HERE.md
    └── ecommart_notify/
        ├── requirements.txt
        ├── .env.example
        ├── main.py
        ├── config.py
        ├── stock_alert.py
        ├── anthropic_client.py
        └── tests/
            ├── test_stock_alert.py
            └── test_config.py
```

- `01_Organizing_Python_Applications/` explains modules, imports, and separation of responsibilities.
- `02_Testing_Fundamentals/` teaches beginner-friendly tests, including error cases.
- `03_Virtual_Environments/` explains and practises isolated Python setups.
- `04_Dependency_and_Configuration_Management/` introduces reproducible installations and settings outside source code.
- `05_Preparing_for_Agentic_AI_Development/` introduces AI agent terminology and future SDK-related practices. The Anthropic integration is **optional/stretch**.
- `06_Building_the_eComMART_Mini_Project/` guides the **Instructor Demo** using the low-stock notifier.
- `07_Practice_and_Review/` provides guided exercises, the **required independent Week 5 catalog restructuring challenge**, and solutions.
- `Examples/` holds the demo's runnable files and a dedicated start-here guide. `anthropic_client.py` is an **optional/stretch** example only.

## 11. Completion checklist

Before finishing Week 6, check each item against work you have actually run or demonstrated:

- [ ] I can explain why a project might need its own virtual environment.
- [ ] I created a virtual environment and activated it on my operating system.
- [ ] I installed a dependency with `pip` in the intended environment.
- [ ] I created and used a `requirements.txt` file.
- [ ] I configured and read at least one environment variable.
- [ ] I can explain why a real `.env` file and API key should not be shared publicly.
- [ ] I can explain what a Python module is and why we use `import`.
- [ ] I organized my **own Week 5 catalog** into understandable files while keeping its original features working.
- [ ] I wrote and ran **2–3 passing `pytest` tests** for straightforward behavior, including an error or boundary case.
- [ ] I can explain Arrange → Act → Assert using one of my tests.
- [ ] I can explain, in simple words, why an AI agent tool should be tested before an LLM is allowed to use it.

## 12. Before you begin

Keep your Week 5 catalog files and SQLite database available. You will need them for the independent challenge, but you do **not** need to modify them during the opening lessons. We will start with small module-organization exercises, learn how to test predictable functions, then study isolated project setup and configuration before applying everything to the new low-stock demo and finally to your existing catalog.

If you encounter an error, keep the full terminal message and note which folder and command you used. These details help you and your instructor diagnose the problem instead of guessing.

**Start here:** `01_Organizing_Python_Applications/01_Modules_Packages_and_Import.md`

The first lesson explains how modules and imports make a growing Python program easier to organize. You will study testing next, then virtual environments and configuration.
