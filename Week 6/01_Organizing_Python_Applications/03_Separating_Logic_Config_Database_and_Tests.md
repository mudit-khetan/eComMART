# Separating Logic, Configuration, Database, and Tests

## Lesson purpose

In the previous lesson, you gave the eComMART low-stock notifier a small folder structure. Now we will make the **responsibilities** inside that structure clearer. A folder layout alone is not enough if every file still performs every job.

Think of the Week 5 product catalog: one Python script handles product operations and SQLite storage, while the database path is written in the script. That is a sensible starting point for learning SQL. In Week 6, we learn how to keep that code easier to change and test **without changing what the catalog does**.

For today's demonstration, we continue with a **small, separate low-stock alert program**. You will restructure **your own Week 5 catalog** only in the independent challenge later in Week 6.

**Core for Week 6:** understand which responsibility belongs in which file, read **one** setting from `.env`, and keep business logic simple enough to test. **Optional/stretch:** add a database module to a larger catalog or explore an AI wrapper. **No real API key, signup, payment, or live LLM call is required.**

## Learning objectives

By the end of this lesson, you will be able to:

- Explain *separation of concerns* in everyday language.
- Identify the roles of `main.py`, `stock_alert.py`, `config.py`, a possible `database.py`, and `tests/`.
- Pass a configuration value into a function rather than hardcoding it inside that function.
- Describe why tests should focus on predictable functions.
- Run a tiny multi-file eComMART program and predict its output.
- Recognize which improvements belong to the required takeaway versus optional extensions.

## 1. What does “separation of concerns” mean?

A **concern** is simply a job your program needs to do. *Separation of concerns* means giving different jobs clear homes instead of putting them all into one long function.

Imagine the eComMART team asks for three changes: change the wording of low-stock alerts, change the alert threshold, and change where catalog records are stored. Those are three different jobs. Keeping them separate lets one change happen with less risk of breaking the others.

| Responsibility | Plain-language question | Suggested home |
|---|---|---|
| Entry point | What happens when I start the program? | `main.py` |
| Business logic | When is stock considered low, and what message do we return? | `stock_alert.py` |
| Configuration | What threshold did this computer's user choose? | `config.py` and local `.env` |
| Database access | How do we save or retrieve product rows from SQLite? | `database.py` in a database-backed app |
| Tests | Does a specific function behave as expected? | `tests/test_*.py` |

**Important:** A module is still a Python file. You do not need classes, advanced design patterns, or a new framework to separate these jobs.

## 2. The difference between logic and input/output

Consider this question: “Should we alert if a Wireless Mouse has 3 units and the threshold is 5?”

The **business rule** can be written as a function:

```python
def is_low_stock(stock, threshold):
    return stock < threshold
```

This function needs only two inputs. It does not print, ask a user a question, open a database, or read an API key. Given the same inputs, it gives the same result. We call this **deterministic** or **predictable** behavior.

In contrast:

```python
stock = int(input("Enter stock: "))
print(is_low_stock(stock, 5))
```

`input()` and `print()` are **input/output** operations: they communicate with a person or another system. They are useful, but keeping them out of the business-rule function makes that rule easier to test automatically.

**Key idea:** Let `main.py` coordinate work; let small functions calculate and return answers.

## 3. Guided build — give each job a file

Create a **new** folder named `separation_practice` beside the `structure_practice` example from the previous lesson. Do not overwrite that example or your Week 5 catalog.

```text
week6_practice/
├── structure_practice/       # from the preceding lesson (keep it)
└── separation_practice/      # work here
    ├── main.py
    ├── stock_alert.py
    ├── config.py
    ├── .env
    ├── .env.example
    └── tests/                # empty today
```

**One-time beginner setup for this early lesson:** Later sections teach `venv`, `pip`, and `.env` from the beginning. For now, `config.py` uses the `python-dotenv` package, which is not part of Python itself. If you already have an active project virtual environment, use it and run `python -m pip install python-dotenv`. Otherwise, you can follow these minimal commands from the `separation_practice` folder; detailed explanations appear in Sections 03 and 04:

| System | Create and activate a temporary local environment |
|---|---|
| Windows PowerShell | `py -m venv .venv` then `.\.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `py -m venv .venv` then `.venv\Scripts\activate.bat` |
| macOS / Linux | `python3 -m venv .venv` then `source .venv/bin/activate` |

With the environment active, run `python -m pip install python-dotenv`. Run the lesson's remaining commands **inside `separation_practice/`**. If PowerShell blocks activation, use Windows Command Prompt rather than weakening system-wide security settings. The `.venv/` folder is local and should not be shared.

### Step 1 — Put predictable rules in `stock_alert.py`

Create `stock_alert.py`:

```python
# stock_alert.py

