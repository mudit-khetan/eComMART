# Independent Challenge — Restructure Your Week 5 eComMART Catalog

**Week 6 · Practice and Review · Required Takeaway Hands-on Exercise (self-paced)**

## Challenge overview

Last week, you built an eComMART product catalog that stores products in SQLite. It can add, view, search, update, and delete products, and the data persists when the application closes. It works—but the reference application keeps all those functions in a single file, `05_Product_Catalog_App.py`, and its SQLite database path is set in Python source code.

Your task is to **improve your own Week 5 catalog without changing what it does**. Make a safe copy, give it a virtual environment, record dependencies, configure one environment variable, move reusable code into modules, and write **2–3 simple pytest tests**. This is not a new low-stock notifier and not a task to copy the Instructor Demo. The goal is to keep your **existing catalog** working while making it easier for another developer to run and maintain.

**Required bar:** `.venv` + `requirements.txt` + **one environment variable** + a clear separation into modules + **2–3 passing pytest tests**. No API signup, real credentials, or live AI calls are needed. **Optional/stretch only:** extra tests, mocking, an Anthropic SDK wrapper, or advanced packaging.

> **Try the tasks independently before opening `solutions.md`.** The starter hints and checks below are intentionally more detailed than the final solution so a beginning programmer can proceed without guessing at the workflow.

## What you will learn

You will practice recreating a project environment, separating responsibilities, configuring a local database path, testing a normal scenario and an error or boundary case, and confirming that an improvement has not broken the original CRUD menu.

## 1. Start with your own Week 5 work

Find the product catalog you created in Week 5. The reference example is `Week 5/Examples/05_Product_Catalog_App.py`; your own filename may differ. Also find your SQLite database and, if you used it, `setup_database.py`.

The reference Week 5 application has:

- `validate_product(name, category, price, stock)` for basic input checks.
- `get_all_products()`, `get_product_by_id(product_id)`, `add_product(...)`, `update_product(...)`, and `delete_product(...)` for SQLite database operations.
- Menu and display functions for user interaction.
- A `products` table with columns `product_id`, `name`, `category`, `price`, and `stock`.
- A `DATABASE_PATH` constant based on the original script location, not an environment setting.

**Your implementation may use different function names or file names.** Keep your own working functions and adapt the instructions rather than replacing your work with the reference program.

### Safety rule — preserve your original

Make a **new folder and copy** the working Week 5 `.py` files and the current `ecommart.db` into it. Do not move or overwrite your only Week 5 copy. The supplied Week 5 `setup_database.py` creates the table and inserts missing starter items without deleting existing rows, but you should still work on a copied database. **Never run a reset/seed script without checking whether it replaces data.**

## 2. Expected end state

A straightforward beginner-friendly example is:

```text
ecommart_catalog_week6/
├── .venv/                 # local Python environment; do not share
├── .env                   # local settings; do not share
├── .env.example           # safe example configuration; share
├── .gitignore
├── requirements.txt
├── main.py                # menu and program entry point
├── catalog.py             # validation and reusable catalog logic
├── database.py            # SQLite access functions
├── config.py              # read the database path setting
├── ecommart.db            # COPY of your Week 5 database
├── setup_database.py      # optional: copied Week 5 setup helper
└── tests/
    └── test_catalog.py   # 2–3 pytest tests
```

This layout is a **suggested organization**, not a requirement to use those precise file names. A reasonable split with a menu file, database logic, configuration, and tests satisfies the objective. You do **not** need to introduce classes, create an installable Python package, or redesign the database.

### Responsibilities

| File | Main job | Avoid |
|---|---|---|
| `main.py` | Show menu, read input, print results | Embedding SQL or credentials |
| `catalog.py` | Validate product data and any reusable business rules | Running the interactive menu on import |
| `database.py` | Open SQLite connections and implement CRUD | Calling `input()` in database helpers |
| `config.py` | Read `ECOMMART_DB_PATH` from the environment | Creating the products table automatically on import |
| `tests/test_catalog.py` | Assert expected program behavior | Modifying your original Week 5 database |

