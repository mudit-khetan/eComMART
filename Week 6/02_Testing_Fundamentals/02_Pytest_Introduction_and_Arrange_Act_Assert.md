# Pytest Introduction and Arrange → Act → Assert

## Lesson purpose

In the previous lesson, you wrote `assert` statements in `check_stock.py` to check the eComMART low-stock rule. That showed how Python can compare an *actual result* with an *expected result*. However, a growing project needs an easier way to collect and run many checks.

**pytest** is a Python testing tool that discovers specially named test files, runs the checks inside them, and shows which checks passed or failed. This lesson turns your existing checks into a small, repeatable test suite. You do not need to learn classes or write complicated setup code.

**Core for Week 6:** install pytest in a small local virtual environment, write 2–3 straightforward tests, and run them using **Arrange → Act → Assert**. **Optional/stretch:** explore more pytest features. No Anthropic account, real API key, signup, payment, live API call, or mocking is required.

## Learning objectives

By the end of this lesson, you will be able to:

- Explain what pytest does and why it is useful.
- Recognize the filenames and function names pytest looks for.
- Describe the three stages of **Arrange → Act → Assert** in plain language.
- Write three small tests for a predictable eComMART function.
- Run pytest in an activated virtual environment and interpret a pass or failure.
- Identify common beginner mistakes when running tests.

## 1. The eComMART problem — repeating checks

Imagine the inventory team changes the alert wording next week. The stock comparison must still behave correctly:

| Stock | Threshold | Expected answer to “Is stock low?” |
|---:|---:|---|
| 3 | 5 | `True` |
| 5 | 5 | `False` |
| 8 | 5 | `False` |

You *could* retype these examples in the Python interpreter every time. Instead, pytest remembers the checks as functions and runs them together on demand. That makes it easier to spot a **regression**: a change that accidentally breaks something that used to work.

## 2. Three words to understand before using pytest

- A **framework/tool** is reusable software that helps you perform a task. pytest helps run tests; it does not write correct business rules for you.
- A **test function** is an ordinary Python function whose job is to check expected behavior.
- **Test discovery** means pytest looks for files and functions that follow its naming rules, so you do not have to run every test individually.

For our beginner exercises, follow two naming rules:

1. Name the file `test_stock_alert.py` (it begins with `test_`).
2. Name each check `def test_something_descriptive():` (the function begins with `test_`).

Unlike a normal script, you usually do **not** call the test functions yourself. pytest finds and runs them.

## 3. Arrange → Act → Assert

A helpful way to write a test is to divide it into three thinking steps:

| Step | Question to ask | eComMART example |
|---|---|---|
| **Arrange** | What inputs and starting conditions do I need? | Stock is `3`, threshold is `5` |
| **Act** | What function am I checking? | Call `is_low_stock(3, 5)` |
| **Assert** | Does the actual result match the expected result? | Expect `True` |

Here is one complete test:

```python
def test_stock_below_threshold():
    # Arrange: choose a product's stock and alert threshold.
    stock = 3
    threshold = 5

    # Act: ask the stock-checking function for its result.
    result = is_low_stock(stock, threshold)

    # Assert: check that it returned the expected answer.
    assert result is True
```

Notice what the test **does not** do: it does not open a database, ask a user for input, or call an AI service. Small predictable functions are a good place to start.

## 4. Guided build — your first pytest test suite

Continue with the `separation_practice` project from the preceding lessons. This is a **small standalone practice project**, not your Week 5 product catalog. Do not overwrite that catalog yet.

Your project should look like this:

```text
separation_practice/
├── main.py
├── stock_alert.py
├── config.py
├── .env
├── .env.example
└── tests/
    └── test_stock_alert.py   # create this file now
```

`stock_alert.py` should contain the function introduced in the previous lesson:

```python
def is_low_stock(stock, threshold):
    return stock < threshold


def make_alert(product_name, stock, threshold):
    if is_low_stock(stock, threshold):
        return f"LOW STOCK: {product_name} has {stock} units left."
    return f"Stock OK: {product_name} has {stock} units."
```

If your existing file already has these functions, keep it — you do **not** need duplicate copies.

### Step 1 — Open the right terminal folder

Open the terminal in your editor. Navigate to the folder containing `main.py` and `stock_alert.py`. For example:

```bash
cd separation_practice
```

If you are *already inside* `separation_practice`, do not run `cd separation_practice` again. To check where you are, use `pwd` on macOS/Linux or `cd` on Windows Command Prompt. You should see `stock_alert.py` in the folder.

Activate the `.venv` you created **inside `separation_practice/`** during Section 01. This is a short setup preview: formal `venv` and `pip` explanations come in Sections 03–04. Keep this environment only for the practice project; do not reuse your Week 5 catalog environment. From the `separation_practice` folder, use the command for your terminal:

| Terminal | Activate the `.venv` in this folder |
|---|---|
| Windows PowerShell | `.\.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `.venv\Scripts\activate.bat` |
| macOS/Linux (bash or zsh) | `source .venv/bin/activate` |

If you have not created it yet, run `py -m venv .venv` on Windows or `python3 -m venv .venv` on macOS/Linux **from this folder**, then activate it with the matching command above. If PowerShell blocks script activation, open Windows Command Prompt and use its activation command instead. The complete explanation of these commands comes in Section 03.

### Step 2 — Install and verify pytest

Use `python -m pip` so the package is installed for the Python interpreter you are using:

```bash
python -m pip install pytest
python -m pytest --version
```

**Expected result:** the second command prints a pytest version number, such as `pytest X.Y.Z`. The precise version may differ with your Python version and the day you install it. If pytest is already installed in your active environment, you do not need to reinstall it.

**Dependency reminder:** This is a guided early installation, not a full dependency-management lesson. Your project's `requirements.txt` should record pytest so someone else can recreate the same environment. The dependency-management lessons in Section 04 will later explain how to record and pin installed versions. `pytest` is a third-party package; it is not built into Python.

### Step 3 — Create the test file

Inside `separation_practice`, create a `tests` folder if it is not already there. Then create `tests/test_stock_alert.py` with **all** the code below:

```python
# tests/test_stock_alert.py
from stock_alert import is_low_stock


def test_low_stock_returns_true():
    # Arrange
    stock = 3
    threshold = 5

    # Act
    result = is_low_stock(stock, threshold)

    # Assert
    assert result is True


def test_stock_at_threshold_returns_false():
    # Arrange
    stock = 5
    threshold = 5

    # Act
    result = is_low_stock(stock, threshold)

    # Assert
    assert result is False


def test_sufficient_stock_returns_false():
    # Arrange
    stock = 8
    threshold = 5

    # Act
    result = is_low_stock(stock, threshold)

    # Assert
    assert result is False
