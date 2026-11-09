# Testing Deterministic Tools Before Connecting an LLM

## Lesson purpose

A future eComMART AI assistant might answer a warehouse employee who asks, “Which products need restocking?” Before an AI model can use a stock-checking function safely, the team needs evidence that the function works **on its own**. If a normal Python function makes a mistake, putting an LLM in front of it does not fix the mistake.

This lesson brings together the week's earlier ideas: write one small Python function, define its expected behavior, test ordinary and unusual inputs with `pytest`, and keep the AI integration separate.

**Core for Week 6:** write and run a few local tests for predictable Python behavior. **Optional/stretch:** think about how a future LLM might choose the function; advanced mocking, SDK integration, and API calls are **not required**. You do not need a real Anthropic account, API key, signup, payment, or live LLM call. If you experiment with `.env`, use a placeholder only.

## Learning objectives

By the end of this lesson, you will be able to:

- Explain **deterministic** in the context of a stock-checking function.
- Describe a simple **tool contract**: inputs, output, rules, and errors.
- Write a function that formats a low-stock alert without changing data or contacting a service.
- Use **Arrange → Act → Assert** to test an ordinary case and a boundary case.
- Use `pytest.raises()` to test an invalid input.
- Explain which checks must pass before a future AI assistant is allowed to call a tool.

## 1. eComMART's business rule comes first

The warehouse team has agreed to this rule: **a low-stock alert is needed only when the quantity is less than the configured threshold**. Equal values do **not** trigger an alert.

| Product | Quantity | Threshold | Expected message |
|---|---:|---:|---|
| Wireless Barcode Scanner | 4 | 10 | `LOW STOCK: Wireless Barcode Scanner has 4 units (threshold: 10).` |
| Thermal Label Roll | 120 | 10 | `OK: Thermal Label Roll has 120 units.` |
| USB-C Docking Station | 10 | 10 | `OK: USB-C Docking Station has 10 units.` |

This rule does not need AI. It is ordinary business logic that Python can calculate consistently.

**Deterministic** means that the same valid inputs produce the same output. For example, checking the scanner with quantity `4` and threshold `10` should return the same alert every time. A function is easier to test when it does not depend on the current time, live internet responses, or other changing information.

## 2. Define a tool contract before writing code

An **agent tool** is a capability that an AI-enabled application might ask to run in the future. Today we will write an ordinary Python function that *could later* be such a tool.

| Contract part | eComMART decision |
|---|---|
| Function name | `format_stock_alert` |
| Inputs | `product_name` (nonempty text), `quantity` (nonnegative whole number), `threshold` (nonnegative whole number) |
| Low-stock rule | Alert if `quantity < threshold` |
| Output | One predictable text message |
| Invalid input | Raise `ValueError` with a useful explanation |
| Side effects | None: do not update the database, send a message, or call an API |

A **side effect** means changing something beyond returning a result, such as editing a database row or sending an email. We deliberately avoid side effects here so students can test safely.

```text
Warehouse employee's future request
                |
                v
  Future LLM chooses an allowed tool    <-- NOT connected this week
                |
                v
   format_stock_alert(...) in Python
                |
                v
         Validate inputs
                |
                v
       Apply stock < threshold
                |
                v
       Return a text message
                |
                v
       Local pytest verification         <-- THIS WEEK'S WORK
```

Notice that the future LLM would not decide whether `4 < 10`. **The Python function owns that rule.**

## 3. Guided practice — create the local project

Create a new folder named `ecommart_tool_tests`. This is a small practice project, **not** the Week 5 catalog refactor and **not** the Instructor Demo application you will build in Section 06.

```text
ecommart_tool_tests/
├── .venv/                       # Created locally; never submit it
├── stock_tool.py                # Business rule and message formatting
├── tests/
│   └── test_stock_tool.py      # Automated checks
└── requirements.txt             # Records the test dependency
```

Open a terminal inside `ecommart_tool_tests`.

