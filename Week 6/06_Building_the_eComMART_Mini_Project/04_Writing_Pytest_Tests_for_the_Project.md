# Instructor Demo — Writing Pytest Tests for the Project

## Lesson purpose

The eComMART warehouse team can now run a small low-stock notifier from `main.py`. It reads its stock threshold from `.env`, checks four sample products, and prints messages. But what happens if somebody changes the meaning of “low stock” by mistake? A message may look plausible while being wrong.

In this final Instructor Demo lesson, we will write **three small automated tests**. Instead of checking the output by eye after every code change, we can ask pytest to check important rules for us in seconds.

**Continuity reminder:** We are testing the **new, standalone `ecommart_notify` demo**, not refactoring or changing your Week 5 `05_Product_Catalog_App.py`. The separate independent challenge will bring these skills back to your existing catalog.

**Core:** write and run 2–3 pytest tests for deterministic Python functions and a configuration error. **Optional/stretch only:** extra tests, mocking, and the Anthropic SDK wrapper. No Anthropic signup, real key, payment, or live LLM API call is required.

## Learning objectives

By the end, you should be able to:

- Explain what a test checks and why a passing test is useful but not proof that all bugs are gone.
- Create a `tests/` directory and Python files whose names begin with `test_`.
- Recognize the **Arrange → Act → Assert** pattern in a test.
- Run `python -m pytest -v` from the project root and interpret **PASSED** and **FAILED**.
- Test a normal case, an important boundary, and an invalid configuration value.
- Correct a deliberately introduced bug and rerun the same tests.

## 1. What are we protecting?

The warehouse rule from the previous lesson is **strictly below the threshold**:

| Quantity | Threshold | Correct result | Why |
|---:|---:|---|---|
| 4 | 10 | Low stock | 4 is less than 10 |
| 10 | 10 | Not low | Equality is **not** below |
| 11 | 10 | Not low | 11 is greater than 10 |

A second rule is that `LOW_STOCK_THRESHOLD` must be a **whole number that is not negative**. A value like `ten` should produce a useful `ValueError`, not an arbitrary stock result.

**Instructor prediction:** Ask, “If someone changes `<` to `<=`, which row would expose the mistake?” The answer is the **equality** row.

## 2. Confirm your starting files

Open the **same `ecommart_notify/` folder** used in the previous three Instructor Demo lessons. Your application should have:

```text
ecommart_notify/
├── .venv/                 # local environment; do not share
├── .env                   # local setting; do not share
├── .env.example           # safe example
├── requirements.txt       # pytest and python-dotenv
├── main.py                # runs the notifier
├── config.py              # get_low_stock_threshold()
└── stock_alert.py         # is_low_stock(), format_stock_message()
```

The existing `stock_alert.py` has:

```python
def is_low_stock(quantity, threshold):
    return quantity < threshold


def format_stock_message(product_name, quantity, threshold):
    if is_low_stock(quantity, threshold):
        return (
            f"LOW STOCK: {product_name} has {quantity} units "
            f"(threshold: {threshold})."
        )
    return f"OK: {product_name} has {quantity} units."
```

Your existing `config.py` reads `LOW_STOCK_THRESHOLD` with `os.getenv`, converts it with `int(...)`, and raises `ValueError` for text or negative values. **Do not replace working application code with the snippets above**—the snippets are a quick reference to the earlier lesson.

Activate your demo virtual environment (or use the `.venv` interpreter directly):

| Terminal | Command from `ecommart_notify/` |
|---|---|
| Windows PowerShell | `.\.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `.venv\Scripts\activate.bat` |
| macOS/Linux bash or zsh | `source .venv/bin/activate` |

Check your project dependencies:

```bash
python -m pip install -r requirements.txt
python -m pytest --version
```

The earlier lesson's core `requirements.txt` pins `pytest==9.2.0` and `python-dotenv==1.2.4`. The version display should report pytest **9.2.0** when those requirements were installed successfully. You do **not** need the Anthropic package for these tests.

## 3. Step 1 — Create the test folder

In the root of `ecommart_notify/`, create a folder named `tests`. Inside it, create two new files:

```text
ecommart_notify/
├── ...existing project files...
└── tests/
    ├── test_stock_alert.py
    └── test_config.py