```

There are **three tests** in one file. The second is especially important: if the code accidentally used `<=` rather than `<`, it would catch the mistake.

### Step 4 — Run pytest

From the **`separation_practice` project root** (the folder containing `stock_alert.py`), run **the command below**. Do not launch it from the Week 6 folder or from inside `tests/`, since that may cause `ModuleNotFoundError` when Python looks for `stock_alert.py`:

```bash
python -m pytest -q
```

**Expected result:** a short report similar to:

```text
...                                                                      [100%]
3 passed in 0.0Xs
```

The timing and formatting can vary. What matters is **`3 passed`**. pytest may display `...` because each dot represents one passing test.

If you run the tests from the wrong directory, imports can fail. Return to the project root and rerun the command.

### Step 5 — Learn from an intentional failure

Temporarily change **only** the last line of the second test to this deliberately incorrect expectation:

```python
assert result is True
```

Run the tests again:

```bash
python -m pytest -q
```

**Expected result:** `1 failed, 2 passed`. pytest will show the failing assertion and help you locate the test. This is good evidence that the test is capable of detecting a problem.

**Restore the correct expectation** (`assert result is False`) and rerun until you see **`3 passed`**. Do not submit the deliberately broken test as your completed work.

## 5. Reading a pytest result

| Result | Meaning | Your next action |
|---|---|---|
| `3 passed` | All three expectations matched the program's results | Continue |
| `1 failed, 2 passed` | pytest ran all three tests, but one expectation did not match | Read the assertion and compare expected versus actual |
| `collected 0 items` | pytest did not find tests under its naming rules | Check `test_...py` and `def test_...()` |
| `ModuleNotFoundError` | Python cannot locate a module | Check your current directory, filenames, and import statement |
| `No module named pytest` | pytest is not installed in the Python environment being used | Activate `.venv` and run `python -m pip install pytest` |

A failed test is **information**, not a reason to delete the test. First check whether the code is wrong, the expected result is wrong, or the business rule was misunderstood.

## 6. Guided practice — explain the test before running it

Without changing the code yet, answer these questions:

1. If stock is `4` and threshold is `5`, what should `is_low_stock()` return?
2. If stock is `5` and threshold is `5`, what should it return?
3. Which part of Arrange → Act → Assert calls the function?
4. Why does `print(result)` not replace `assert result is True`?

**Self-check:** (1) `True`. (2) `False`. (3) **Act**. (4) Printing only displays a result; asserting checks it against an expected value.

**Try it:** Change the *inputs* in the first test to `stock = 4` and `threshold = 5`. Keep the expected result `True`. Run pytest again and confirm all three tests still pass. Restore the sample values afterward if you want to keep the published example unchanged.

### Optional/stretch (not required)

Try running just one test by name:

```bash
python -m pytest tests/test_stock_alert.py::test_stock_at_threshold_returns_false -q
```

Or explore `python -m pytest -v` for a more detailed report. Neither command is required for the graded Week 6 takeaway.

## 7. Common mistakes and troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| `0 tests` found | File/function names do not start with `test_` | Rename the file and functions using pytest conventions |
| `No module named pytest` | Installed pytest in a different environment | Activate the correct `.venv`; use `python -m pip install pytest` |
| `No module named stock_alert` | Running from the wrong folder or a misspelled filename | Run `python -m pytest -q` from `separation_practice` |
| The test is always marked as passed | You printed the result but never asserted anything | Add an `assert` with a meaningful expected value |
| Test fails at stock exactly 5 | The program or expectation uses the wrong comparison | Confirm the requirement is **strictly less than** 5 |
| `NameError: is_low_stock is not defined` | Missing import at the top of the test file | Add `from stock_alert import is_low_stock` |

## 8. Knowledge check

1. What does pytest **discover** automatically?
2. Which two names must begin with `test_` in our examples?
3. What do Arrange, Act, and Assert each do?
4. What does `3 passed` tell you — and what does it **not** tell you?
5. Must a Week 6 pytest test connect to Claude or any other LLM?

**Answers:** (1) Test files and functions that follow its conventions. (2) The file name and each test-function name. (3) Prepare inputs, call the function, compare with an expected result. (4) Three specific checks succeeded; it does not prove the program has no other bugs. (5) **No.** The required tests run locally.

## Lesson recap

- pytest runs your checks and reports which ones passed or failed.
- `test_` naming conventions help pytest find tests.
- **Arrange → Act → Assert** makes tests easy to read and reason about.
- The eComMART low-stock rule can be checked without a database or LLM.
- **Three simple passing tests are enough to practice the required testing skill.**
- The final Week 6 takeaway still asks for **2–3 simple pytest tests for your own Week 5 catalog**, plus a virtual environment, `requirements.txt`, and an environment variable.

**Next lesson:** `03_Testing_Functions_and_Error_Scenarios.md` shows why we should test both correct results and what happens when something goes wrong.
