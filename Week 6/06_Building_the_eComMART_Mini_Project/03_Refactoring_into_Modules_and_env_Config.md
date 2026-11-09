# Instructor Demo — Refactoring into Modules and .env Configuration

## Lesson purpose

Our new eComMART low-stock notifier now has its own `.venv` and `requirements.txt`. It is ready for Python code, but we do not want every responsibility crammed into one file. A second developer should be able to tell **where to change the alert rule**, **where to change a setting**, and **which file starts the program**.

In this demo, the instructor builds the small notifier using separate Python modules. We will also move the stock threshold out of Python source code and into a local `.env` setting.

**Continuity reminder:** Despite the word *refactoring* in this lesson's filename, we are organizing the **new Instructor Demo app**. Students will restructure **their own Week 5 product catalog** in the separate required independent challenge. Do not replace or edit `05_Product_Catalog_App.py` during this demo.

**Core:** split the program into simple modules, configure one environment variable, and run a deterministic stock check. **Optional/stretch only:** `anthropic_client.py` illustrates a future LLM integration point; it is **not imported or executed by `main.py`**. No real Anthropic API key, account, signup, payment, or live API request is required.

## Learning objectives

By the end of the instructor walkthrough, you should be able to:

- Describe why the alert rule, configuration, and entry point belong in different files.
- Explain what `from module import function` means.
- Write and run a small pure function that checks a stock threshold.
- Create `.env.example` and a local `.env` with `LOW_STOCK_THRESHOLD=10`.
- Read and validate the threshold in `config.py` without hardcoding it in `main.py`.
- Run the notifier, predict its output, and change behavior by editing `.env` only.
- Identify how the separate modules make automated tests easier in the next lesson.

## 1. The eComMART business rule

The warehouse manager wants an alert only when a product's available units are **strictly less** than the reorder threshold.

| Product | Units on hand | Threshold | Expected |
|---|---:|---:|---|
| Wireless Barcode Scanner | 4 | 10 | Low stock |
| Thermal Label Roll | 120 | 10 | OK |
| USB-C Docking Station | 8 | 10 | Low stock |
| Shipping Label Printer | 10 | 10 | OK — equal is **not** low |

The exact rule is `quantity < threshold`, **not** `quantity <= threshold`. This equality boundary will matter when we write tests.

### Why separate files?

| File | Its single main job | Does **not** do |
|---|---|---|
| `stock_alert.py` | Decide low/not-low and format a message | Read `.env`, make network requests, or open SQLite |
| `config.py` | Load and validate a stock threshold | Decide which products are low |
| `main.py` | Provide sample products, call helpers, print results | Contain a hardcoded threshold or a second copy of the alert rule |
| `.env` | Hold your local threshold value | Contain Python code; be distributed to classmates |
| `.env.example` | Show safe example settings to copy | Store real secrets |
| `tests/` | Hold tests (added in the **next** lesson) | Run automatically when `main.py` is launched |

A **module** is just a Python file that other Python files can import. An **entry point** is the Python file that starts the application when you run it.

## 2. Confirm the starting project

Open the **same `ecommart_notify/` folder** used in `02_Setting_Up_venv_and_requirements_txt.md`. Your terminal must be in the folder containing `requirements.txt`.

You should already have:

```text
ecommart_notify/
├── .venv/                 # created locally
└── requirements.txt       # pytest and python-dotenv
```

Activate `.venv` if it is not active:

| Terminal | Command from ecommart_notify/ |
|---|---|
| Windows PowerShell | `.\.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `.venv\Scripts\activate.bat` |
| macOS/Linux | `source .venv/bin/activate` |

Use `python -m pip install -r requirements.txt` if the dependencies have not yet been installed. All following `python` commands must use the demo virtual environment. The previous lesson explains how to use the `.venv` Python executable directly if activation is blocked.

## 3. Step 1 — Create stock_alert.py (business logic)

In the root of `ecommart_notify/`, create `stock_alert.py` and type **all** of the code below:

```python
# stock_alert.py

def is_low_stock(quantity, threshold):
    """Return True only when available units are below the threshold."""
    return quantity < threshold


def format_stock_message(product_name, quantity, threshold):
    """Create a predictable message that another function can display."""
    if is_low_stock(quantity, threshold):
        return (
            f"LOW STOCK: {product_name} has {quantity} units "
            f"(threshold: {threshold})."
        )
    return f"OK: {product_name} has {quantity} units."
