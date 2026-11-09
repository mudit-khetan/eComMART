# Why Automated Testing Matters

## Lesson purpose

You have now seen how an eComMART program can be split into small functions and modules. But how do we know those functions still work after we change the code?

In Week 5, you could run your product catalog manually: add a product, search for it, update its details, and check the output. That is useful. But every time the application changes, repeating the same checks by hand takes time, and it is easy to forget an unusual case.

**Automated testing** means writing code that checks other code. Today we focus on the *reason* for doing it and start with very small checks. In the next lesson, we will run those checks using **pytest**.

**Core for Week 6:** understand why tests matter and identify 2–3 important checks for a simple Python function. **Optional/stretch:** investigate test coverage, database test isolation, or mocking. No LLM, Anthropic account, real API key, signup, payment, or live API call is required.

## Learning objectives

By the end of this lesson, you will be able to:

- Explain the difference between manual and automated testing.
- Describe why a program needs tests even when it ran successfully once.
- Recognize a **test case**, **expected result**, **actual result**, and **regression**.
- Distinguish normal cases, boundary cases, and error cases.
- Write a basic `assert` check for the eComMART stock rule.
- Select a small, useful set of future pytest tests.

## 1. The eComMART problem — “It worked yesterday”

Imagine eComMART shows a low-stock alert whenever a product has fewer than 5 units. The team later changes the wording of its messages. A developer tests only a product with 3 units and sees the expected warning.

That is a good start, but it leaves questions:

- What if the product has **exactly 5** units?
- What if it has **8** units?
- What if the stock value is invalid?
- Did changing the message accidentally change the stock rule?

An application can work for **one example** and still contain a bug for another. A **bug** is a mistake in code or behavior.

A **regression** happens when a change breaks something that previously worked. Automated tests are especially useful for catching regressions early.

## 2. Manual tests and automated tests

| Manual testing | Automated testing |
|---|---|
| A person runs the program and checks what appears | Test code runs a function and checks the result |
| Useful for exploring a new feature | Useful for repeating known checks consistently |
| Can take time when repeated after every edit | Can run many small checks quickly |
| Human judgment can notice confusing experiences | Checks only what the test author actually specified |

**Automated tests do not replace thinking.** A test with the wrong expected result can pass even when the business requirement is wrong. We must decide **what correct behavior means** first.

## 3. Four testing terms in plain language

Consider the business rule: **low stock means stock is strictly less than the threshold**.

| Term | Meaning | Example |
|---|---|---|
| Test case | One situation we want to check | Stock = `3`, threshold = `5` |
| Expected result | What should happen if the rule is correct | `True` (low stock) |
| Actual result | What the program really returns | The value returned by `is_low_stock(3, 5)` |
| Pass or fail | Whether actual and expected match | Pass if the result is `True` |

A good test describes a meaningful example, not just a random number.

### Normal, boundary, and error cases

- **Normal case:** `stock = 3`, `threshold = 5` → low stock is `True`.
- **Boundary case:** `stock = 5`, `threshold = 5` → low stock is `False`. *Boundary* means a value at the edge where the decision changes.
- **Error case:** configuration says `LOW_STOCK_THRESHOLD=five` → the settings function should explain the invalid number instead of silently proceeding.

For the final Week 6 takeaway, **2–3 tests** are sufficient. You do not need to test every possible value.

## 4. How a tiny automated check works

Recall the predictable function from the previous lesson:

```python
def is_low_stock(stock, threshold):
    return stock < threshold
```

You can check it manually in the Python interpreter, but you can also write an `assert` statement:

```python
assert is_low_stock(3, 5) is True
```

Read this as: “I expect the function to return `True` for stock 3 and threshold 5.”

If the condition is true, execution continues without printing a success message. If it is false, Python raises an **AssertionError**. Later, pytest will collect these checks and show a readable report.

This is not the same as showing a printed message:

```python
print(is_low_stock(3, 5))
```

`print()` displays a value for a human to inspect. `assert` **checks an expectation automatically**.

## 5. Guided practice — make your first checks

This practice can reuse the `separation_practice` folder you created in the preceding lesson. You do **not** need to create or alter your Week 5 catalog yet.

### Step 1 — Check your existing function

Open `separation_practice/stock_alert.py`. It should contain:

```python
def is_low_stock(stock, threshold):
    return stock < threshold


def make_alert(product_name, stock, threshold):
    if is_low_stock(stock, threshold):
        return f"LOW STOCK: {product_name} has {stock} units left."
    return f"Stock OK: {product_name} has {stock} units."
```

If your file already contains the same functions, **do not create duplicate definitions**. Keep the existing ones.

### Step 2 — Create a tiny check script

In the **same `separation_practice/` folder**, create `check_stock.py`:

```python
# check_stock.py
from stock_alert import is_low_stock

# Check a normal low-stock example.
assert is_low_stock(3, 5) is True

# Check the boundary: 5 is not below 5.
assert is_low_stock(5, 5) is False

# Check a product that has enough stock.
assert is_low_stock(8, 5) is False

print("All three stock checks passed.")
```

