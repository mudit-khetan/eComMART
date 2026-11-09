# Week 6 — Practice and Review: Reference Solutions

**eComMART · Instructor/reference copy · Open after attempting the exercises**

## How to use these solutions

The answers follow the three activities in `07_Practice_and_Review/` in order. First attempt each task and run its checkpoint; then compare your work with the reference. A correct solution can use different names or organization if it meets the requirements and preserves the behavior of **your own Week 5 catalog**.

**Required bar:** a project `.venv`, a `requirements.txt`, at least one environment variable, separated modules, and **2–3 simple passing pytest tests** in the independent challenge. **Optional/stretch:** extra automated tests, test fixtures/mocking, and Anthropic integration. You need no real API key, Anthropic account, signup, payment, or live LLM/API call.

> These are example answers, not additional tasks to submit. Never run catalog update/delete exercises against your only copy of the Week 5 database.

---

## Solution 1 — Guided Practice: venv and Dependencies

**Companion:** `01_Guided_Practice_venv_and_Dependencies.md`

### 1. Create the practice project

Create a folder called `ecommart_setup_practice` and open a terminal **inside** it. Confirm the directory with `Get-Location` (PowerShell), `cd` (Windows Command Prompt), or `pwd` (macOS/Linux).

### 2. Create and activate a local environment

| Terminal | Create | Activate |
|---|---|---|
| Windows PowerShell | `py -m venv .venv` | `.\.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `py -m venv .venv` | `.venv\Scripts\activate.bat` |
| macOS/Linux | `python3 -m venv .venv` | `source .venv/bin/activate` |

If your organization blocks activation, run the `.venv` interpreter directly: `.venv\Scripts\python.exe` (Windows) or `.venv/bin/python` (macOS/Linux), replacing `python` in later commands. Do not change system-wide security settings.

Check which Python will run:

```bash
python -c "import sys; print(sys.executable)"
```

**Expected:** its path contains your new `ecommart_setup_practice/.venv` directory (with the OS's path separators). Seeing `(.venv)` in the terminal prompt is useful, but this interpreter check is stronger evidence.

### 3. Record and install dependencies

Create `requirements.txt`:

```text
python-dotenv==1.2.4
pytest==9.2.0
```

Then run, from the project root:

```bash
python -m pip install -r requirements.txt
python -m pip show python-dotenv
python -m pip show pytest
python -m pytest --version
```

**Expected:** both installed packages show the pinned versions, and the last command reports `pytest 9.2.0` (possibly with extra formatting). Package installation may need access to your approved Python package index, **not** an AI API.

### 4. What should be shared?

| File/folder | Share? | Explanation |
|---|---|---|
| `requirements.txt` | Yes | Lets another developer install the selected versions |
| Python source files | Yes | Contains the application behavior |
| `.venv/` | No | A local, operating-system-specific environment |
| `.env` | No | Contains local configuration and could contain secrets |
| `.env.example` | Yes | Safe template without genuine secrets |

**Mini-challenge solution:** `No module named pytest` often means (a) pytest was installed in a **different** Python environment or (b) dependencies have not yet been installed in the newly created `.venv`. Check `python -c "import sys; print(sys.executable)"`, select the correct environment, and rerun `python -m pip install -r requirements.txt`.

**Knowledge-check takeaway:** `requirements.txt` travels between computers; `.venv` is recreated on each computer.

---

## Solution 2 — Guided Practice: Configuration and Project Structure

**Companion:** `02_Guided_Practice_Config_and_Project_Structure.md`

### 1. Correct structure

```text
ecommart_config_practice/
├── .venv/                 # created locally; not shared
├── .env                   # created locally; not shared
├── .env.example
├── .gitignore
├── requirements.txt
├── stock_alert.py
├── config.py
└── main.py
```

Use the same `requirements.txt`, create and activate a new `.venv` **in this folder**, and run `python -m pip install -r requirements.txt`.

Create `.env.example` and copy its contents to `.env`:

```dotenv
LOW_STOCK_THRESHOLD=10
```

Create `.gitignore`:

```gitignore
.venv/
.env
__pycache__/
.pytest_cache/
*.pyc
```

### 2. `stock_alert.py` — business rule

```python
def is_low_stock(quantity, threshold):
    """Low stock means strictly fewer units than the threshold."""
    return quantity < threshold


def format_stock_message(name, quantity, threshold):
    if is_low_stock(quantity, threshold):
        return f"LOW STOCK: {name} has {quantity} units (threshold: {threshold})."
    return f"OK: {name} has {quantity} units."
```

`10` units at threshold `10` is **not** low stock. The function has no file access, network access, or side effects.

### 3. `config.py` — one configurable setting

```python
import os
from dotenv import load_dotenv


def get_low_stock_threshold():
    load_dotenv()
    raw_value = os.getenv("LOW_STOCK_THRESHOLD", "10")
    try:
        threshold = int(raw_value)
    except ValueError as error:
        raise ValueError("LOW_STOCK_THRESHOLD must be a whole number.") from error
    if threshold < 0:
        raise ValueError("LOW_STOCK_THRESHOLD cannot be negative.")
    return threshold