| System | Create environment | Activate environment |
|---|---|---|
| Windows PowerShell | `py -m venv .venv` | `.\.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `py -m venv .venv` | `.venv\Scripts\activate.bat` |
| macOS / Linux | `python3 -m venv .venv` | `source .venv/bin/activate` |

If Windows PowerShell blocks activation, you may switch to Command Prompt and its matching command. Do not change machine-wide security policies just to complete a lesson.

With the environment active, run:

```bash
python -m pip install pytest
python -m pip freeze > requirements.txt
python -m pytest --version
```

**Expected result:** the last command displays a pytest version. The version in `requirements.txt` depends on what was installed; do not manually guess a version. No external AI service is involved.

Create the `tests` folder in the editor or file explorer. You do not need a Python package or `__init__.py` for this small project when running pytest from the project root.

## 4. Build the predictable stock tool

Create `stock_tool.py`:

```python
# stock_tool.py

def format_stock_alert(product_name, quantity, threshold):
    """Return a stock message without changing inventory or calling an API."""
    if not isinstance(product_name, str) or not product_name.strip():
        raise ValueError("product_name must be nonempty text")

    # bool counts as int in Python, so reject it explicitly.
    if type(quantity) is not int or type(threshold) is not int:
        raise ValueError("quantity and threshold must be whole numbers")
    if quantity < 0 or threshold < 0:
        raise ValueError("quantity and threshold cannot be negative")

    name = product_name.strip()
    if quantity < threshold:
        return f"LOW STOCK: {name} has {quantity} units (threshold: {threshold})."
    return f"OK: {name} has {quantity} units."


if __name__ == "__main__":
    print(format_stock_alert("Wireless Barcode Scanner", 4, 10))
    print(format_stock_alert("Thermal Label Roll", 120, 10))
```

**Read the code in this order:**

1. `def` defines a function. The three names in parentheses are its **parameters** (inputs).
2. The first checks reject a missing name, non-integer quantities, and negative numbers. Clear input checks help prevent surprising behavior.
3. `name = product_name.strip()` removes extra whitespace around the product name.
4. `quantity < threshold` is the exact eComMART rule; equality does not trigger an alert.
5. `return` gives the caller a result without printing or changing records.
6. The `if __name__ == "__main__":` block runs only when you directly execute this file, not when pytest imports the function.

Run from the project root:

```bash
python stock_tool.py
```

**Expected output:**

```text
LOW STOCK: Wireless Barcode Scanner has 4 units (threshold: 10).
OK: Thermal Label Roll has 120 units.
```

If your output differs, inspect the comparison operator and the punctuation in the returned strings before writing tests.

## 5. Write three pytest tests using Arrange → Act → Assert

**Arrange** means prepare inputs. **Act** means call the function. **Assert** means check the returned result against the expected result.

Create `tests/test_stock_tool.py`:

```python
# tests/test_stock_tool.py
import pytest

from stock_tool import format_stock_alert


def test_low_stock_returns_alert():
    # Arrange
    name = "Wireless Barcode Scanner"
    quantity = 4
    threshold = 10

    # Act
    message = format_stock_alert(name, quantity, threshold)

    # Assert
    assert message == "LOW STOCK: Wireless Barcode Scanner has 4 units (threshold: 10)."


def test_equal_to_threshold_is_not_low_stock():
    # Arrange
    name = "USB-C Docking Station"
    quantity = 10
    threshold = 10

    # Act
    message = format_stock_alert(name, quantity, threshold)

    # Assert
    assert message == "OK: USB-C Docking Station has 10 units."


def test_negative_quantity_raises_value_error():
    # Arrange
    quantity = -1

    # Act + Assert: this invalid input must be rejected.
    with pytest.raises(ValueError, match="cannot be negative"):
        format_stock_alert("Wireless Barcode Scanner", quantity, 10)
