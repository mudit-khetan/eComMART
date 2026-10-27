# Config-Driven Application

## eCOMMart AI Squad | Week 4

> “Separate changeable settings from program logic so an application can adapt without rewriting its workflow.”

## What We Will Cover

1. Review how a JSON configuration controls application settings.
2. Load settings and product data from files.
3. Use configuration values to control a small application.
4. Validate configuration and handle expected file errors.
5. Build an eCOMMart report workflow from configuration and product data.

---

## 1. What Does Config-Driven Mean?

A config-driven application reads changeable settings from a configuration file rather than hard-coding every setting in the program.

For eCOMMart, the configuration might specify:
- The store name.
- The minimum stock quantity that triggers a low-stock warning.
- The paths to the product data and report output files.
- Whether the application should include a report heading.

Example project structure:

```text
ecommart/
├── app.py
├── config.json
├── data/
│   └── products.json
└── reports/
    └── low_stock.txt
```

The example in this lesson uses JSON files and standard Python libraries. The paths shown are relative to the current working directory.

## 2. Create the Configuration File

Create `config.json` with this content:

```json
{
    "store_name": "eCOMMart",
    "low_stock_threshold": 10,
    "products_file": "data/products.json",
    "report_file": "reports/low_stock.txt",
    "include_heading": true
}
```

This configuration means that products with fewer than ten units in stock should appear in the report. The data and report paths can be changed without editing the main report logic.

## 3. Prepare the Product Data

Create `data/products.json` with a list of product records:

```json
[
    {
        "product_id": "P101",
        "name": "Wireless Mouse",
        "price": 799,
        "quantity": 25
    },
    {
        "product_id": "P102",
        "name": "Keyboard",
        "price": 1299,
        "quantity": 6
    },
    {
        "product_id": "P103",
        "name": "Laptop Stand",
        "price": 999,
        "quantity": 4
    }
]
```

Each record stores a product identifier, name, price, and quantity. The application will read this list and select products that fall below the configured stock threshold.

## 4. Load and Validate the Configuration

Start by loading the configuration file and checking the settings the application requires.

```python
import json

with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

required_keys = {
    "store_name",
    "low_stock_threshold",
    "products_file",
    "report_file",
    "include_heading"
}

missing_keys = required_keys - config.keys()

if missing_keys:
    raise ValueError(f"Missing configuration keys: {', '.join(sorted(missing_keys))}")

if not isinstance(config["low_stock_threshold"], int):
    raise ValueError("low_stock_threshold must be an integer.")

if config["low_stock_threshold"] < 0:
    raise ValueError("low_stock_threshold cannot be negative.")

print("Configuration loaded.")
```

Output:

```text
Configuration loaded.
```

This validation checks required keys and the threshold's basic type and range. For stricter validation, check the types of all settings, including the path strings and the `include_heading` Boolean.

## 5. Use the Settings to Filter Products

The filtering logic should use the configured threshold rather than a fixed number.

```python
import json

with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

with open(config["products_file"], "r", encoding="utf-8") as file:
    products = json.load(file)

threshold = config["low_stock_threshold"]

low_stock_products = [
    product for product in products
    if product["quantity"] < threshold
]

print(f'Products below threshold: {len(low_stock_products)}')

for product in low_stock_products:
    print(f'{product["name"]}: {product["quantity"]} remaining')
```

Output:

```text
Products below threshold: 2
Keyboard: 6 remaining
Laptop Stand: 4 remaining
```

If you change `low_stock_threshold` in `config.json`, the program uses the new value on the next run. The filtering logic does not need to change.

## 6. Build the Report Content

Prepare the report as a string before saving it. This separates the content-generation step from the file-writing step.

```python
store_name = config["store_name"]
include_heading = config["include_heading"]

lines = []

if include_heading:
    lines.append(f"{store_name} Low-Stock Report")

for product in low_stock_products:
    lines.append(
        f'{product["name"]}: {product["quantity"]} remaining'
    )

report_text = "\n".join(lines) + "\n"

print(report_text, end="")
```

Output:

```text
eCOMMart Low-Stock Report
Keyboard: 6 remaining
Laptop Stand: 4 remaining
```

The heading is included only when `include_heading` is `true` in the JSON configuration. If the setting is `false`, the product lines are still included.

## 7. Save the Report to the Configured Path

The report path comes from `config.json`. Create its parent directory if necessary before opening the file.

