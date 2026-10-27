# File Error Handling

## eCOMMart AI Squad | Week 4

> “Reliable programs plan for files that are missing, unreadable, or contain unexpected data.”

## What We Will Cover

1. Recognize common file-related exceptions.
2. Handle missing files and permission-related errors.
3. Handle invalid JSON and malformed input.
4. Use `try`, `except`, `else`, and `finally` appropriately.
5. Apply error handling to an eCOMMart data-loading workflow.

---

## 1. Why File Error Handling Matters

A file operation can fail for reasons outside the program's control. A file may not exist, a folder may be missing, the program may not have permission to read or write, or a data file may contain invalid content.

For eCOMMart, these problems could affect loading a product catalogue, reading application settings, or saving a sales report.

Error handling lets the program respond clearly instead of stopping with an unhandled exception. It does not mean hiding every error: handle expected problems and preserve enough information to diagnose unexpected ones.

## 2. Common File-Related Exceptions

| Exception | Typical cause |
|---|---|
| `FileNotFoundError` | The requested file does not exist |
| `PermissionError` | The process does not have the required permission |
| `IsADirectoryError` | A directory was supplied where a file was expected |
| `OSError` | A broader operating-system or file-system problem |
| `UnicodeDecodeError` | File bytes cannot be decoded using the chosen text encoding |
| `json.JSONDecodeError` | File content is not valid JSON |
| `ValueError` | A value cannot be converted or does not meet an expected condition |

The exception raised depends on the operation and the problem. For example, malformed JSON is different from a missing JSON file: the first file exists but cannot be parsed, while the second cannot be opened at all.

## 3. Handle a Missing File

Use `try` and `except` to handle a file that may not exist.

```python
try:
    with open("products.txt", "r", encoding="utf-8") as file:
        content = file.read()
except FileNotFoundError:
    print("Product file was not found.")
else:
    print("Product file loaded.")
```

Output if the file is missing:

```text
Product file was not found.
```

Output if the file exists and can be read:

```text
Product file loaded.
```

The `else` block runs only if the `try` block completes without raising an exception.

## 4. Handle Permission and Other Operating-System Errors

You can handle a more specific error when you know what to expect.

```python
try:
    with open("sales_report.txt", "w", encoding="utf-8") as file:
        file.write("eCOMMart sales report\n")
except PermissionError:
    print("Permission denied while saving the report.")
else:
    print("Report saved.")
```

Output when writing succeeds:

```text
Report saved.
```

Whether a permission error occurs depends on the environment and the destination. Do not try to create a permission error by changing permissions on a shared or important file. If you need to handle other file-system failures, `OSError` can be used as a broader fallback after more specific exceptions.

## 5. Handle Invalid JSON

A file can exist and still contain invalid JSON. Catch `json.JSONDecodeError` when parsing JSON data.

```python
import json

try:
    with open("config.json", "r", encoding="utf-8") as file:
        config = json.load(file)
except FileNotFoundError:
    print("Configuration file is missing.")
except json.JSONDecodeError:
    print("Configuration file contains invalid JSON.")
else:
    print("Configuration loaded.")
```

Possible output if the file exists but contains malformed JSON:

```text
Configuration file contains invalid JSON.
```

The order of the `except` clauses is intentional: each one handles a different expected problem. If the file is missing, the JSON parser is never reached.

## 6. Validate Data After Reading It

Successfully reading a file does not guarantee that its data is suitable for the application. For example, a product record might contain a price that is not a valid number.

```python
price_text = "unknown"

try:
    price = int(price_text)
except ValueError:
    print("Product price must be a whole number.")
else:
    print(f"Price loaded: ₹{price}")
```

Output:

```text
Product price must be a whole number.
```

This example handles conversion of a single value. When loading records from JSON or CSV, validate the required fields and types before using them in calculations.

## 7. Understand `finally`

The `finally` block runs whether the operation succeeds or raises an exception. It is often used for cleanup that must happen in either case.

