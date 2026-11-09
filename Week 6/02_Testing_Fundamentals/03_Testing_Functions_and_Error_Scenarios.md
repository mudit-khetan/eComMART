# Testing Functions and Error Scenarios

## Lesson purpose

You have now used pytest to check three normal eComMART stock situations. Real programs must also behave sensibly when a value is on a boundary or when an input is invalid. If the stock threshold is configured as `five` instead of `5`, the application should explain the mistake rather than silently use a wrong value.

In this lesson, you will learn to test **successful results, boundaries, and errors**. We will reuse the small `separation_practice` project, especially its existing `stock_alert.py` and `config.py`. This keeps the exercise manageable for a beginner and avoids changing your Week 5 catalog before the required independent challenge.

**Core for Week 6:** write and understand a small set of tests for ordinary function results and one error case. The final takeaway still requires **only 2–3 simple pytest tests**; adding more tests here is for guided learning. **Optional/stretch:** pytest fixtures, monkeypatching, mocking, or AI SDK tests. No live API call, real Anthropic key, account, signup, or payment is required.

## Learning objectives

By the end of this lesson, you will be able to:

- Distinguish a normal case, a boundary case, and an error case.
- State what an expected error looks like in Python.
- Use `pytest.raises()` to check that a function rejects an invalid input.
- Test a business rule and a configuration rule separately.
- Explain why tests should avoid depending on real databases, credentials, or external services when possible.
- Choose 2–3 sensible tests for your own Week 5 product catalog.

## 1. What should happen when something goes wrong?

Suppose eComMART uses this stock rule:

```python
def is_low_stock(stock, threshold):
    return stock < threshold
```

The rule is **strictly less than** the threshold, so `stock=5, threshold=5` means stock is **not** low. That is a boundary case because the decision changes at that value.

Now imagine a configuration error:

```dotenv
LOW_STOCK_THRESHOLD=five
```

The value `five` is text, not a whole number. The function responsible for loading the threshold should reject it in a way that a developer can understand. Python often signals this using an **exception**: a named error such as `ValueError`.

A good test can check that **the correct exception occurs**. An error is not automatically a test failure — if your program *should* reject bad input, rejecting it is the correct behavior.

## 2. Three useful categories of test cases

| Category | Question | eComMART example | Expected result |
|---|---|---|---|
| Normal | Does the function handle ordinary input? | Stock `3`, threshold `5` | `True` |
| Boundary | Does it handle the exact decision edge? | Stock `5`, threshold `5` | `False` |
| Error | Does it reject a value that cannot be used? | Threshold text `five` | `ValueError` |

You do not need a huge number of tests this week. A small group of meaningful cases often teaches more than many nearly identical examples.

## 3. Understanding `pytest.raises()`

In Python, a function can signal invalid input using `raise`:

```python
def parse_quantity(text):
    return int(text)
```

`parse_quantity("12")` returns the number `12`. But `parse_quantity("twelve")` causes Python to raise `ValueError`.

Here is how pytest checks that **the error was expected**:

```python
import pytest


def parse_quantity(text):
    return int(text)


def test_invalid_quantity_raises_error():
    # Arrange
    bad_input = "twelve"

    # Act + Assert: the next call should raise ValueError.
    with pytest.raises(ValueError):
        parse_quantity(bad_input)
```

Read `with pytest.raises(ValueError):` as **“the indented call must raise a `ValueError`.”**

- If the expected error occurs, this test **passes**.
- If no error occurs, this test **fails** because the program accepted something it should have rejected.
- If a different error occurs, the test **fails**, helping you discover another problem.

The `with` block is a Python way to control what happens for a small indented section of code. You saw a similar shape earlier with file handling (`with open(...)`).

**Important:** The last example is just a teaching example. You do not need to add `parse_quantity()` to your eComMART application.

## 4. Guided build — test your existing configuration function

Continue in the same `separation_practice` folder used in the preceding lesson. Your files should include:

```text
separation_practice/
├── stock_alert.py
├── config.py
├── .env
└── tests/
    ├── test_stock_alert.py    # created in the previous lesson
    └── test_config.py         # create this one now
```

### Step 1 — Check the configuration function

In the preceding application-organization lesson, your `config.py` used `python-dotenv` and `os.getenv()` to read a threshold. The relevant function should have this behavior:

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()