```

**Read the code in plain language:**

- `def` creates a function. Inputs inside the parentheses are its **parameters**.
- `is_low_stock` answers one yes/no question. In Python, a yes/no result is a **Boolean** (`True` or `False`).
- `format_stock_message` calls the first function and **returns** text; it does not print it itself.
- The `f"..."` syntax builds a string using values from variables.
- Neither function reads a file, queries a database, or contacts an LLM. This predictable behavior is called **deterministic**: the same inputs produce the same result.

### Quick manual check

From the `ecommart_notify` terminal, run:

```bash
python -c "from stock_alert import is_low_stock; print(is_low_stock(4, 10)); print(is_low_stock(10, 10))"
```

Expected:

```text
True
False
```

**Instructor prediction prompt:** Ask learners which part of `quantity < threshold` would be incorrect if the business requested an alert **at or below** a threshold. Explain that our actual requirement is **below only**, so we are not changing it.

## 4. Step 2 — Create the safe settings template

Create `.env.example` in the same folder, containing:

```dotenv
# Safe example for the Week 6 local stock notifier
LOW_STOCK_THRESHOLD=10
# OPTIONAL/STRETCH ONLY: nonworking placeholder; no API call is required
ANTHROPIC_API_KEY=YOUR_PLACEHOLDER_KEY_HERE
```

Now create your own local file named `.env` and copy the same lines into it. The `.env` file is a **plain text configuration file**, not Python code. Keep the uppercase spelling exactly: `LOW_STOCK_THRESHOLD`.

- `.env.example` is a **safe template** that may be distributed.
- `.env` is the **local copy** on your computer; do not distribute or commit it.
- The Anthropic key is a **fake placeholder only** and is **not used** in this lesson or any required Week 6 work. Do **not** replace it with a real key.

**Why do we use an environment variable?** A threshold may be `10` in one environment and `5` in another. We want to change a setting without editing `stock_alert.py` or `main.py`.

## 5. Step 3 — Create config.py (configuration logic)

Create `config.py` with the complete code below:

```python
# config.py
import os
from dotenv import load_dotenv


def get_low_stock_threshold():
    """Read LOW_STOCK_THRESHOLD and return a validated integer."""
    load_dotenv()
    raw_value = os.getenv("LOW_STOCK_THRESHOLD", "10")

    try:
        threshold = int(raw_value)
    except ValueError as error:
        raise ValueError(
            "LOW_STOCK_THRESHOLD must be a whole number."
        ) from error

    if threshold < 0:
        raise ValueError("LOW_STOCK_THRESHOLD cannot be negative.")

    return threshold
```

Here is what each new piece does:

| Code | Meaning |
|---|---|
| `import os` | Uses Python's built-in tool for reading environment variables |
| `from dotenv import load_dotenv` | Imports a helper from the **python-dotenv** package installed in the previous demo |
| `load_dotenv()` | Loads values from local `.env` into the program's environment if not already set |
| `os.getenv("LOW_STOCK_THRESHOLD", "10")` | Reads the value, using a default of `"10"` if none was set |
| `int(raw_value)` | Converts text such as `"10"` to the number `10` |
| `try` / `except ValueError` | Produces a helpful error if someone writes a nonnumeric value |
| `threshold < 0` | Rejects a negative threshold |

**Important detail:** `os.getenv()` gives back text, even when `.env` contains digits. We must convert it before comparing it to stock quantities. The default value is for a missing setting; it does not silently accept a setting that is present but invalid.

**Safe handling:** There are no credentials in this core logic. Do not print API keys or use them in error messages. The fake `ANTHROPIC_API_KEY` line exists only to illustrate a future optional setting.

### Verify configuration before writing main.py

Run:

```bash
python -c "from config import get_low_stock_threshold; print(get_low_stock_threshold())"
```

Expected with `LOW_STOCK_THRESHOLD=10`:

```text
10
```

If you see `ModuleNotFoundError: No module named 'dotenv'`, activate your demo environment and run `python -m pip install -r requirements.txt`. If you see a different threshold, check whether the variable was **already set** in your terminal: existing operating-system environment variables take precedence over values in `.env` by default.

## 6. Step 4 — Create main.py (entry point)

Create `main.py`:

```python
# main.py
from config import get_low_stock_threshold
from stock_alert import format_stock_message


def main():
    threshold = get_low_stock_threshold()

    # Fresh, in-memory demo data; this is NOT the Week 5 SQLite catalog.
    products = [
        ("Wireless Barcode Scanner", 4),
        ("Thermal Label Roll", 120),
        ("USB-C Docking Station", 8),
        ("Shipping Label Printer", 10),
    ]

    print("=== eComMART Low-Stock Notifier ===")
    for product_name, quantity in products:
        message = format_stock_message(product_name, quantity, threshold)
        print(message)


if __name__ == "__main__":
    main()
