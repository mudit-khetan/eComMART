# Instructor Demo — eComMART Low-Stock Notifier: Project Overview and Goals

## Lesson purpose

In Week 5, you built the eComMART B2B product catalog using Python functions and SQLite in one file, `05_Product_Catalog_App.py`. It can store and manage product records, but it has no dedicated virtual environment, dependency list, environment-based configuration, or automated test suite.

This week's **Instructor Demo** shows how those professional project habits fit together. To keep the live webinar manageable, the instructor will create a **fresh, small eComMART low-stock notifier** rather than refactoring the entire Week 5 catalog live.

**Important continuity:** The instructor's notifier is a **separate teaching example**. You will restructure **your own Week 5 catalog** in `07_Practice_and_Review/03_Independent_Challenge_Restructure_Your_Week5_Catalog.md`. Do not replace or overwrite your Week 5 application with the demo code.

**Core/required skills:** create a project-specific `.venv`, record dependencies in `requirements.txt`, configure and read an environment variable, organize code into modules, and write/run **2–3 simple pytest tests**. **Optional/stretch:** a thin Anthropic SDK wrapper for a future assistant. No API account, real key, signup, payment, or live Claude call is needed for required or graded Week 6 work. Any Claude key shown this week is a **nonworking placeholder only**.

## Learning objectives

By the end of the Instructor Demo, you should be able to:

- Explain what problem the stock notifier solves for eComMART.
- Describe the jobs of `main.py`, `stock_alert.py`, `config.py`, and `tests/`.
- Identify which files are code, configuration, dependencies, or automated tests.
- Follow the instructor as they create a virtual environment and install only the core dependencies.
- Explain how `.env` changes the low-stock threshold without editing business logic.
- Predict what a low-stock message should say for a given quantity.
- Understand the three core tests and run them with `python -m pytest -q`.
- Recognize the Anthropic client wrapper as a **separate optional demonstration**, not a requirement.

## 1. The eComMART business request

The warehouse team says:

> “We need a quick way to flag products that are running below our reorder threshold. Another developer should be able to run the tool without changing Python code, and we want a simple way to check that its stock rule still works.”

Imagine the tool receives a list of product names and available quantities. For the demo, these are **sample Python values**, not database records. We deliberately keep SQLite out of the new notifier so the instructor can focus on Week 6 project organization and tests.

| Product | Available units | Threshold | Expected result |
|---|---:|---:|---|
| Wireless Barcode Scanner | 4 | 10 | Low-stock alert |
| Thermal Label Roll | 120 | 10 | No alert |
| USB-C Docking Station | 8 | 10 | Low-stock alert |
| Shipping Label Printer | 10 | 10 | No alert — equality is not low stock |

**Business rule:** create an alert if `quantity < threshold`. If `quantity == threshold`, do not alert.

### What the user should see

For a threshold of `10`, the core demo may print:

```text
=== eComMART Low-Stock Notifier ===
LOW STOCK: Wireless Barcode Scanner has 4 units (threshold: 10).
OK: Thermal Label Roll has 120 units.
LOW STOCK: USB-C Docking Station has 8 units (threshold: 10).
OK: Shipping Label Printer has 10 units.
```

The exact number of sample products is not the learning target. The learning target is that the rule is predictable and that configuration, logic, and tests have clear places.

## 2. What changes compared with Week 5?

| Week 5 product catalog | Week 6 instructor notifier |
|---|---|
| One main `.py` file | Small, clearly named modules |
| Database path written in code | Low-stock threshold read from environment configuration |
| No project-specific dependency record | `requirements.txt` documents packages |
| No isolated project environment | `.venv` keeps packages local to the demo project |
| Features checked manually | Three simple pytest tests check the business rule and configuration |
| Uses SQLite for persistent catalog records | Uses sample in-memory product data to keep this demo focused |

These are **two different applications within the same eComMART story**. The stock notifier demonstrates the techniques; the independent challenge applies them to the existing catalog. You are not expected to merge the two applications this week.

## 3. Project map — find each file's job

The complete **reference example** will appear in `Examples/ecommart_notify/`. For the instructor demo, use this planned layout:

```text
Examples/
└── ecommart_notify/
    ├── .venv/                   # Created by YOU locally; not distributed
    ├── .env                     # Created by YOU locally; not distributed
    ├── requirements.txt         # Core dependencies only
    ├── .env.example             # Safe settings template
    ├── main.py                  # Entry point; displays sample product results
    ├── config.py                # Reads/validates the stock threshold
    ├── stock_alert.py           # Pure stock rule and alert formatting
    ├── anthropic_client.py      # OPTIONAL/STRETCH only; not used by main.py
    └── tests/
        ├── test_stock_alert.py  # Core: stock-rule tests
        └── test_config.py       # Core/example: local configuration test
```

**Important:** `.venv` and `.env` are generated on each student's computer and are **not** part of the provided example files. The actual shipped `Examples/ecommart_notify/` directory contains the files listed in the Week 6 folder plan, including `anthropic_client.py` only as a labeled optional stub/wrapper.

| File | Responsibility | Why it is separate |
|---|---|---|
| `main.py` | Starts the program and prints sample results | Keeps the entry point easy to read |
| `stock_alert.py` | Decides which quantities are low and formats messages | Makes business logic testable without an API or database |
| `config.py` | Reads `LOW_STOCK_THRESHOLD` from the environment and checks its value | Changes settings without rewriting the stock rule |
| `.env.example` | Shows a safe example value that can be copied into `.env` | Lets collaborators configure their own local copy |
| `requirements.txt` | Lists third-party packages needed for the core example | Makes setup reproducible |
| `tests/test_stock_alert.py` | Checks normal and boundary behavior | Catches mistakes in the business rule |
| `tests/test_config.py` | Checks a configuration rule | Makes bad settings visible early |
| `anthropic_client.py` | **Optional/stretch only:** a thin illustration of where an Anthropic SDK integration could go | Prevents required logic from relying on an LLM |

For consistency, use the following **planned core dependencies**: `python-dotenv` to load `.env`, and `pytest` to run tests. The instructor will explain how to install them and record their versions rather than asking beginners to memorize package-version numbers. Python's `os` and `sqlite3` modules are part of the standard library; the demo does not require SQLite.

## 4. The data and logic flow

```text
          .env (local, created by student)
          LOW_STOCK_THRESHOLD=10
                      |
                      v
                  config.py
           read and check threshold
                      |
                      v
main.py --> sample product data --> stock_alert.py
   |                                  |
   |                           compare quantity
   |                           with threshold
   |                                  |
   +<----------- returned alert text --+
   |
   v
print the result in the terminal

Separate verification path:
   tests/test_stock_alert.py + tests/test_config.py
                       |
                       v
              python -m pytest -q
                       |
                       v
             passing or failing tests

OPTIONAL/STRETCH: anthropic_client.py
   Not imported by the required main.py path
   No network calls in the required demo
```

This diagram shows **separation of concerns**: each file has one main responsibility. An **entry point** is the file you run first (`main.py`). A **module** is a Python file whose functions can be imported by another file. A **test** is a small program that checks whether another function behaves as expected.

## 5. Instructor demo sequence

The instructor will build and explain the project in the following order. Students can follow the webinar or reproduce the steps later using the next three lesson files.

| Step | Instructor action | Student observation / interaction | Required? |
|---|---|---|---|
| 1 | Show the Week 5 one-file catalog and identify project-setup limitations | Name one reason another developer might struggle to run it | Context |
| 2 | Create `ecommart_notify`, create/activate `.venv` | Check the Python interpreter being used | **Core** |
| 3 | Install `python-dotenv` and `pytest`; create `requirements.txt` | Explain what one line in `requirements.txt` means | **Core** |
| 4 | Create `.env.example` and local `.env` with `LOW_STOCK_THRESHOLD=10` | Predict what happens if the threshold becomes `5` | **Core** |
| 5 | Add `stock_alert.py`, `config.py`, and `main.py` | Trace one product through the data flow | **Core** |
| 6 | Run the program and compare messages against expected output | Check the equality boundary at `10` units | **Core** |
| 7 | Write and run 2–3 pytest tests | Predict what will fail when `<` is changed to `<=` | **Core** |
| 8 | Point out the optional `anthropic_client.py` integration point | Explain why a real LLM call is unnecessary today | **Optional/stretch** |