def get_stock_threshold():
    raw_value = os.getenv("LOW_STOCK_THRESHOLD", "5")
    try:
        threshold = int(raw_value)
    except ValueError as error:
        raise ValueError("LOW_STOCK_THRESHOLD must be a whole number") from error

    if threshold < 0:
        raise ValueError("LOW_STOCK_THRESHOLD cannot be negative")

    return threshold
```

If your existing `config.py` already has this function, **keep it**. The key facts are that it returns an integer for valid input and raises `ValueError` for invalid input.

Notice the responsibilities: `config.py` checks the **setting**, while `stock_alert.py` checks **inventory stock**. Testing them separately makes it easier to find a bug.

### Step 2 — Keep the existing three stock tests

Your `tests/test_stock_alert.py` from the previous lesson already checks below, equal to, and above the threshold. Run it from **inside the `separation_practice` folder**:

```bash
python -m pytest tests/test_stock_alert.py -q
```

**Expected result:** `3 passed`. Make sure the deliberately broken expectation from the preceding lesson has been restored before continuing.

### Step 3 — Make one test for invalid configuration

Create `tests/test_config.py`:

```python
# tests/test_config.py
import os
import pytest

from config import get_stock_threshold


def test_threshold_rejects_text():
    # Arrange: save the previous value, if one exists.
    previous_value = os.environ.get("LOW_STOCK_THRESHOLD")

    try:
        # Arrange: pretend the setting contains invalid text.
        os.environ["LOW_STOCK_THRESHOLD"] = "five"

        # Act + Assert: this must raise ValueError.
        with pytest.raises(ValueError):
            get_stock_threshold()
    finally:
        # Restore the setting so the test does not affect later work.
        if previous_value is None:
            os.environ.pop("LOW_STOCK_THRESHOLD", None)
        else:
            os.environ["LOW_STOCK_THRESHOLD"] = previous_value
```

**Why save and restore the value?** Environment variables belong to the running process. A test should not accidentally change a setting that another test uses. `try` / `finally` makes sure the original value is restored whether the check passes or fails.

**Why not edit `.env` to `five`?** The test sets the value temporarily in memory. That is safer and faster than changing a file and trying to remember to change it back.

> **Beginner note:** You only need to understand that the test temporarily gives `get_stock_threshold()` a bad setting, expects `ValueError`, and puts the previous setting back. The save/restore code is shown in full so the exercise is safe to run. An optional tool called `monkeypatch` can shorten this later, but you do **not** need it for Week 6.

### Step 4 — Run only the new test

From the **`separation_practice` root** with the correct virtual environment active:

```bash
python -m pytest tests/test_config.py -q
```

**Expected result:** a report ending in `1 passed`. The test succeeds because `get_stock_threshold()` correctly rejects `five`.

### Step 5 — Run the complete small suite

```bash
python -m pytest -q
```

**Expected result:** `4 passed` if you have exactly the three tests from the preceding lesson and this new configuration test. That is four **guided-practice** tests; it does **not** increase the required independent-challenge minimum of 2–3 tests.

### Step 6 — Understand what a failed error test means

Read the test again. If the configuration function silently accepted `five` and returned an arbitrary number, then `pytest.raises(ValueError)` would report **“DID NOT RAISE”** and the test would fail.

**Do not change your actual `config.py` to make it incorrect just to see a failure.** Understanding the report is sufficient for this exercise.

## 5. Why we test deterministic logic first

A **deterministic function** produces the same answer when given the same inputs. For example:

```python
is_low_stock(3, 5)  # Always True for this rule
```

That makes it easy to know what to assert. In contrast, a real API response can depend on network availability, service behavior, rate limits, or cost. A database can depend on old records left behind from earlier runs.

| Easier beginner test | More complicated test |
|---|---|
| Compare two stock numbers | Write real records to the Week 5 SQLite database |
| Format an alert string | Send an email or notification |
| Validate a local threshold | Connect to a live LLM or external service |

For Week 6, concentrate on **local, predictable functions**. When we later introduce agent tools, these functions can become safe building blocks: an AI system may choose **when** to call a stock tool, while ordinary Python code still decides **whether** the stock is low.

**Core:** test deterministic behavior without an AI connection. **Optional/stretch:** learn test fixtures, mocking, or the `monkeypatch` fixture in a later lesson. Never place real API keys in tests.

## 6. Your Week 5 catalog — selecting 2–3 meaningful tests

For the required **Takeaway Hands-on Exercise**, you will restructure **your own Week 5 eComMART catalog**, preserving its original functionality. Do not replace your Week 5 file with the low-stock notifier; these are separate projects serving different learning goals.

Before writing tests for the catalog, inspect its existing functions. Choose **2–3 tests** that match the features **your version actually implements**. Potential categories include:

1. **Normal case:** a small function accepts valid product data and returns or formats the expected result.
2. **Boundary or missing-data case:** a lookup or validation function handles an edge value or missing item as the existing app specifies.
3. **Error case:** a function rejects invalid data *if your actual function already has that validation*.

These are suggestions, **not** instructions to invent behavior or change Week 5 rules just to make a particular test pass. Tests must reflect the requirements and behavior of your code.

If your chosen function accesses SQLite, **do not run tests against your real catalog database**. For this week's required 2–3 tests, prefer pure helper functions that need no database. If you choose a database-writing test as an extra challenge, use a **separate temporary database**; that is beyond the minimum required work.

## 7. Guided practice — predict the results

Without running the code, decide whether each test **should pass**:

| Check | Expected behavior | Should it pass? |
|---|---|---|
| `assert is_low_stock(2, 5) is True` | Below threshold is low stock | ? |
| `assert is_low_stock(5, 5) is True` | Exactly at threshold is low stock | ? |
| `with pytest.raises(ValueError): int("five")` | Invalid number text raises `ValueError` | ? |

**Self-check:** **Pass**, **fail**, **pass**. The second test fails because the rule uses `<`, not `<=`.

### Optional/stretch — shorter configuration test

Once you are comfortable with the core version above, pytest offers `monkeypatch`, a fixture (a helper pytest provides to tests) that automatically restores modified environment variables:

```python
def test_threshold_rejects_text_with_monkeypatch(monkeypatch):
    monkeypatch.setenv("LOW_STOCK_THRESHOLD", "five")
    with pytest.raises(ValueError):
        get_stock_threshold()