```

Why those names? By default, pytest finds files named `test_*.py` or `*_test.py` and runs functions whose names start with `test_`. An ordinary `.py` file does not become a test merely because it is inside `tests/`.

**Important:** Run pytest from the **project root**, the folder containing `stock_alert.py` and `config.py`. We use `python -m pytest`, which helps Python find these sibling modules without custom import-path settings.

## 4. Step 2 — Test the business rule

Type this complete code into `tests/test_stock_alert.py`:

```python
# tests/test_stock_alert.py
from stock_alert import is_low_stock, format_stock_message


def test_quantity_below_threshold_is_low():
    # Arrange: choose a product quantity and a threshold.
    quantity = 4
    threshold = 10

    # Act: run the function we want to check.
    result = is_low_stock(quantity, threshold)

    # Assert: compare the actual result with our expected rule.
    assert result is True


def test_quantity_equal_to_threshold_is_not_low():
    # Arrange
    quantity = 10
    threshold = 10

    # Act
    result = is_low_stock(quantity, threshold)

    # Assert: equality is an important boundary.
    assert result is False
```

### Read Arrange → Act → Assert

| Part | Question it answers | Example |
|---|---|---|
| **Arrange** | What values and setup do we need? | `quantity = 4`, `threshold = 10` |
| **Act** | Which function are we checking? | `is_low_stock(4, 10)` |
| **Assert** | What result should be true? | `assert result is True` |

`assert` is a Python statement that checks whether a condition is true. If it is false, pytest marks the test as **FAILED** and shows where the expectation did not match reality.

**Optional extra check (not part of the required three tests):** use the already-imported `format_stock_message` to verify exact text. For example, `assert format_stock_message("Scanner", 4, 10) == "LOW STOCK: Scanner has 4 units (threshold: 10)."`.

## 5. Step 3 — Test an error scenario without changing `.env`

In `tests/test_config.py`, type:

```python
# tests/test_config.py
import pytest
from config import get_low_stock_threshold


def test_invalid_threshold_text_raises_error(monkeypatch):
    # Arrange: temporarily set an invalid environment variable.
    monkeypatch.setenv("LOW_STOCK_THRESHOLD", "ten")

    # Act + Assert: this function should reject the value.
    with pytest.raises(ValueError, match="whole number"):
        get_low_stock_threshold()
```

New ideas, explained:

- **`pytest.raises(ValueError)`** says that raising this type of error is the *correct* outcome for this input.
- **`match="whole number"`** also checks that the error message includes the words `whole number`.
- **`monkeypatch`** is a built-in pytest helper (**fixture**). Pytest provides it automatically when you put `monkeypatch` in the test function's parameters.
- **`monkeypatch.setenv(...)`** sets the variable temporarily for this test. Pytest restores the original environment afterward. It does **not** edit your `.env` file.
- Your `config.py` calls `load_dotenv()` without `override=True`, so an environment variable set by `monkeypatch` takes precedence over `.env` while the test runs.

This short use of `monkeypatch` is **included in the instructor demonstration** so learners can see a safe configuration-error test. **Writing mocking/monkeypatch code independently is optional**, not required for the Week 6 takeaway; students may instead write 2–3 ordinary function tests in their own catalog.

**Instructor explanation:** The function is supposed to *reject* an invalid value. For an error test, “success” means the *expected error happened*.

## 6. Step 4 — Run all three tests

From `ecommart_notify/`, run:

```bash
python -m pytest -v
```

You should see entries similar to:

```text
tests/test_stock_alert.py::test_quantity_below_threshold_is_low PASSED
tests/test_stock_alert.py::test_quantity_equal_to_threshold_is_not_low PASSED
tests/test_config.py::test_invalid_threshold_text_raises_error PASSED
============================== 3 passed in ... ==============================
```

The order, timing, operating-system details, and other pytest lines can differ. **Three passed** is the important result. If an unrelated test file is already in the folder, pytest may report more tests; look for these three named tests specifically.

Run just the stock tests:

```bash
python -m pytest -v tests/test_stock_alert.py
```

Expected: **2 passed**.

Run just the configuration test:

```bash
python -m pytest -v tests/test_config.py
```

Expected: **1 passed**.

## 7. Step 5 — Make a test fail on purpose, then repair it

This step shows why testing is useful. Keep the test files unchanged.

1. Open `stock_alert.py`.
2. Temporarily change the stock comparison from `quantity < threshold` to `quantity <= threshold`.
3. Save the file.
4. Run `python -m pytest -v` again.
5. Find the failure: `test_quantity_equal_to_threshold_is_not_low` expected `False` but received `True`.
6. **Restore** `quantity < threshold` and save.
7. Run `python -m pytest -v` a final time. Confirm **3 passed**.

A failing test is not a wasted test. It tells us a known business rule was broken. Do not “fix” the failure by changing the test expectation to the wrong rule.

**Instructor interaction:** Before step 4, ask learners which test will fail and why. This creates a brief predict → observe → explain cycle.

## 8. Run the application separately

Tests do **not** replace the application. After restoring the rule, confirm the notifier still runs:

```bash
python main.py
```

With `.env` set to `LOW_STOCK_THRESHOLD=10`, expected:

```text
=== eComMART Low-Stock Notifier ===
LOW STOCK: Wireless Barcode Scanner has 4 units (threshold: 10).
OK: Thermal Label Roll has 120 units.
LOW STOCK: USB-C Docking Station has 8 units (threshold: 10).
OK: Shipping Label Printer has 10 units.
```

Notice the difference: `python main.py` **runs the application** and prints product messages; `python -m pytest -v` **checks expectations** and prints test results.

## 9. Finished Instructor Demo structure

```text
ecommart_notify/
├── .venv/                         # created locally; never distribute
├── .env                           # local only; threshold and fake key placeholder
├── .env.example                   # shareable template
├── requirements.txt               # pytest and python-dotenv
├── main.py                        # runs stock checks
├── config.py                      # loads/validates threshold
├── stock_alert.py                 # deterministic rule and messages
└── tests/
    ├── test_stock_alert.py        # two rule tests
    └── test_config.py             # one error test