The full program is designed for **self-paced learning during the week** plus a **2-hour virtual lecture-and-demo webinar**. The instructor can ask learners to predict outputs, identify errors, and explain what changed, while students complete the independent Week 5 catalog restructure after the session. The overall program targets approximately **70% hands-on/interactive learning and 30% instructor-led explanation**, not two hours of nonstop typing during the webinar.

## 6. Before following the live demo

Check that you have:

1. **Python 3** working in a terminal. On Windows, try `py --version`; on macOS/Linux, try `python3 --version`.
2. Your editor (for example, VS Code) open in the demo project folder.
3. A terminal in that folder, so files are created in the correct place.
4. Read the earlier lessons on `.venv`, `pip`, `.env`, modules, and pytest.
5. Kept a separate copy of your Week 5 `05_Product_Catalog_App.py` and its SQLite database for the later independent challenge.

**There is no need to create an Anthropic account or obtain an API key.** Any optional key example uses the literal fake placeholder `YOUR_PLACEHOLDER_KEY_HERE`. It is not usable for authentication and no live calls are made.

### Venv quick reference

| System | Create | Activate |
|---|---|---|
| Windows PowerShell | `py -m venv .venv` | `.\.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `py -m venv .venv` | `.venv\Scripts\activate.bat` |
| macOS / Linux | `python3 -m venv .venv` | `source .venv/bin/activate` |

After activation, later steps will use `python -m pip ...` and `python -m pytest ...` to ensure they run through the selected environment.

## 7. What counts as complete?

### Core demo completion checklist

- [ ] I can explain why the new notifier is **separate** from my Week 5 catalog.
- [ ] I can create and activate a `.venv` for the demo.
- [ ] I can explain what `requirements.txt` contains and install its packages.
- [ ] I can read `LOW_STOCK_THRESHOLD` from local configuration.
- [ ] I can point to the roles of `main.py`, `stock_alert.py`, `config.py`, and `tests/`.
- [ ] I can run the notifier and understand its alert/no-alert messages.
- [ ] I can run **2–3 simple pytest tests** and understand their results.
- [ ] I understand that no real Anthropic API request is involved.

### Optional/stretch — not part of the required bar

- Inspect the separate `anthropic_client.py` wrapper as an example of a future integration point.
- Discuss what additional authorization, network-error handling, and API testing might require in later weeks.
- Explore additional tests beyond the required two or three.

**Not required:** a working Claude integration, test mocking, a real key, an API subscription, or any paid usage.

## 8. Guided understanding check

Before the instructor builds the program, answer these questions:

1. If `LOW_STOCK_THRESHOLD=10`, should a product with quantity `10` trigger a low-stock alert? Why?
2. Which file should contain the comparison `quantity < threshold`?
3. Which file should read the threshold from `.env`?
4. Which file should you run to start the program?
5. Why should automated tests run without depending on Anthropic?
6. Which application will you restructure in the **Takeaway Hands-on Exercise**?

**Self-check:** (1) No, because the rule is strictly less than. (2) `stock_alert.py`. (3) `config.py`. (4) `main.py`. (5) The stock rule is local, predictable Python behavior and should not depend on network availability or service charges. (6) Your **own existing Week 5 product catalog**, not the new instructor notifier.

## 9. Where to go next

- `02_Setting_Up_venv_and_requirements_txt.md` — create the demo folder, isolated environment, and dependency record.
- `03_Refactoring_into_Modules_and_env_Config.md` — organize the **new demo** into small modules and load the low-stock threshold from `.env`. (“Refactoring” here means organizing this small demo, not rewriting your Week 5 catalog.)
- `04_Writing_Pytest_Tests_for_the_Project.md` — add 2–3 local tests and demonstrate how a test catches a bug.
- `Examples/00_START_HERE.md` and `Examples/ecommart_notify/` — reference code that accompanies the instructor's walkthrough.
- `07_Practice_and_Review/03_Independent_Challenge_Restructure_Your_Week5_Catalog.md` — your required self-paced continuity exercise using **your own Week 5 app**.

**Key takeaway:** Week 6 does not require a more complicated application. It requires a **more maintainable way to run, configure, and test simple Python code**. That foundation will make later agentic AI projects easier to reason about and verify.