## 3. Task 1 — Create and verify a virtual environment

Open a terminal in the new `ecommart_catalog_week6/` folder, not in the original Week 5 folder.

| Terminal | Create environment | Activate |
|---|---|---|
| Windows PowerShell | `py -m venv .venv` | `.\.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `py -m venv .venv` | `.venv\Scripts\activate.bat` |
| macOS/Linux | `python3 -m venv .venv` | `source .venv/bin/activate` |

If activation is blocked, use `.venv\Scripts\python.exe` on Windows or `.venv/bin/python` on macOS/Linux in place of `python` for remaining commands.

Run:

```bash
python -c "import sys; print(sys.executable)"
```

**Expected:** the interpreter path is inside `ecommart_catalog_week6/.venv`. If it is not, activate the right environment before continuing.

## 4. Task 2 — Make requirements.txt reproducible

Create `requirements.txt` beside `main.py`:

```text
python-dotenv==1.2.4
pytest==9.2.0
```

`sqlite3` is included with normal Python installations and does **not** need a separate `pip` entry. Install and verify:

```bash
python -m pip install -r requirements.txt
python -m pytest --version
```

**Expected:** pytest reports its version, and `python -m pip show python-dotenv` displays the installed package. Avoid copying packages from a global Python environment. These are the third-party dependencies needed for this exercise; Anthropic is **not** required.

## 5. Task 3 — Configure the database path with one environment variable

Create `.env.example`:

```dotenv
# Copy this file to .env; do not add real secrets
ECOMMART_DB_PATH=ecommart.db
```

Make a local `.env` containing the same value. The variable name must match exactly. It is a **file path**, not a password or API key. Place a **copy** of your Week 5 `ecommart.db` in your new project root so the example value points to it.

Create `.gitignore`:

```gitignore
.venv/
.env
__pycache__/
.pytest_cache/
*.pyc
```

**Note:** Your working `ecommart.db` is a local training data file. If you later share the project, decide whether to include a sanitized demo database; never share private production data.

Create `config.py`:

```python
import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_DIR = Path(__file__).resolve().parent


def get_database_path():
    """Return a database path anchored to this project folder."""
    load_dotenv()
    raw_path = os.getenv("ECOMMART_DB_PATH", "ecommart.db")
    path = Path(raw_path).expanduser()
    return path if path.is_absolute() else PROJECT_DIR / path
```

The important detail is that a **relative path is anchored to the project folder**, not whichever directory the terminal happens to be in. A different warehouse could choose a different local database path without editing Python code. Use this function where your old source currently defines `DATABASE_PATH`.

**Check before proceeding:** Run `python -c "from config import get_database_path; print(get_database_path())"`. It should print a path ending in `ecommart_catalog_week6/ecommart.db` (Windows uses backslashes). The file should already exist because you copied it.

## 6. Task 4 — Separate the existing code into modules

Use the Week 5 program as your **source of truth**. Move code in small pieces so you can run a check after each change.

1. Create `catalog.py`. Move your product validation function (such as `validate_product`) into it. Preserve its argument names, validation rules, and error messages where practical.
2. Create `database.py`. Move the SQLite CRUD functions into it. Add imports for `sqlite3`, `get_database_path`, and `validate_product` if used. Where the old function had `sqlite3.connect(DATABASE_PATH)`, use `sqlite3.connect(get_database_path())`.
3. Create `main.py`. Move the menu, input parsing, display functions, and program entry point into it. Import the CRUD helpers from `database.py` instead of copying their SQL.
4. Make sure `main.py` only starts the menu when run directly, using `if __name__ == "__main__":`. This prevents the menu from opening when a test imports a module.
5. Move no more code than necessary. Keep SQL placeholders (`?`) rather than building SQL statements from text entered by the user.

For example, the start of `database.py` might look like:

```python
import sqlite3
from config import get_database_path
from catalog import validate_product


