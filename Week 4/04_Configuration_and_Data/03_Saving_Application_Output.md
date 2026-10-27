# Saving Application Output

## eCOMMart AI Squad | Week 4

> “A program becomes more useful when it can save its results for the next run.”

## What We Will Cover

1. Understand the difference between displaying and saving output.
2. Save text reports to a file.
3. Save structured output as JSON.
4. Create output folders and build file paths.
5. Handle common output-saving errors.

---

## 1. Displaying Output vs Saving Output

`print()` displays information in the terminal. When the program ends, that terminal output is not automatically saved as a file.

For example:

```python
products_sold = 12
print(f"Products sold today: {products_sold}")
```

Output:

```text
Products sold today: 12
```

To keep a result for later, write it to a file. eCOMMart might save a daily sales summary, an order confirmation, or a list of products that need restocking.

## 2. Save a Text Report

Use `open()` in write mode (`"w"`) to create a text file or replace its existing content. The `write()` method writes a string to the file.

```python
report = "eCOMMart Daily Report\nProducts sold: 12\n"

with open("daily_report.txt", "w", encoding="utf-8") as file:
    file.write(report)

print("Report saved.")
```

Output:

```text
Report saved.
```

The file `daily_report.txt` contains:

```text
eCOMMart Daily Report
Products sold: 12
```

The `\n` characters create line breaks in the saved file. `write()` does not automatically add a newline, so include one where needed.

**Important:** Opening a file with `"w"` replaces its existing contents. Use this mode only when creating a new file or intentionally replacing the previous report.

## 3. Build a Report from Variables

Instead of hard-coding all report content, build it from the values calculated by your application.

```python
store_name = "eCOMMart"
orders_processed = 28
sales_total = 45670

report = (
    f"{store_name} Daily Sales Report\n"
    f"Orders processed: {orders_processed}\n"
    f"Total sales: ₹{sales_total}\n"
)

with open("sales_report.txt", "w", encoding="utf-8") as file:
    file.write(report)

print("Sales report saved.")
```

Output:

```text
Sales report saved.
```

The resulting file contains:

```text
eCOMMart Daily Sales Report
Orders processed: 28
Total sales: ₹45670
```

Parentheses allow adjacent f-strings to be combined into one string. This makes a multi-line report easier to read in the source code.

## 4. Append to an Existing Log

Use append mode (`"a"`) when new output should be added after existing content rather than replacing it.

```python
with open("activity.log", "a", encoding="utf-8") as file:
    file.write("Order ORD501 processed\n")

print("Activity recorded.")
```

Output:

```text
Activity recorded.
```

Run the code again and another line will be added. Append mode creates the file if it does not already exist.

Use append mode for logs or records that should accumulate. If the file is a report that must contain only the latest results, write mode may be more appropriate.

## 5. Save Structured Output as JSON

Text reports are readable by people, but structured data is often easier for another program to process. Use JSON when you want to preserve dictionaries, lists, numbers, and Boolean values.

```python
import json

sales_summary = {
    "store": "eCOMMart",
    "orders_processed": 28,
    "sales_total": 45670,
    "currency": "INR"
}

with open("sales_summary.json", "w", encoding="utf-8") as file:
    json.dump(sales_summary, file, indent=4)

print("Sales data saved.")
```

Output:

```text
Sales data saved.
```

The file `sales_summary.json` contains:

```json
{
    "store": "eCOMMart",
    "orders_processed": 28,
    "sales_total": 45670,
    "currency": "INR"
}
```

`json.dump()` converts the Python data into JSON and writes it to the file. The `indent=4` argument makes the saved JSON easier to inspect.

## 6. Save Output to a Specific Folder

When an application produces several reports, keeping them in a dedicated folder makes the project easier to manage.

Use `os.makedirs()` to ensure the output directory exists and `os.path.join()` to build the path.