```python
try:
    number = int("25")
    print(f"Quantity: {number}")
except ValueError:
    print("Quantity must be numeric.")
finally:
    print("Quantity check finished.")
```

Output:

```text
Quantity: 25
Quantity check finished.
```

For ordinary file operations, `with open(...)` is usually the simplest way to ensure a file is closed. You do not need to manually close a file opened by a `with` statement in a `finally` block.

## 8. Avoid Overly Broad Exception Handling

Catching every exception can conceal bugs.

Avoid using this pattern without a specific reason:

```python
try:
    # Perform an operation
    pass
except Exception:
    print("Something went wrong.")
```

A better approach is to catch the errors you expect and respond meaningfully.

```python
import json

try:
    with open("products.json", "r", encoding="utf-8") as file:
        products = json.load(file)
except FileNotFoundError:
    print("Create or provide products.json before running the program.")
except json.JSONDecodeError:
    print("Fix the JSON format in products.json.")
else:
    print(f"Loaded {len(products)} products.")
```

This example assumes the valid JSON data is a list. If the file contains a different JSON structure, additional validation is needed.

## 9. Worked Example: Load a Product Catalogue Safely

Create `products.json` containing a list of product dictionaries:

```json
[
    {"product_id": "P101", "name": "Wireless Mouse", "price": 799},
    {"product_id": "P102", "name": "Keyboard", "price": 1299}
]
```

Then load the data and validate the product prices:

```python
import json

try:
    with open("products.json", "r", encoding="utf-8") as file:
        products = json.load(file)
except FileNotFoundError:
    print("Product catalogue is missing.")
except json.JSONDecodeError:
    print("Product catalogue contains invalid JSON.")
else:
    valid_products = []

    for product in products:
        try:
            price = int(product["price"])
        except (KeyError, TypeError, ValueError):
            print("Skipped a product with an invalid price.")
            continue

        valid_products.append(product)
        print(f'{product["name"]}: ₹{price}')

    print(f"Valid products loaded: {len(valid_products)}")
```

Output for the sample file:

```text
Wireless Mouse: ₹799
Keyboard: ₹1299
Valid products loaded: 2
```

This example uses two layers of validation:
- The outer `try` block handles problems opening or parsing the file.
- The inner `try` block handles a missing or invalid `price` value in an individual product.

The example assumes the top-level JSON value is a list and that each item is intended to be a dictionary. A production application should validate the overall structure too.

## 10. Practice Tasks

Complete the tasks in order. Each task builds on the ideas introduced in this lesson.

### Task 1 — Handle a Missing File

Try to open `missing_report.txt` for reading. Catch `FileNotFoundError` and print the message below.

Expected output when the file is absent:

```text
Report file not found.
```

### Task 2 — Handle Invalid JSON

Use `json.loads()` to parse this invalid string:

```python
invalid_json = '{"store": "eCOMMart",}'
```

Catch `json.JSONDecodeError` and print the message below.

Expected output:

```text
Invalid JSON data.
```

### Task 3 — Validate a Product Price

Set `price_text = "free"` and attempt to convert it to an integer. Catch `ValueError` and print the message below.

Expected output:

```text
Price must be numeric.
```

## Summary

| Technique | Purpose |
|---|---|
| `try` | Run code that may raise an exception |
| `except` | Handle a specified exception |
| `else` | Run when the `try` block succeeds |
| `finally` | Run cleanup or final steps regardless of success or failure |
| `FileNotFoundError` | Handle a missing file |
| `PermissionError` | Handle a permission-related failure |
| `json.JSONDecodeError` | Handle invalid JSON |
| `ValueError` | Handle invalid value conversion |
| `with open(...)` | Ensure the file is closed after the block |

Good error handling distinguishes between missing files, invalid content, and invalid field values. Catch expected exceptions, give useful messages, and validate data before relying on it.

*Next: `01_Product_Class_From_Scratch.md`*