```

**Let's trace the program:**

1. `main.py` imports the two helpers it needs.
2. `get_low_stock_threshold()` reads the local setting (normally `10`).
3. `products` holds four small sample product records. These are tuples: each pair has a name and a quantity.
4. The `for` loop visits the products one at a time.
5. `format_stock_message()` returns the message for one product.
6. `print()` displays that message in the terminal.
7. The final `if __name__ == "__main__"` line means `main()` runs when we launch `main.py` directly.

Notice that `main.py` **does not** contain the comparison `quantity < threshold`, **does not** call `os.getenv`, and **does not** import Anthropic. Those jobs belong elsewhere (or, for Anthropic, are **optional and unused**).

## 7. Step 5 — Run the complete local notifier

Make sure `.env` contains `LOW_STOCK_THRESHOLD=10`. From the root of `ecommart_notify/`, run:

```bash
python main.py
```

Expected output:

```text
=== eComMART Low-Stock Notifier ===
LOW STOCK: Wireless Barcode Scanner has 4 units (threshold: 10).
OK: Thermal Label Roll has 120 units.
LOW STOCK: USB-C Docking Station has 8 units (threshold: 10).
OK: Shipping Label Printer has 10 units.
```

### Try one configuration change

Edit only this line in `.env`:

```dotenv
LOW_STOCK_THRESHOLD=5
```

Save the file and run `python main.py` again in a **new Python process** (the ordinary terminal command starts one). Now the USB-C Docking Station with 8 units should show **OK**, while the Wireless Barcode Scanner with 4 units should still show **LOW STOCK**.

Return the setting to `10` after the experiment, so the next lesson's examples start from the expected demo configuration.

**Instructor interaction:** Before running with threshold `5`, ask learners: “Which products will change status?” Wait for predictions, then run the program and compare answers.

## 8. Finished project layout (before tests)

Your local folder should now resemble:

```text
ecommart_notify/
├── .venv/                     # local only
├── .env                       # local only, not shared
├── .env.example               # shareable settings template
├── requirements.txt           # core dependencies
├── main.py                    # starts program and prints results
├── config.py                  # reads and validates threshold
└── stock_alert.py             # deterministic rule and messages
```

The complete **reference example** later also contains `anthropic_client.py` (**optional/stretch only**) and a `tests/` directory. We will create the tests in `04_Writing_Pytest_Tests_for_the_Project.md`. No database integration is needed for this fresh instructor demo.

## 9. Why this separation helps with testing

Suppose the instructor accidentally edits the rule in `stock_alert.py` from `<` to `<=`. With a threshold of `10`, the shipping printer at exactly `10` units would incorrectly trigger an alert.

Because `is_low_stock()` accepts ordinary values and returns a simple Boolean, a pytest test can catch this without starting `main.py`, reading `.env`, opening SQLite, or contacting an LLM. A second test can check that invalid threshold settings produce an understandable error.

In the next lesson, we will write **2–3 basic tests** around these behaviors. Additional tests, mocking, and any Anthropic SDK work are **optional/stretch**, not part of the required bar.

## 10. Troubleshooting

| Symptom | What to check | Fix |
|---|---|---|
| `No module named dotenv` | Is the correct `.venv` active? | Run `python -m pip install -r requirements.txt` through that environment |
| `No module named stock_alert` or `config` | Are files beside `main.py`? Is the terminal in the project root? | Correct the filename and run `python main.py` from `ecommart_notify/` |
| Wrong threshold displayed | Is an OS-level `LOW_STOCK_THRESHOLD` already set? | Remove or change that override in the current terminal, then rerun; `load_dotenv()` does not override an existing environment value by default |
| `LOW_STOCK_THRESHOLD must be a whole number` | `.env` contains a value such as `ten` or `10.5` | Use whole-number digits such as `10` |
| `LOW_STOCK_THRESHOLD cannot be negative` | `.env` contains `-1` | Set a value of `0` or greater |
| Product at exactly threshold shows LOW STOCK | Comparison was mistakenly changed | Restore `quantity < threshold` in `stock_alert.py` |
| `.env` looks like `.env.txt` | Editor or OS added `.txt` | Rename it exactly `.env`; ensure file extensions are visible |
| Program unexpectedly tries Anthropic | Extra optional code was added to `main.py` | Remove that import/call; the core entry point must work entirely locally |

## 11. Guided practice — predict, edit, verify

1. In one sentence, explain why `stock_alert.py` does **not** read `.env` itself.
2. With threshold `10`, predict the status of a product with `9`, `10`, and `11` units.
3. Change `.env` to threshold `5` and predict the printed results before running.
4. Restore `10` and deliberately enter `ten`; run `python main.py` and read the error. Restore `10` again.
5. Point to the line that starts the program and the function that owns the stock comparison.

**Expected understanding:** `stock_alert.py` handles predictable business logic, `config.py` handles configuration, and `main.py` coordinates them. Values below `10` are low; equal/above are not. `ten` is invalid because the program expects a whole number.

## 12. Completion checklist and next step

- [ ] `stock_alert.py` contains the deterministic stock rule and message formatting.
- [ ] `.env.example` safely shows a local stock threshold and a **fake** Anthropic placeholder.
- [ ] Local `.env` exists and is not distributed or committed.
- [ ] `config.py` reads and validates `LOW_STOCK_THRESHOLD`.
- [ ] `main.py` displays the four expected results with threshold `10`.
- [ ] Changing `.env` changes the output without editing the business rule.
- [ ] My Week 5 catalog application remains untouched.
- [ ] No Anthropic signup, real key, payment, or live API call was needed.

Next: `04_Writing_Pytest_Tests_for_the_Project.md` will add local pytest tests for below-threshold, equality boundary, and configuration errors. The separate Takeaway Hands-on Exercise will then use these ideas to restructure **your own Week 5 EcomMART catalog**.