```

An environment variable is read as text, so `int()` is necessary. The `ValueError` protects the application against nonsensical settings.

### 4. `main.py` — program entry point

```python
from config import get_low_stock_threshold
from stock_alert import format_stock_message


def main():
    threshold = get_low_stock_threshold()
    products = [
        ("Wireless Barcode Scanner", 4),
        ("Thermal Label Roll", 120),
        ("USB-C Docking Station", 10),
    ]
    for name, quantity in products:
        print(format_stock_message(name, quantity, threshold))


if __name__ == "__main__":
    main()
```

Run:

```bash
python main.py
```

**Expected with `LOW_STOCK_THRESHOLD=10`:**

```text
LOW STOCK: Wireless Barcode Scanner has 4 units (threshold: 10).
OK: Thermal Label Roll has 120 units.
OK: USB-C Docking Station has 10 units.
```

Change `.env` to `LOW_STOCK_THRESHOLD=12` and run the script again. **Expected:** the Docking Station now also produces a low-stock alert. If the value does not change, check whether the terminal already defines `LOW_STOCK_THRESHOLD`; `load_dotenv()` normally does not overwrite a preexisting shell variable. Use a clean terminal without that setting.

**Invalid-setting mini-challenge:** `LOW_STOCK_THRESHOLD=banana` makes `int("banana")` fail. The program should report `ValueError: LOW_STOCK_THRESHOLD must be a whole number.` Restore `10` afterward.

**Which file changes?** Changing the rule from *below* to *at or below* affects `stock_alert.py`. Changing only the warehouse's chosen number affects `.env`.

**Optional/stretch test only** (the guided exercise does not require a test):

```python
# tests/test_stock_alert.py
from stock_alert import is_low_stock


def test_equal_threshold_is_not_low():
    assert is_low_stock(10, 10) is False
```

---

## Solution 3 — Independent Challenge: Reorganize Your Own Week 5 Catalog

**Companion:** `03_Independent_Challenge_Restructure_Your_Week5_Catalog.md`

Unlike the separate Instructor Demo, this is a continuation of **your existing Week 5 application**, not a new toy app. The Week 5 reference is `05_Product_Catalog_App.py`; its original implementation contains `validate_product`, five SQLite CRUD functions, and console-menu functions. Your own version may differ. Keep its behavior, data, input validation, confirmation before deletion, and parameterized SQL.

### 1. Copy first; do not work on the original

Copy the original `05_Product_Catalog_App.py` (or your version), a **copy** of `ecommart.db`, and any existing setup helper into `ecommart_catalog_week6/`. Check that the database copy already contains the `products` table. Do not rerun any script that might reset or overwrite records.

One acceptable target structure:

```text
ecommart_catalog_week6/
├── .venv/             # local only
├── .env               # local only
├── .env.example
├── .gitignore
├── requirements.txt
├── ecommart.db         # copy of training database
├── config.py
├── catalog.py
├── database.py
├── main.py
└── tests/
    └── test_catalog.py
```

Create and select `.venv` using the commands from Solution 1. Use the same pinned `requirements.txt` and install it with `python -m pip install -r requirements.txt`. No Anthropic dependency is needed.

### 2. Configuration files

`.env.example` (also copy to a local `.env`):

```dotenv
ECOMMART_DB_PATH=ecommart.db
```

`.gitignore`:

```gitignore
.venv/
.env
__pycache__/
.pytest_cache/
*.pyc
```

`config.py`:

```python
import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_DIR = Path(__file__).resolve().parent


def get_database_path():
    """Resolve a local database setting relative to this project."""
    load_dotenv()
    raw_path = os.getenv("ECOMMART_DB_PATH", "ecommart.db")
    path = Path(raw_path).expanduser()
    return path if path.is_absolute() else PROJECT_DIR / path