```

Why these three?

- **Normal case:** when stock is genuinely low, the correct alert appears.
- **Boundary case:** when quantity equals the threshold, no alert appears.
- **Error case:** a negative quantity is rejected instead of becoming a misleading business result.

`pytest.raises()` checks that the function produces an **expected error**. A test **passes** when the expected error happens; the unexpected absence of an error makes the test fail.

From the project root (the folder containing `stock_tool.py`), run:

```bash
python -m pytest -q
```

**Expected result:** a summary containing `3 passed`. The execution time may vary. If Python reports `ModuleNotFoundError: No module named 'stock_tool'`, confirm that your terminal is in `ecommart_tool_tests` and that `stock_tool.py` is next to `tests/`, not inside it.

## 6. Make one test fail on purpose, then repair the bug

A test that only ever passes is not enough evidence that it can detect a mistake.

1. Temporarily change the condition in `stock_tool.py` from `quantity < threshold` to `quantity <= threshold`.
2. Run `python -m pytest -q` again.
3. Find the failed test: **equal-to-threshold** should no longer be treated correctly.
4. Read pytest's **expected** and **actual** message values.
5. Restore `<` and rerun the tests.

**Expected sequence:** first all three tests pass; after introducing the bug, the boundary test fails; after fixing the comparison, all three pass again.

This is a small example of **regression testing**: using existing tests to catch a bug introduced by a later edit.

## 7. What should be checked before a future LLM connection?

A local tool should have dependable behavior **before** an AI application is allowed to call it. A sensible first checklist is:

| Check | Question | Evidence in this lesson |
|---|---|---|
| Clear inputs | Does the tool state what data it accepts? | Contract table and validation checks |
| Predictable output | Does it return a defined result? | Exact message assertions |
| Correct boundaries | Does equality behave correctly? | Second test |
| Safe errors | Does invalid data get rejected? | Third test |
| No unnecessary side effects | Does it avoid modifying inventory? | Function only returns text |
| No external dependency for core logic | Can it run without an LLM or network? | `python -m pytest -q` works locally |

These checks do **not** prove that a future AI integration will be safe or correct; they verify the Python part that the AI might eventually use. Future lessons may add permissions, tool-call validation, authorization, and testing of model interactions.

### Optional/stretch thought experiment — no code needed

If an LLM were to request `format_stock_alert(product_name="Scanner", quantity=-5, threshold=10)`, the function would raise `ValueError`. This is preferable to silently presenting an impossible quantity as valid.

**Optional only:** advanced students can write a fourth test checking a blank name, or explore mocking in a later course. Do not install the Anthropic SDK, create a real key, make API calls, or mock an LLM to meet this week's required outcome.

## 8. Troubleshooting

| Problem | Likely cause | Beginner-friendly fix |
|---|---|---|
| `No module named pytest` | pytest was not installed into the active environment | Activate `.venv`, then run `python -m pip install pytest` |
| `No module named stock_tool` | Wrong terminal directory or file placement | Run from `ecommart_tool_tests`, with `stock_tool.py` in the root |
| `collected 0 items` | File or test function does not start with `test_` | Use `tests/test_stock_tool.py` and `def test_...():` |
| Expected alert but got `OK` | Condition or threshold is wrong | Confirm the rule is **strictly less than** (`<`) |
| Test fails on punctuation | String differs from expected text | Compare the entire output message carefully |
| Red traceback mentions `ValueError` | An invalid input was used outside the expected-error test | Check input values; in tests use `pytest.raises()` for expected errors |

## 9. Guided practice and knowledge check

**Try without looking at the answer first:**

1. Run `format_stock_alert("Packing Tape", 0, 5)` manually. Predict the result before running it.
2. Change the threshold to `0` and predict the result for quantity `0`.
3. In plain language, explain why `quantity=10` and `threshold=10` must **not** trigger an alert.
4. Point to the part of the function that validates data before applying the stock rule.
5. Explain why testing this Python tool does not require a Claude account.

**Self-check:** For `("Packing Tape", 0, 5)`, the result is a low-stock alert. For quantity `0` and threshold `0`, the result is `OK`, because `0 < 0` is false. A Claude account is unnecessary because the function executes locally with no AI call.

## 10. Lesson recap and connection to the Instructor Demo

- A **deterministic tool-shaped function** follows a clearly defined rule and returns predictable results.
- A **tool contract** states accepted inputs, output format, error behavior, and side effects.
- Three well-chosen tests can cover a normal case, a boundary, and an error.
- `pytest` detects mistakes before other parts of a system depend on the function.
- **Core Week 6 work is local Python testing.** AI SDKs, API calls, real keys, and mocking are optional or outside this week's requirements.

In `06_Building_the_eComMART_Mini_Project/`, you will see the instructor assemble a fresh **low-stock notifier** using modules, a virtual environment, a configuration variable, and pytest. The separate **Independent Challenge** will then apply the same project-organization skills to **your own Week 5 catalog**.