```

This is **bonus material only**. Neither fixtures nor mocking are required for the Week 6 takeaway.

## 8. Common mistakes and troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| `No module named pytest` | pytest is not installed in the active environment | Activate `.venv`; run `python -m pip install pytest` |
| `No module named dotenv` | `python-dotenv` was not installed for the active Python | Install the recorded dependency from `requirements.txt` |
| `No module named config` | Ran tests from the wrong folder | Run pytest from the folder containing `config.py` |
| `DID NOT RAISE ValueError` | The function accepted invalid input or the test used the wrong input | Confirm `LOW_STOCK_THRESHOLD` is set to `five` for the tested call |
| One test affects other tests | A setting changed and was not restored | Use the provided `try` / `finally` pattern |
| Only the error test passes | The other tests are missing or not discovered | Check `tests/test_stock_alert.py` and `test_` function names |
| Tests modify real Week 5 data | A database-writing function points at your normal database | Stop; choose a safe pure function or an isolated test database |

## 9. Knowledge check

1. How is a boundary case different from a normal case?
2. What does `ValueError` usually tell you?
3. What does `with pytest.raises(ValueError):` check?
4. Why should the test restore an environment variable after changing it?
5. How many pytest tests must you write for the **independent Week 5 catalog challenge**?

**Answers:** (1) It checks a value at an edge where the rule changes. (2) A value is not appropriate for an operation or conversion. (3) That a call raises that expected error. (4) To avoid affecting later work or tests. (5) **2–3 simple tests**, not four or a large suite.

## Lesson recap

- A useful test suite checks successful results **and** meaningful boundaries or errors.
- `pytest.raises()` lets a test pass when an expected exception occurs.
- Configuration rules and stock rules have separate responsibilities, so they can be tested separately.
- Small, predictable Python functions are good foundations for later agent tools.
- **Core requirement remains unchanged:** a virtual environment, `requirements.txt`, one environment variable, and **2–3 simple pytest tests** for your own Week 5 catalog.
- Anthropic SDK integration, live LLM calls, paid accounts, real API keys, and mocking are not required.

**Next section:** `../03_Virtual_Environments/01_Why_Isolated_Environments_Matter.md` will explain isolated Python project environments before discussing any optional SDK setup.