**Why this file?** For now, it lets us understand what automated checks do without introducing a new test framework in the middle of the explanation. In the next lesson, we will turn checks like these into `test_...` functions for pytest.

### Step 3 — Run the checks

From your terminal **inside `separation_practice/`**, run:

```bash
python check_stock.py
```

**Expected output:**

```text
All three stock checks passed.
```

If a check fails, you will see `AssertionError` instead of the success message.

### Step 4 — Observe a deliberate failure

Temporarily change the second assertion to this **incorrect expectation**:

```python
assert is_low_stock(5, 5) is True
```

Run `python check_stock.py` again. The check should fail with `AssertionError` because `5 < 5` is false. This failure is **intentional**: it proves the check can detect a mismatch.

**Restore the correct line afterward:**

```python
assert is_low_stock(5, 5) is False
```

Run again and confirm all three checks pass. Do not leave intentionally broken checks in your practice project.

## 6. Why small functions are easier to test

The `is_low_stock()` function takes numbers and returns `True` or `False`. Its answer does not depend on a menu, a database file, or a network response. We can therefore test it directly.

Compare the responsibilities:

```text
main.py                 Starts the app and prints a result
       |
       v
stock_alert.py          Makes a predictable low-stock decision
       ^
       |
check_stock.py          Calls the function and checks its answer
```

This design matters later for **agent tools** as well. A future AI assistant may choose *when* to call a stock-checking function, but the function's numeric rule should still work correctly on its own. We test that deterministic rule **before** connecting anything to an LLM.

**Core:** test the Python rule without any AI service. **Optional/stretch:** future lessons may show how to isolate a network client in tests. Mocking and live LLM testing are not required in Week 6.

## 7. Designing 2–3 useful tests for your own app

In the required independent challenge, you will restructure **your own Week 5 eComMART product catalog**. Think about its existing functions. Which ones could be checked automatically?

For example, depending on the functions in *your* catalog, you might choose:

1. A valid product input is accepted and returns the expected result.
2. A lookup for a missing product has the expected outcome.
3. An invalid input is rejected or handled in the documented way.

These are **test ideas**, not instructions to invent features your Week 5 code never had. Match the tests to what your application actually does. If a function writes to SQLite, the test must avoid damaging your real practice database; we will keep the required tests simple and focus on functions or safe, controlled inputs.

**Your required takeaway remains just 2–3 simple pytest tests.** You are not required to create a large test suite or learn mocking.

## 8. Guided exercise — decide what deserves a test

For each situation, write the **input** and the **expected result** before looking at the self-check.

| Situation | Input | Expected result |
|---|---|---|
| Low stock | `stock=2`, `threshold=5` | ? |
| Exactly on threshold | `stock=5`, `threshold=5` | ? |
| Stock is sufficient | `stock=7`, `threshold=5` | ? |

**Self-check:** `True`, `False`, `False`.

Now explain in one sentence: why is the second case particularly important? **Suggested answer:** It checks the exact boundary and confirms the rule uses “less than,” not “less than or equal to.”

### Optional/stretch thought exercise

What if someone changes the rule from `stock < threshold` to `stock <= threshold`? Which check would catch the mistake? The **exact-threshold** check.

No code changes or additional installations are needed for this thought exercise.

## 9. Common mistakes and troubleshooting

| Problem | Why it happens | What to do |
|---|---|---|
| `ModuleNotFoundError: No module named 'stock_alert'` | `check_stock.py` and `stock_alert.py` are not together | Keep them in the same `separation_practice/` folder |
| `AssertionError` after changing the boundary expectation | The test expects `True`, but the rule correctly returns `False` | Restore `assert is_low_stock(5, 5) is False` |
| Program prints `True`, but no check fails | You used `print()` instead of `assert` | Use `assert` to compare the result with a clear expectation |
| `check_stock.py` finishes with no output | You may have removed the last `print()` line; passing assertions normally print nothing | Keep the success message for this first exercise |
| Writing tests that depend on a real API | Confuses an external service with a local Python rule | Keep tests local and deterministic; no API signup or network call is required |

## 10. Knowledge check

1. What is a **regression**?
2. Why is a test different from simply printing a value?
3. What is a **boundary case** for a threshold of 5?
4. What does `AssertionError` tell you?
5. How many pytest tests are required in the Week 6 takeaway?

**Answers:** (1) A change breaks previously working behavior. (2) A test automatically checks an expected result. (3) Stock exactly equal to 5. (4) An assertion's condition was false. (5) **2–3 simple tests**.

## Lesson recap

- Testing turns an expectation into a repeatable check.
- A single successful manual run does not prove every case works.
- Normal cases, boundaries, and error cases reveal different kinds of mistakes.
- Small, predictable functions are natural candidates for automated tests.
- The required Week 6 outcome is modest: **2–3 simple pytest tests**, alongside `.venv`, `requirements.txt`, and one environment variable.
- AI SDK integration, mocking, and live LLM calls are not part of the required work.

**Next lesson:** `02_Pytest_Introduction_and_Arrange_Act_Assert.md` shows how pytest discovers tests and how to structure them using **Arrange → Act → Assert**.