```python
import os

output_folder = "reports"
os.makedirs(output_folder, exist_ok=True)

report_path = os.path.join(output_folder, "daily_report.txt")

with open(report_path, "w", encoding="utf-8") as file:
    file.write("eCOMMart Daily Report\nOrders processed: 28\n")

print(f"Report saved to {report_path}")
```

Example output on macOS or Linux:

```text
Report saved to reports/daily_report.txt
```

On Windows, the displayed path may use backslashes instead. The `os.path.join()` function handles the platform-specific separator.

The path is relative to the current working directory. Make sure you run the program from the intended project location.

## 7. Handle Output-Saving Errors

Saving a file can fail, for example, if the program does not have permission to write to the destination.

```python
try:
    with open("daily_report.txt", "w", encoding="utf-8") as file:
        file.write("eCOMMart report\n")
except OSError:
    print("Could not save the report.")
else:
    print("Report saved successfully.")
```

Output when the write succeeds:

```text
Report saved successfully.
```

`OSError` covers many operating-system-related file errors, including some permission and path problems. In a real application, you can log the original error or show a more specific message when appropriate.

If you are saving to a subdirectory, create it first. Otherwise, opening a file inside a missing directory will normally fail.

## 8. Worked Example: Save a Low-Stock Report

This example creates a report listing products with fewer than ten items in stock.

```python
import os

products = [
    {"name": "Wireless Mouse", "quantity": 25},
    {"name": "Keyboard", "quantity": 6},
    {"name": "Laptop Stand", "quantity": 4}
]

low_stock = [
    product for product in products
    if product["quantity"] < 10
]

lines = ["eCOMMart Low-Stock Report"]

for product in low_stock:
    lines.append(f'{product["name"]}: {product["quantity"]} remaining')

report_text = "\n".join(lines) + "\n"

os.makedirs("reports", exist_ok=True)
report_path = os.path.join("reports", "low_stock.txt")

with open(report_path, "w", encoding="utf-8") as file:
    file.write(report_text)

print(f"Low-stock products: {len(low_stock)}")
print("Report saved.")
```

Output:

```text
Low-stock products: 2
Report saved.
```

The file `reports/low_stock.txt` contains:

```text
eCOMMart Low-Stock Report
Keyboard: 6 remaining
Laptop Stand: 4 remaining
```

This example combines lists, dictionaries, a list comprehension, string formatting, directory creation, and file writing.

## 9. Practice Tasks

Complete the tasks in order. Each task builds on the ideas introduced in this lesson.

### Task 1 — Save a Summary

Create a string containing these two lines:

```text
eCOMMart Order Summary
Orders processed: 5
```

Write it to `order_summary.txt` and print `Summary saved.`

Expected output:

```text
Summary saved.
```

### Task 2 — Save Structured Data

Create this dictionary:

```python
report = {
    "report_name": "weekly_sales",
    "orders": 42,
    "total_sales": 68500
}
```

Use `json.dump()` to save it to `weekly_sales.json` with `indent=4`. Print `JSON report saved.` after writing.

Expected output:

```text
JSON report saved.
```

### Task 3 — Create a Report Folder and Save a File

Use `os.makedirs()` with `exist_ok=True` to create a folder named `reports`. Build the path to `stock_summary.txt` with `os.path.join()`. Write the text `Products needing restock: 3` to the file and print the saved path.

Example output on macOS or Linux:

```text
Saved: reports/stock_summary.txt
```

On Windows, the path separator may differ.

## Summary

| Tool or mode | Purpose |
|---|---|
| `print()` | Display output in the terminal |
| `file.write()` | Write text to a file |
| Mode `"w"` | Create or replace file contents |
| Mode `"a"` | Append content to a file |
| `json.dump()` | Save structured Python data as JSON |
| `os.makedirs()` | Create output directories |
| `os.path.join()` | Build a platform-appropriate path |
| `OSError` | Handle many file-system-related failures |

Saving application output lets eCOMMart keep reports and structured data beyond a single program run. Choose text, JSON, or another format based on how the saved information will be used.

*Next: `04_File_Error_Handling.md`*