```python
import os

report_path = config["report_file"]
report_folder = os.path.dirname(report_path)

if report_folder:
    os.makedirs(report_folder, exist_ok=True)

with open(report_path, "w", encoding="utf-8") as file:
    file.write(report_text)

print(f"Report saved to {report_path}")
```

Example output:

```text
Report saved to reports/low_stock.txt
```

The path shown is an example for macOS or Linux; separators may differ on Windows if the path is built using platform-specific components. The configured path is interpreted relative to the current working directory.

## 8. Complete Worked Example

The following script combines configuration loading, product loading, filtering, report generation, and saving. It assumes that `config.json` and `data/products.json` have been created as shown above.

```python
import json
import os


def load_json(path):
    """Load and return JSON data from a file."""
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def build_low_stock_report(config, products):
    """Return a text report for products below the configured threshold."""
    threshold = config["low_stock_threshold"]
    low_stock_products = [
        product for product in products
        if product["quantity"] < threshold
    ]

    lines = []
    if config["include_heading"]:
        lines.append(f'{config["store_name"]} Low-Stock Report')

    for product in low_stock_products:
        lines.append(
            f'{product["name"]}: {product["quantity"]} remaining'
        )

    report_text = "\n".join(lines) + "\n"
    return low_stock_products, report_text


def save_report(path, report_text):
    """Create the parent directory if needed and save the report."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        file.write(report_text)


config = load_json("config.json")
products = load_json(config["products_file"])

low_stock_products, report_text = build_low_stock_report(config, products)
save_report(config["report_file"], report_text)

print(f"Products below threshold: {len(low_stock_products)}")
print(f'Report saved to {config["report_file"]}')
```

Output:

```text
Products below threshold: 2
Report saved to reports/low_stock.txt
```

The saved report contains:

```text
eCOMMart Low-Stock Report
Keyboard: 6 remaining
Laptop Stand: 4 remaining
```

The helper functions give each part of the workflow a clear responsibility:
- `load_json()` reads structured data.
- `build_low_stock_report()` filters products and prepares the report text.
- `save_report()` creates the destination folder and writes the output.

## 9. Handle Expected File Errors

A configuration-driven workflow depends on external files, so expected errors should be handled deliberately.

```python
import json

try:
    with open("config.json", "r", encoding="utf-8") as file:
        config = json.load(file)
except FileNotFoundError:
    print("Configuration file not found.")
except json.JSONDecodeError:
    print("Configuration file contains invalid JSON.")
else:
    print("Configuration file is ready.")
```

Possible output if the configuration file is missing:

```text
Configuration file not found.
```

This small example handles two common cases. In the complete application, you should also consider a missing product file, invalid product data, and errors while saving the report. Avoid catching every exception without a clear recovery plan.

## 10. Practice Tasks

Complete the tasks in order. Each task builds on the ideas introduced in this lesson.

### Task 1 — Use a Configured Threshold

Create a configuration dictionary with `low_stock_threshold` set to `5`. Given these products:

```python
products = [
    {"name": "Mouse", "quantity": 8},
    {"name": "Keyboard", "quantity": 3},
    {"name": "Laptop Stand", "quantity": 2}
]
```

Filter products using the threshold from the configuration and print the names of products below it.

Expected output:

```text
Keyboard
Laptop Stand
```

### Task 2 — Save a Configured Report

Create a configuration dictionary with `report_file` set to `"reports/task_report.txt"`. Create the parent directory if needed, save the text `Weekly report ready.` to that path, and print the success message.

Expected output:

```text
Report saved.
```

### Task 3 — Build a Mini Config-Driven Workflow

Create a JSON configuration file with a store name and a low-stock threshold. Load it, filter a list of product dictionaries, and save a report that includes the store name and products below the threshold.

For sample data where `Keyboard` has a quantity of `3` and the threshold is `5`, the report should include:

```text
eCOMMart Low-Stock Report
Keyboard: 3 remaining
```

## Summary

| Concept | Purpose |
|---|---|
| JSON configuration | Stores changeable application settings |
| Configured threshold | Controls filtering without changing the algorithm |
| `json.load()` | Loads configuration and product records |
| Helper functions | Separate loading, report creation, and saving responsibilities |
| `os.makedirs()` | Ensures the report directory exists |
| `os.path.dirname()` | Gets the directory part of the report path |
| File error handling | Provides clear responses to missing or malformed files |

A config-driven application keeps settings separate from its core logic. This makes small eCOMMart workflows easier to adjust, test, and maintain.

*Next: `05_Mini_OOP_Agent_Tool.md`*
