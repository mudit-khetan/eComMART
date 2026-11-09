# Modules, Packages, and `import`

## Lesson purpose

In Week 5, you built the eComMART product catalog in one Python file, `05_Product_Catalog_App.py`. A single file can be a good way to learn: you can see everything in one place. But as a program grows, finding a function, changing one feature, or testing it without starting the whole application becomes harder.

This week, the instructor will build a **separate, smaller eComMART low-stock notifier**. We will use that small example to understand **modules**, **packages**, and **imports** before organizing a larger project. **Do not restructure your Week 5 catalog yet**; that is the independent challenge later in Week 6.

**Core for Week 6:** move reusable Python functions into a second file and import them. **Optional/stretch:** learn how a multi-file package works. You need no real API key, signup, or live AI call.

## Learning objectives

By the end of this lesson, you will be able to:

- Explain what a module, package, and `import` statement mean.
- Move a function into another `.py` file and call it from a main program.
- Recognize the difference between `import module` and `from module import function`.
- Understand why a module should not start a whole application when imported.
- Identify typical import errors and check the folder you are running from.
- Describe why small, reusable functions are useful for future agent tools.

## 1. The eComMART problem: too much in one file

Imagine the eComMART team wants a tool that checks whether an item is running low and prints a message. A first version might look like this:

```python
# one_file_alert.py

def is_low_stock(stock, threshold):
    return stock < threshold


def make_alert(product_name, stock, threshold):
    if is_low_stock(stock, threshold):
        return f"LOW STOCK: {product_name} has {stock} units left."
    return f"Stock OK: {product_name} has {stock} units."


print(make_alert("Wireless Mouse", 3, 5))
```

**Expected output:**

```text
LOW STOCK: Wireless Mouse has 3 units left.
```

This works. But suppose someone wants to **reuse** `make_alert()` in a different program or test it with different stock values. Keeping the reusable functions in their own file makes that easier.

## 2. Three terms you need

| Term | Plain-language meaning | Example |
|---|---|---|
| **Module** | A Python file whose code can be used from another Python file | `stock_alert.py` |
| **Package** | A folder that groups related modules, commonly with an `__init__.py` file | A future `catalog/` folder containing `products.py` |
| **Import** | A statement telling Python to make names from another module available | `from stock_alert import make_alert` |

Think of a **module** as one labeled toolbox. A **package** is a cabinet holding several labeled toolboxes. An **import** lets your code take a tool from the correct place. You already imported Python's built-in modules such as `sqlite3` in Week 5. This lesson shows how to import a module **you write yourself**.

**A distinction:** a Python package in your own project is not the same as an installable third-party distribution such as `pytest`. Both can provide importable code, but a local module you create does not need `pip install` merely to be imported from the same folder.

## 3. Step 1 — Make a tiny practice project

Create a folder named `week6_practice` anywhere convenient, then create `module_practice` inside it. Open `module_practice` in your editor. This first exercise uses only Python's built-in features, so **no virtual environment or package installation is needed yet**. You will learn virtual environments in Section 03.

```text
week6_practice/
└── module_practice/
    ├── stock_alert.py
    └── main.py
```

No new package installation is required for this exercise. Both files use ordinary Python features.

### Create `stock_alert.py`

```python
# stock_alert.py

def is_low_stock(stock, threshold):
    """Return True when the stock is below the alert threshold."""
    return stock < threshold


def make_alert(product_name, stock, threshold):
    """Build a message; do not print it inside this function."""
    if is_low_stock(stock, threshold):
        return f"LOW STOCK: {product_name} has {stock} units left."
    return f"Stock OK: {product_name} has {stock} units."
```

**Notice:** there is no `input()` or `print()` inside these reusable functions. A function **returns** a result, so another program or a future test can check that result.

### Create `main.py`

```python
# main.py
from stock_alert import make_alert

message = make_alert("Wireless Mouse", 3, 5)
print(message)
```

Open the terminal **inside `module_practice`** and run:

```bash
python main.py
```

**Expected output:**

```text
LOW STOCK: Wireless Mouse has 3 units left.
```

**What happened?** Python loaded `stock_alert.py`, found `make_alert`, and made that function available in `main.py`. Your main program did not need a second copy of the alert logic.

## 4. Step 2 — Understand two import styles

Both styles work when `stock_alert.py` and `main.py` are in the same folder.

**Style A — import the module:**

```python
import stock_alert

print(stock_alert.is_low_stock(3, 5))
```

Expected output: `True`. The name `stock_alert.` shows where the function comes from.

**Style B — import a specific function:**

```python
from stock_alert import is_low_stock

print(is_low_stock(5, 5))
```

Expected output: `False`. A stock level **equal to** the threshold is *not* below it; the rule is `<`, not `<=`.

Use one style consistently in a small example. You do not need both at once. Avoid `from stock_alert import *` in this course because it becomes difficult to see which file supplied a name.

## 5. Step 3 — Why import-time behavior matters

When Python imports a module for the first time in a running program, it executes statements at the top level of that module. **Function definitions are created; function bodies do not run until called.** But a top-level `print()` or `input()` *will* run during the import.

