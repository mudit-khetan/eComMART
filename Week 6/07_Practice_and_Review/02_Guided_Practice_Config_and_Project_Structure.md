# Guided Practice — Configuration and Project Structure

**Week 6 · Practice and Review · Guided Practice 2**

## Practice purpose

In the previous guided practice, you prepared an isolated Python environment for eComMART. Now you will make a tiny stock-checking program easier to maintain: put the stock rule in one module, read a configurable threshold from `.env`, and keep the program entry point in another module.

Imagine two eComMART warehouses use the same Python code but want different low-stock thresholds. Changing the code every time would be error-prone. Configuration lets them change a setting without changing the rule.

**Core:** one environment variable, `.env.example`, module separation, and a working local program. **Optional/stretch:** extra validation and additional tests. No Anthropic SDK, API key, account, paid service, or live AI call is required. The Instructor Demo remains separate from your Week 5 catalog; you will reorganize your own catalog in the next challenge.

## Learning objectives

By the end, you should be able to:

- Explain what belongs in `main.py`, `stock_alert.py`, and `config.py`.
- Create `.env` and `.env.example` safely and describe the difference.
- Use `load_dotenv()` and `os.getenv()` to read a threshold.
- Use `from stock_alert import ...` to share a function across files.
- Run the program, predict its output, change the configuration, and diagnose a common error.
- Explain which files should be shared with a teammate and which should remain local.

## 1. What you are building

Build this small **practice project**, separate from both the `ecommart_notify/` Instructor Demo and `05_Product_Catalog_App.py`:

```text
ecommart_config_practice/
├── .venv/                 # local only; created by Python
├── .env                   # local only; create from .env.example
├── .env.example           # safe template to share
├── .gitignore
├── requirements.txt
├── config.py              # read the threshold
├── stock_alert.py         # decide whether stock is low
└── main.py                # run a few example checks
```

**Application flow:** `main.py` → reads threshold using `config.py` → calls `stock_alert.py` → prints results. The arrow means “uses the code in,” not “moves a file.”

## 2. Before you start

You need Python 3.10 or newer, a terminal, and an editor such as VS Code. You should have completed `01_Guided_Practice_venv_and_Dependencies.md`. If you have not, review how to activate `.venv` and install packages first.

Create `ecommart_config_practice/` and open it as the current folder in your editor. Check your terminal location with `pwd` (macOS/Linux), `Get-Location` (PowerShell), or `cd` (Command Prompt). The path should end with `ecommart_config_practice`.

## 3. Task 1 — Create an isolated environment

From the practice folder:

| Terminal | Create | Activate |
|---|---|---|
| Windows PowerShell | `py -m venv .venv` | `.\.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `py -m venv .venv` | `.venv\Scripts\activate.bat` |
| macOS/Linux | `python3 -m venv .venv` | `source .venv/bin/activate` |

If activation is blocked, you can use `.venv\Scripts\python.exe` (Windows) or `.venv/bin/python` (macOS/Linux) in place of `python` in commands below.

Create `requirements.txt`:

```text
python-dotenv==1.2.4
pytest==9.2.0
```

Install from this file, **with the environment selected**:

```bash
python -m pip install -r requirements.txt
python -m pip show python-dotenv
```

**Expected:** the second command displays information about `python-dotenv` installed in your `.venv`. An internet connection may be needed to download the packages from your approved package source; no AI service is involved.

**Checkpoint 1:** In your terminal, run `python -c "import sys; print(sys.executable)"`. It should point inside this practice `.venv`.

## 4. Task 2 — Add safe configuration files

Create `.env.example`:

```dotenv
# eComMART practice configuration — safe to share
LOW_STOCK_THRESHOLD=10
```

Copy that content to a second file named `.env`. Both files are plain text. The uppercase name `LOW_STOCK_THRESHOLD` must match the Python code exactly. Here, `10` is a **placeholder business setting** you may change—not an API key.

Create `.gitignore`:

```gitignore
.venv/
.env
__pycache__/
.pytest_cache/
```

`.gitignore` tells Git which local files not to add to version control. It does not delete them or protect files you have already shared. **Never place real passwords or API keys in a distributed `.env.example`.** There is no need to create any key in this practice.

**Checkpoint 2:** Explain why `.env.example` is appropriate to share, but `.env` should remain local.

## 5. Task 3 — Put the stock rule in stock_alert.py

Create `stock_alert.py`:

```python
def is_low_stock(quantity, threshold):
    """Return True when stock is strictly below the threshold."""
    return quantity < threshold


def format_stock_message(name, quantity, threshold):
    """Build a predictable message, without printing it."""
    if is_low_stock(quantity, threshold):
        return f"LOW STOCK: {name} has {quantity} units (threshold: {threshold})."
    return f"OK: {name} has {quantity} units."