```

The course reference in `Examples/ecommart_notify/` also includes `anthropic_client.py`: **optional/stretch only**. No test or run command above imports or calls it. **Do not add an actual Anthropic API request to `main.py`** for Week 6.

## 10. Troubleshooting

| Symptom | Likely cause | What to do |
|---|---|---|
| `No module named pytest` | Installed outside the project environment | Activate `.venv`; run `python -m pip install -r requirements.txt` |
| `No module named stock_alert` | Started pytest from the wrong folder or filename differs | From `ecommart_notify/`, run `python -m pytest -v`; check `stock_alert.py` spelling |
| `collected 0 items` | File/function names do not start with `test_` | Rename to `test_stock_alert.py` and `def test_...()` |
| Equality test fails | Rule is `<=` instead of `<` | Restore the strict-below comparison |
| Error test fails | `config.py` is different from the previous lesson | Confirm it converts with `int()`, raises `ValueError`, and calls `load_dotenv()` without overriding existing variables |
| `fixture 'monkeypatch' not found` | Test was not launched through pytest or test signature changed | Use `python -m pytest -v`; keep `monkeypatch` as a function parameter |
| Test unexpectedly contacts a network | Additional API code was connected | Remove network calls from required code; test deterministic functions locally |
| Wrong output after the deliberate bug | Original comparison was not restored | Save `quantity < threshold` and rerun tests/application |

## 11. Guided review — explain the test, not just the syntax

1. Why is **exactly 10** an important test quantity when the threshold is 10?
2. Which line in each test is the **Assert** step?
3. Why is an invalid text value like `ten` a useful error scenario?
4. Why did we test `is_low_stock()` directly rather than requiring an LLM to run?
5. What is the difference between `python main.py` and `python -m pytest -v`?

**Expected understanding:** We isolate the business rule so we can verify it quickly, test the critical boundary, and catch bad configuration before a warehouse team relies on incorrect alert messages.

## 12. Completion checklist and next step

- [ ] I created `tests/test_stock_alert.py` and `tests/test_config.py`.
- [ ] I understand Arrange → Act → Assert.
- [ ] I ran the three demo tests and saw **3 passed**.
- [ ] I intentionally broke the strict-below rule and saw the boundary test fail.
- [ ] I restored the rule and confirmed the application still runs.
- [ ] I kept the Week 5 catalog separate from the Instructor Demo.
- [ ] I needed no real API key, signup, payment, or live LLM API call.

**What comes next:** `07_Practice_and_Review/` begins with small guided practice tasks. Its **required Independent Challenge** will ask you to take **your own Week 5 `05_Product_Catalog_App.py`** and add a virtual environment, `requirements.txt`, a local `.env`, sensible module separation, and **2–3 simple pytest tests** while preserving the catalog's behavior.