For example, this would be a poor pattern for a reusable module:

```python
# Avoid placing this at the bottom of stock_alert.py
print(make_alert("Wireless Mouse", 3, 5))
```

If `main.py` imports `stock_alert`, that extra print executes even when the caller did not request it. In the reusable `stock_alert.py` above, we leave out all top-level application actions.

If you want a script that can be run directly **and** imported safely, you may see this pattern:

```python
if __name__ == "__main__":
    print(make_alert("Wireless Mouse", 3, 5))
```

`__name__` is a special Python variable. When you run the file directly, its value is `"__main__"`. When another file imports it, the value is the module's name. The block therefore runs only on direct execution. For our mini-project, we keep the entry point in `main.py` instead, which is even easier to follow.

## 6. A first look at packages

Later, if a project has several related modules, you can group them in a folder:

```text
module_practice/
├── main.py
└── alerts/
    ├── __init__.py
    └── stock_alert.py
```

The `__init__.py` file can be empty. It marks `alerts` as a regular Python package and makes the structure clear to beginners. (Python also supports some packages without this file; you do not need that variation this week.)

If you **move** `stock_alert.py` into `alerts/`, change the import in `main.py` to:

```python
from alerts.stock_alert import make_alert
```

Run `python main.py` from `module_practice` again. Its output should remain the same. The dot in `alerts.stock_alert` means “find `stock_alert.py` inside the `alerts` package.”

**Core exercise:** the two-file version from Step 1 is enough. **Optional/stretch:** try the `alerts/` package move after you have a working two-file version. Do not keep both copies of `stock_alert.py`; that makes it unclear which one Python imported.

## 7. Why this prepares you for agentic AI

In a later AI application, a language model may ask the program to perform an action such as “check an item's stock.” The Python function that performs that action is often called an **agent tool**. You do not need an AI model to write or test the function itself.

The `is_low_stock()` function is a good starting point: it accepts known inputs and gives the same answer for the same inputs. We call this **deterministic** behavior. In Week 6 you will test this ordinary function before considering any optional AI connection.

**No Anthropic SDK, account, API key, network call, or paid usage is needed for this lesson.**

## 8. Guided practice — try it yourself

Keep the working **two-file** version for this practice.

1. In `main.py`, call `make_alert("USB-C Cable", 12, 5)` and print the result.
2. Change the stock value from `12` to `2`. Run the program again.
3. Change `main.py` to use `import stock_alert` and call `stock_alert.make_alert(...)`.
4. **Predict before running:** what will `is_low_stock(5, 5)` return? Confirm with a print statement.
5. **Optional/stretch:** move the module into an `alerts` package using Section 6 and update the import.

**Expected checks:**

| Call | Expected result |
|---|---|
| `make_alert("USB-C Cable", 12, 5)` | `Stock OK: USB-C Cable has 12 units.` |
| `make_alert("USB-C Cable", 2, 5)` | `LOW STOCK: USB-C Cable has 2 units left.` |
| `is_low_stock(5, 5)` | `False` |

Before moving on, explain aloud why `main.py` does the printing while `stock_alert.py` returns text.

## 9. Common mistakes and troubleshooting

| What you see | Likely reason | What to check |
|---|---|---|
| `ModuleNotFoundError: No module named 'stock_alert'` | File is not in the expected folder, or its name differs | Check spelling and make sure `main.py` and `stock_alert.py` are together in the core version |
| `ImportError: cannot import name 'make_alert'` | The requested function is missing or misspelled | Compare the `def make_alert(...)` line and import statement |
| An unexpected line prints during import | Code runs at the module's top level | Move the print into `main.py`, or use the `__main__` guard |
| `NameError: name 'make_alert' is not defined` | You used `import stock_alert` but called `make_alert()` directly | Call `stock_alert.make_alert()` or use `from stock_alert import make_alert` |
| Output seems to use old code | A file was not saved or you edited the wrong copy | Save all files; look for duplicate `stock_alert.py` files |

**Do not install a package with pip to fix a missing local file.** Check your filenames and project folder first.

## 10. Quick knowledge check

1. What is the difference between a module and a package?
2. Which file should hold reusable logic: `stock_alert.py` or `main.py`?
3. What is the difference between `import stock_alert` and `from stock_alert import make_alert`?
4. Why is it better for `make_alert()` to **return** a message rather than always print it?

**Self-check answers:** (1) A module is a Python file; a package groups modules. (2) `stock_alert.py`. (3) The first uses the module prefix, the second imports the named function. (4) Returning a value lets other code reuse and test it without depending on terminal output.

## Lesson recap

- A module is a `.py` file; a package groups related modules.
- Imports allow you to reuse functions without copy-pasting them.
- Keep application startup in a clear entry-point file such as `main.py`.
- Returning values from small functions makes them easier to test and reuse as future agent tools.

**Next lesson:** `02_Basic_Project_Structure.md` shows where code, configuration, database files, and tests belong in an understandable eComMART project.