```

**Why?** This file contains a business rule, not configuration or user input. The same inputs always give the same output, which makes it easy to test later.

Predict the results: `is_low_stock(4, 10)` is `True`; `is_low_stock(10, 10)` is `False`. **Equal to the threshold is not low stock.**

## 6. Task 4 — Read configuration in config.py

Create `config.py`:

```python
import os
from dotenv import load_dotenv


def get_low_stock_threshold():
    """Return LOW_STOCK_THRESHOLD as a nonnegative whole number."""
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

- `load_dotenv()` loads the local `.env` file when the program starts.
- `os.getenv()` reads a named environment variable; the fallback `"10"` applies if the variable is missing.
- Values from environment variables are **text**. `int(...)` turns that text into a number.
- `raise ValueError(...)` stops the program with a clear explanation when the value is invalid.

**Important:** If `LOW_STOCK_THRESHOLD` is already defined in the terminal, `load_dotenv()` normally does not replace it with the value from `.env`. If a change to `.env` appears to be ignored, check for a preexisting terminal setting or open a fresh terminal and activate `.venv` again.

**Checkpoint 3:** Without running the program, predict the result of `LOW_STOCK_THRESHOLD=banana` and explain why the conversion fails.

## 7. Task 5 — Tie the modules together in main.py

Create `main.py`:

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

The `import` lines let `main.py` use functions defined in other files. The `main()` function **coordinates** the work; it does not duplicate the stock-comparison rule or read `.env` itself.

From the folder containing `main.py`, run:

```bash
python main.py
```

**Expected output with `.env` set to `LOW_STOCK_THRESHOLD=10`:**

```text
LOW STOCK: Wireless Barcode Scanner has 4 units (threshold: 10).
OK: Thermal Label Roll has 120 units.
OK: USB-C Docking Station has 10 units.
```

**Checkpoint 4:** Change only `.env` to `LOW_STOCK_THRESHOLD=12`; run `python main.py` again in a clean terminal without a conflicting environment variable. The Docking Station should now trigger an alert, because `10 < 12`. You did not need to edit the business logic.

## 8. Guided mini-challenge — catch an invalid setting

Change `.env` temporarily to:

```dotenv
LOW_STOCK_THRESHOLD=banana
```

Run `python main.py`. **Expected:** the application reports a `ValueError` explaining that the threshold must be a whole number; it should **not** silently use `10`. Restore `LOW_STOCK_THRESHOLD=10` afterward.

**Think before checking:** Which file should you change if the rule becomes “alert at or below the threshold”? Which file should you change if a warehouse simply wants to use threshold `20`? Suggested answer: change the comparison in `stock_alert.py` for a different business rule; change `.env` for a different setting.

### Optional/stretch — one tiny test

Only if you have time, create `tests/test_stock_alert.py` and run `python -m pytest -q`:

```python
from stock_alert import is_low_stock


def test_equal_threshold_is_not_low():
    # Arrange
    quantity, threshold = 10, 10
    # Act
    result = is_low_stock(quantity, threshold)
    # Assert
    assert result is False
```

This extra test is **not required for this guided practice**; the required 2–3 tests belong to the independent Week 5 catalog challenge.

## 9. Troubleshooting

| Problem | Likely cause | What to check |
|---|---|---|
| `No module named 'dotenv'` | Installed packages in another Python | Activate this `.venv`; rerun `python -m pip install -r requirements.txt` |
| `No module named 'stock_alert'` | File is misspelled or terminal is in another folder | Confirm `main.py` and `stock_alert.py` are side by side |
| Threshold change has no effect | Existing shell variable overrides `.env` | Check the terminal environment, or restart in a clean terminal |
| `ValueError` on threshold | `.env` contains a nonnumeric or negative value | Put a whole number `0` or greater in `.env` |
| `.env` is missing | You only created `.env.example` | Make a separate `.env` from the template |
| `.env` appears in source control | `.gitignore` is missing or the file was already tracked | Add `.env` to `.gitignore`; ask the instructor about removing previously tracked secrets |

## 10. Knowledge check

1. What is the difference between an environment variable and a Python variable?
2. Why does the program convert `"10"` using `int()`?
3. Why should `stock_alert.py` avoid reading `.env` directly?
4. What happens when stock is exactly equal to the threshold?
5. Which files could a teammate receive safely: `.env`, `.env.example`, `requirements.txt`, `.venv/`?

## 11. Completion checklist

- [ ] I created `ecommart_config_practice/` without modifying the Week 5 catalog.
- [ ] I created and used its `.venv`.
- [ ] I installed its `requirements.txt` dependencies.
- [ ] I created `.env`, `.env.example`, and `.gitignore`.
- [ ] I placed application logic, configuration, and the entry point in separate files.
- [ ] `python main.py` produced the three expected messages.
- [ ] I changed the threshold through `.env` without editing Python code.
- [ ] I tried and corrected one invalid setting.
- [ ] I did not use or need a real API key or live LLM call.

**Next:** `03_Independent_Challenge_Restructure_Your_Week5_Catalog.md` applies the same ideas to **your own existing Week 5 product catalog**. That is the required Week 6 takeaway.