def is_low_stock(stock, threshold):
    """Return True only when stock is below the threshold."""
    return stock < threshold


def make_alert(product_name, stock, threshold):
    """Return a readable message without printing it."""
    if is_low_stock(stock, threshold):
        return f"LOW STOCK: {product_name} has {stock} units left."
    return f"Stock OK: {product_name} has {stock} units."
```

**Why this design?** The function accepts the threshold as a parameter instead of searching for it in a settings file. That means it can work with a threshold of 5, 10, or any other number. The caller chooses the setting.

### Step 2 — Put a setting in `.env`

Create a local file named `.env`:

```dotenv
LOW_STOCK_THRESHOLD=5
```

Create `.env.example` with the same **non-secret sample value**:

```dotenv
LOW_STOCK_THRESHOLD=5
```

The `.env.example` file is a safe template for teammates. The `.env` file is your local copy. Remember that Python **does not read `.env` automatically**.

### Step 3 — Read and validate it in `config.py`

Create `config.py`:

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()


def get_stock_threshold():
    """Read the stock threshold and return it as an integer."""
    raw_value = os.getenv("LOW_STOCK_THRESHOLD", "5")
    try:
        threshold = int(raw_value)
    except ValueError as error:
        raise ValueError("LOW_STOCK_THRESHOLD must be a whole number") from error

    if threshold < 0:
        raise ValueError("LOW_STOCK_THRESHOLD cannot be negative")
    return threshold
```

Let's unpack the new parts:

- `os.getenv("LOW_STOCK_THRESHOLD", "5")` retrieves a text setting. The second value, `"5"`, is a fallback if the setting is missing.
- `int(raw_value)` turns text such as `"5"` into the number `5`.
- `try` and `except` produce a useful error when someone enters something like `five` instead of `5`.
- A negative threshold is rejected because it would not make sense for this exercise.

**Small but important detail:** A pre-existing shell environment variable can take precedence over the same name in `.env` with the default `load_dotenv()` behavior. For this lesson, make sure you have not set another `LOW_STOCK_THRESHOLD` in your terminal if your output seems different.

### Step 4 — Join the pieces in `main.py`

Create `main.py`:

```python
# main.py
from config import get_stock_threshold
from stock_alert import make_alert


def main():
    product_name = "Wireless Mouse"
    stock = 3
    threshold = get_stock_threshold()

    message = make_alert(product_name, stock, threshold)
    print(message)


if __name__ == "__main__":
    main()
```

Read the flow in order: **read the setting → call the business rule → print the result**. No database or AI model is needed.

### Step 5 — Run and verify

Open a terminal in `separation_practice/` and run:

```bash
python main.py
```

**Expected output when `.env` contains `LOW_STOCK_THRESHOLD=5`:**

```text
LOW STOCK: Wireless Mouse has 3 units left.
```

Change the value in `.env` to `2`. Start the program again:

```text
Stock OK: Wireless Mouse has 3 units.
```

**Why?** Three is **not less than** two. You changed configuration, not the logic in `stock_alert.py`. Restore `LOW_STOCK_THRESHOLD=5` afterward.

> Note: Each `python main.py` command starts a fresh Python process. If you run code inside a long-lived Python notebook or interpreter, changing `.env` may require restarting that process to reload settings.

## 4. Where would a database fit?

Your Week 5 product catalog uses SQLite, but this separate low-stock demo does **not** need a database. Here is a **design sketch**, not a file you must implement today:

```text
main.py
   |
   +--> config.py         reads database path / other settings
   |
   +--> database.py       uses sqlite3 to fetch product records
   |
   +--> catalog_logic.py  checks product rules, returns results
   |
   +--> prints result

tests/                      checks key functions independently
```

`database.py` would be the place for connecting to SQLite and issuing SQL statements. It should use **parameterized queries**, as introduced in Week 5, rather than building SQL with pasted input values.

For your **later independent challenge**, you will take your *own* `05_Product_Catalog_App.py` and separate its existing operations into sensible modules. You should retain its create/read/update/delete behavior, not replace it with today's alert demo. You do **not** have to create elaborate classes or implement a new database framework.

## 5. How separation makes testing easier

A test can import the alert function without running `main.py`:

```python
from stock_alert import is_low_stock

assert is_low_stock(3, 5) is True
assert is_low_stock(5, 5) is False
```

`assert` means “check that this condition is true.” If it is not, Python reports a failure. Later, `pytest` will find and run these kinds of checks for us automatically.

The function is easy to test because it takes input values directly and returns an answer directly. A function that calls `input()`, opens SQLite, and sends an API request just to decide whether `3 < 5` would be much harder to test.

For Week 6, **2–3 simple pytest tests** are required in the final takeaway. More extensive database testing, mocking, and LLM integration are **optional/stretch**.

## 6. Guided practice — predict, change, verify

Use `separation_practice/`:

1. **Predict:** With stock `3` and threshold `5`, what message appears? Run and compare.
2. **Change config only:** Set `LOW_STOCK_THRESHOLD=3`. Does stock `3` count as low? Run to confirm.
3. **Change the input only:** Restore threshold `5` and set `stock = 8` in `main.py`. Run to confirm the stock-OK branch.
4. **Try an invalid setting:** Set `LOW_STOCK_THRESHOLD=five` in `.env`, run `python main.py`, and observe the `ValueError` explaining that a whole number is required. Restore `5` afterward.
5. **Explain the boundary:** Identify which file you would edit to (a) change alert wording, (b) change the threshold for one computer, and (c) change the displayed product.

**Self-check:** (2) No; our rule uses `<`, not `<=`. (3) `Stock OK: Wireless Mouse has 8 units.` (5) (a) `stock_alert.py`, (b) `.env`, (c) `main.py`.

### Optional/stretch — think ahead, don't build an LLM integration

Suppose a future AI assistant asks, “Which eComMART products need reordering?” The assistant could use the predictable stock-checking function as an **agent tool**. The tool should return a correct answer without depending on how the LLM phrases the request. We will explain the terminology in `05_Preparing_for_Agentic_AI_Development/00_What_Is_an_Agent_Tool.md`.

**Do not create an Anthropic account or make API calls.** Any API key shown in Week 6 is a placeholder only, and no live AI integration is required for graded work.

## 7. Common mistakes and troubleshooting

| Symptom | Likely reason | What to check |
|---|---|---|
| `ModuleNotFoundError: No module named 'dotenv'` | `python-dotenv` was not installed in the active environment | Activate `.venv`, then run `python -m pip install -r requirements.txt` from the earlier practice project's root |
| `ModuleNotFoundError: No module named 'stock_alert'` | Wrong file name or working folder | Keep `main.py` and `stock_alert.py` together and run from `separation_practice/` |
| Threshold does not change | `.env` is not being loaded, the file is in a different folder, or a shell variable overrides it | Check the exact `.env` filename, current directory, and shell variables |
| `ValueError: ... whole number` | Text like `five` cannot be converted by `int()` | Use `LOW_STOCK_THRESHOLD=5` |
| `.env.example` changes do nothing | It is a template, not the active local settings file | Change `.env` for this practice |
| A test starts the whole app unexpectedly | Main program runs during import | Put startup behind `if __name__ == "__main__":` |

Keep `.env` and `.venv/` out of source control. They are different things: `.env` holds local settings; `.venv/` holds the isolated Python environment.

## 8. Knowledge check

1. What is the difference between **business logic** and **configuration**?
2. Why does `is_low_stock(stock, threshold)` accept a threshold parameter instead of reading `.env` itself?
3. Where would SQL queries belong in a database-backed catalog?
4. Why can an `assert` test the stock rule without launching `main.py`?
5. Which application must you restructure in the Week 6 independent challenge?

**Answers:** (1) Logic decides what the program does; configuration supplies settings that can vary. (2) The function stays reusable and easy to test. (3) A database-access module such as `database.py`. (4) It imports a predictable function and checks its returned value. (5) Your own Week 5 eComMART product catalog.

## Lesson recap

- Keep the startup flow, business rules, settings, database access, and tests in clear places.
- Small, predictable functions are easier to understand and verify.
- The separate low-stock notifier is the **instructor demo**; your Week 5 catalog remains intact for the required independent challenge.
- The required Week 6 bar stays small: `.venv`, `requirements.txt`, **one** environment variable, and **2–3** simple pytest tests. AI SDK integration and advanced testing are optional.

**Next lesson:** `../02_Testing_Fundamentals/01_Why_Automated_Testing_Matters.md` explains why we automate these checks instead of relying only on manual runs.