def get_all_products():
    connection = sqlite3.connect(get_database_path())
    try:
        cursor = connection.execute(
            "SELECT product_id, name, category, price, stock "
            "FROM products ORDER BY product_id"
        )
        return cursor.fetchall()
    finally:
        connection.close()
```

This is a **small example**, not a replacement for your five CRUD operations. Move your own tested SQL and functions over. Keep parameterized queries, commits, rollbacks, and connection cleanup that your Week 5 version already uses.

### Critical continuity check

Before writing tests, run `python main.py` and check all the Week 5 capabilities still work:

| Original capability | Your manual check |
|---|---|
| Add | Add a disposable product to the **copied** database |
| View | New product appears in the list |
| Search | Find the product by ID |
| Update | Change its stock or price and confirm the new value |
| Delete | Remove the disposable product and confirm it is gone |
| Persistence | Exit, reopen `python main.py`, and confirm remaining products are preserved |

**Do not** use the original Week 5 database for these experiments. If one operation breaks after moving code, fix the corresponding import or function call before moving to the testing section.

## 7. Task 5 — Write 2–3 simple pytest tests

Create `tests/test_catalog.py`. Start with **three tests of pure validation**—they do not touch SQLite and therefore cannot accidentally alter your catalog. The reference Week 5 application defines `validate_product(name, category, price, stock)` and raises `ValueError` on invalid input. Adapt the examples if your own function names or argument order differ.

```python
import pytest
from catalog import validate_product


def test_valid_product_is_accepted():
    # Arrange
    name, category, price, stock = "USB Cable", "Accessories", 299.0, 5
    # Act
    result = validate_product(name, category, price, stock)
    # Assert: the Week 5 reference returns None for valid input
    assert result is None


def test_empty_product_name_is_rejected():
    # Arrange
    name = ""
    # Act and Assert
    with pytest.raises(ValueError, match="Product name must not be empty"):
        validate_product(name, "Accessories", 299.0, 5)


def test_negative_stock_is_rejected():
    # Arrange
    stock = -1
    # Act and Assert
    with pytest.raises(ValueError, match="Stock cannot be negative"):
        validate_product("USB Cable", "Accessories", 299.0, stock)