```

**Check:** `python -c "from config import get_database_path; print(get_database_path())"` should show the path to your **copied** database. SQLite can silently create a new empty file if it is given a wrong path; check that the file exists and contains the expected table before testing CRUD.

### 3. `catalog.py` — preserve the Week 5 validation rule

The Week 5 **reference** function is reproduced here because its exact return values and error strings matter to the three sample tests. If your function differs, adapt the tests to **your function's documented behavior**.

```python
def validate_product(name, category, price, stock):
    """Raise ValueError for invalid product input; otherwise return None."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Product name must not be empty.")
    if not isinstance(category, str) or not category.strip():
        raise ValueError("Product category must not be empty.")
    if isinstance(price, bool) or not isinstance(price, (int, float)):
        raise ValueError("Price must be a number.")
    if price <= 0:
        raise ValueError("Price must be greater than 0.")
    if isinstance(stock, bool) or not isinstance(stock, int):
        raise ValueError("Stock must be a whole number.")
    if stock < 0:
        raise ValueError("Stock cannot be negative.")
```

The function ends without an explicit `return`, so a valid input produces `None`. That is intentional and mirrors the Week 5 example.

### 4. `database.py` — move, do not reinvent, SQLite functions

Move **all five** Week 5 data-access functions from the original file into `database.py` without changing their SQL or return contracts:

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

In the **other four original functions**, replace their old `sqlite3.connect(DATABASE_PATH)` call with `sqlite3.connect(get_database_path())`:

- `get_product_by_id(product_id)` — return a row or `None`; preserve `WHERE product_id = ?`.
- `add_product(name, category, price, stock)` — validate, insert with `?` placeholders, commit, and return the new ID.
- `update_product(product_id, name, category, price, stock)` — validate, update with placeholders, commit on success, and return `True`/`False`.
- `delete_product(product_id)` — delete with a placeholder, commit on success, and return `True`/`False`.

Keep the **existing** `try`/`except sqlite3.Error`/`rollback`/`finally: connection.close()` behavior from Week 5. Do **not** put `input()` or `print()` inside these functions. The full CRUD implementations are already in the Week 5 source; copying them is safer than retyping new SQL for this challenge.

### 5. `main.py` — keep the real catalog interface

Move the Week 5 user-interaction functions to `main.py`:

`read_integer`, `read_number`, `format_product_row`, `view_all_products`, `search_product`, `add_product_menu`, `update_product_menu`, `delete_product_menu`, `show_menu`, and `main`.

At the top of `main.py`, add:

```python
import sqlite3
from config import get_database_path
from database import (
    get_all_products,
    get_product_by_id,
    add_product,
    update_product,
    delete_product,
)
```

**One required line change in the original `main()`**: replace `if not DATABASE_PATH.exists():` with:

```python
if not get_database_path().is_file():
    print("Database file not found.")
    print("Check ECOMMART_DB_PATH and your copied database.")
    return
```

Keep the rest of the Week 5 menu and its **six options** intact. At the bottom, keep:

```python
if __name__ == "__main__":
    main()
```

This guard means tests can import functions without accidentally launching an interactive menu. `main.py` should call functions from `database.py` rather than contain duplicate SQL.

### 6. `tests/test_catalog.py` — the three required example tests

Run `python -m pytest -q` from the folder containing `catalog.py`.

```python
import pytest
from catalog import validate_product


def test_valid_product_is_accepted():
    # Arrange
    name, category, price, stock = "USB Cable", "Accessories", 299.0, 5
    # Act
    result = validate_product(name, category, price, stock)
    # Assert
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

**Expected:** `3 passed` (timing and report details vary). These tests only check `validate_product`, so they do **not** read or modify the SQLite database. The required bar is **2–3 simple tests**, not comprehensive database testing. More tests and temporary test databases are optional/stretch.

### 7. Verify your *existing* app still works

Run `python main.py` with the copied `ecommart.db`. Check each original operation manually on a disposable product:

| Action | Expected check |
|---|---|
| Add | New ID reported; row appears in catalog |
| View | Product list contains the new row |
| Search | Search by ID displays the correct row |
| Update | New price/stock appears after saving |
| Delete | Confirmation is required; row disappears afterward |
| Persistence | Restarting the app leaves other copied records intact |

An empty `products` table or `no such table: products` usually means the configured path points to the wrong/new database file. Recheck the copy **before** attempting to seed or edit anything.

### 8. Submission checks

- [ ] Original Week 5 code and database remain untouched.
- [ ] `sys.executable` points into this project's `.venv`.
- [ ] `requirements.txt` pins `python-dotenv` and `pytest`.
- [ ] `.env.example` documents `ECOMMART_DB_PATH`; `.env` stays local.
- [ ] Menu, validation, and SQLite access are in separate modules.
- [ ] The original menu, all five CRUD functions, and data persistence still work.
- [ ] `python -m pytest -q` reports **2–3 passing tests**.
- [ ] Submission excludes `.venv/`, `.env`, cache files, and real secrets.

**Reflection answers:** A copy protects the original; dependency pins make setup reproducible; `ECOMMART_DB_PATH` lets environments use different database locations without source edits; validation tests protect good input, missing names, and negative stock; future AI agents should call **existing, verified Python tools** rather than invent SQL or modify database records unpredictably.

---

## Instructor notes and common review mistakes

1. **Wrong interpreter:** If pytest is missing, check `sys.executable` before reinstalling anything.
2. **Import opens the menu:** Ensure the entry-point guard exists and only `main.py` handles user interaction.
3. **False test success:** A passing validation suite does **not** prove database CRUD works; manual copied-database acceptance checks are still essential.
4. **Lost database:** A wrong SQLite path may create a blank database. Recheck `ECOMMART_DB_PATH` and the original Week 5 copy.
5. **Secret handling:** `.gitignore` prevents *new* tracked files, not the disclosure of secrets already committed.
6. **Incorrect scope:** A live Claude/Anthropic API call, mocks, fixtures, or extra test count are **not** needed for completion.

**Next:** `../Examples/00_START_HERE.md` explains how to use the separate instructor low-stock notifier code when those example files are provided.