```

- **Arrange** prepares the inputs.
- **Act** calls the function under test.
- **Assert** checks the result or confirms an expected error.
- `pytest.raises(ValueError)` checks that invalid input is *rejected*. The `match=` message checks wording specific to the supplied reference function; update it if your own Week 5 program used different messages.

**If your function returns a success value instead of `None`, test that documented result.** If your function prints a warning rather than raising an exception, adapt your tests to the actual Week 5 behavior or improve error handling deliberately, then verify that the menu still handles the error gracefully.

### Run the tests

From the **project root** (the folder containing `catalog.py`), run:

```bash
python -m pytest -q
```

**Expected with the example reference validation function:**

```text
3 passed
```

The exact time and output decoration may differ. If importing `catalog` fails, confirm the terminal is in the project root and that `catalog.py` exists there. **Do not add database-writing tests to satisfy the minimum**; the three safe tests above are sufficient.

### Optional/stretch — database testing with a disposable copy

If you want to test SQLite CRUD, create a **separate temporary test database** and point `ECOMMART_DB_PATH` to it for the test. Never run add/update/delete tests against your only project database. Creating disposable test databases and using pytest fixtures or monkeypatching are **bonus skills, not required for Week 6**.

## 8. Final acceptance checks

Before submitting, verify the following:

| Requirement | Evidence to show |
|---|---|
| Isolated environment | Python interpreter path points to `.venv` |
| Dependencies | `requirements.txt` exists; `python -m pytest --version` succeeds |
| Configuration | `.env.example` contains `ECOMMART_DB_PATH`; `config.py` reads it |
| Organization | Menu, validation, and database helpers are separated into clearly named modules |
| Unchanged behavior | Add/view/search/update/delete and persistence work on your **copied** SQLite data |
| Automated testing | `python -m pytest -q` shows **2–3 passing tests** |
| Safe sharing | `.env` and `.venv/` are ignored; no real keys in source or submissions |

**Suggested submission:** A copy of the project **without** `.venv/`, `.env`, caches, or secrets, plus a screenshot or copied terminal output showing the pytest result. Include `.env.example` so the instructor knows which setting to configure. If your instructor wants a working sample database, provide **only the synthetic or training dataset**, not private records.

### Instructor rubric — 10 points

This rubric checks the existing required outcomes; it does **not** add extra assignments. The instructor can award partial credit based on the student's working copy of the Week 5 catalog.

| Required outcome | Points | Evidence |
|---|---:|---|
| Local virtual environment created and verified | 2 | Interpreter path belongs to the project's `.venv` |
| Dependencies recorded | 2 | `requirements.txt` lists actual third-party requirements and can be installed |
| One environment variable configured safely | 2 | `.env` read by code; safe `.env.example` provided; no real secrets shared |
| Code organized without losing Week 5 behavior | 2 | Clear modules; original CRUD and SQLite persistence still function |
| 2–3 meaningful pytest tests pass | 2 | Passing test output; normal and boundary/error coverage |
| **Total** | **10** | Optional AI, mocking and extra tests are not graded |

## 9. Troubleshooting

| Problem | Likely reason | Beginner-friendly fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'dotenv'` | Environment not active or dependency not installed | Activate `.venv`, then `python -m pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'catalog'` | Wrong folder or filename | Open project root; confirm `catalog.py` is there and run `python -m pytest -q` from that folder |
| `sqlite3.OperationalError: no such table: products` | Pointed to a new/empty SQLite file | Verify `ECOMMART_DB_PATH`; copy your existing populated training database into the project |
| Menu opens during pytest import | Menu function runs at import time | Put the menu call under `if __name__ == "__main__":` |
| Data disappeared | Wrong database path or copy | Check the resolved path; compare against your untouched Week 5 original |
| Test fails because validation message differs | Your Week 5 version has different wording | Adjust expected message to the behavior you intentionally kept |
| `.env` edit has no effect | Shell environment variable takes priority | Check/unset the old shell variable or use a fresh terminal |
| Python says `No module named pytest` | pytest is in another environment | Verify `sys.executable`; reinstall inside `.venv` |

## 10. Reflect on the eComMART story

Answer in a few sentences each:

1. Why is it safer to restructure a **copy** of the Week 5 catalog rather than the original?
2. How does `requirements.txt` help another eComMART developer run your application?
3. Why is `ECOMMART_DB_PATH` better as a setting than a path edited in the main Python file?
4. What does each test prove? Which bug might it catch next week?
5. Why should an eventual AI agent call **tested catalog functions** instead of inventing or writing SQL directly?

## 11. Completion checklist — required takeaway

- [ ] I began with **my own Week 5 product catalog** and kept a backup.
- [ ] I created and verified a local `.venv`.
- [ ] I created `requirements.txt` and installed its dependencies.
- [ ] I configured **at least one environment variable** using `.env`.
- [ ] I included a safe `.env.example` and `.gitignore`.
- [ ] I separated application/menu code, database functions, and configuration into modules.
- [ ] All original catalog actions and data persistence still work on the copied database.
- [ ] I wrote **2–3 simple pytest tests** and saw them pass.
- [ ] My tests do not alter my original Week 5 data.
- [ ] I required **no** Anthropic account, real API key, payment, or live LLM call.

**After submitting:** Compare your approach with `07_Practice_and_Review/solutions.md` when it becomes available. The point is not to create exactly the same filenames as the reference, but to demonstrate a safely configured, reproducible, testable version of the **catalog you already built**.
