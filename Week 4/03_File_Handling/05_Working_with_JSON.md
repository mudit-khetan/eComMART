# Working with JSON

## eCOMMart AI Squad | Week 4

> “A useful application can save its data in a format that other tools can read too.”

## What We Will Cover

1. Understand JSON and where it is useful.
2. Read JSON data from a file using Python.
3. Write Python data to a JSON file.
4. Work with nested JSON objects and lists.
5. Handle common JSON-related errors.

---

## 1. What Is JSON?

JSON stands for **JavaScript Object Notation**. It is a text format commonly used to store and exchange structured data. Python can convert between JSON text and familiar Python data types.

For eCOMMart, JSON can store application settings, product details, or a customer's order.

Example JSON:

```json
{
    "product_id": "P101",
    "name": "Wireless Mouse",
    "price": 799,
    "in_stock": true,
    "tags": ["accessories", "electronics"]
}
```

JSON uses:
- Objects, written with `{}` and key-value pairs.
- Arrays, written with `[]`.
- Strings in double quotes.
- Numbers, booleans (`true` and `false`), and `null`.

Python's corresponding values use `dict`, `list`, `str`, `int` or `float`, `True` or `False`, and `None`.

| JSON | Python |
|---|---|
| Object `{}` | Dictionary `dict` |
| Array `[]` | List `list` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

JSON is a data format, not a Python file. A `.json` file normally contains JSON text, not Python statements.

## 2. Convert Between JSON and Python

Python's built-in `json` module provides functions for conversion.

```python
import json

product = {
    "product_id": "P101",
    "name": "Wireless Mouse",
    "price": 799,
    "in_stock": True
}

json_text = json.dumps(product, indent=4)
print(json_text)
```

Output:

```json
{
    "product_id": "P101",
    "name": "Wireless Mouse",
    "price": 799,
    "in_stock": true
}
```

`json.dumps()` converts a Python object into a JSON-formatted string. The `indent=4` argument makes the output easier to read.

To convert a JSON string back into Python data, use `json.loads()`:

```python
import json

json_text = '{"name": "Wireless Mouse", "price": 799}'
product = json.loads(json_text)

print(product["name"])
print(product["price"])
print(type(product))
```

Output:

```text
Wireless Mouse
799
<class 'dict'>
```

Remember:
- `dumps()` and `loads()` work with strings.
- `dump()` and `load()` work with file objects.

## 3. Read JSON from a File

Imagine that the project contains a file named `product.json` with this content:

```json
{
    "product_id": "P101",
    "name": "Wireless Mouse",
    "price": 799,
    "in_stock": true,
    "tags": ["accessories", "electronics"]
}
```

Use `json.load()` to read and parse the file.

```python
import json

with open("product.json", "r", encoding="utf-8") as file:
    product = json.load(file)

print(product["name"])
print(product["price"])
print(product["tags"])
```

Output:

```text
Wireless Mouse
799
['accessories', 'electronics']
```

The `with` statement closes the file automatically. The `encoding="utf-8"` argument makes the expected text encoding explicit.

Once loaded, `product` is a Python dictionary. You can access its values using dictionary keys, loop over its lists, and pass the data to functions.

### Access Nested Data

A JSON object can contain another object or an array.

Suppose `order.json` contains:

```json
{
    "order_id": "ORD501",
    "customer": {
        "name": "Aarav",
        "city": "Agra"
    },
    "items": [
        {"name": "Wireless Mouse", "quantity": 1},
        {"name": "Keyboard", "quantity": 2}
    ]
}
```

```python
import json

with open("order.json", "r", encoding="utf-8") as file:
    order = json.load(file)

print(order["customer"]["city"])
print(order["items"][1]["name"])
print(order["items"][1]["quantity"])
```

Output:

```text
Agra
Keyboard
2
```

Use a dictionary key to access an object field and an index to access an item in a list.

## 4. Write Python Data to a JSON File

Use `json.dump()` to write a Python dictionary or list to a file.

```python
import json

product = {
    "product_id": "P205",
    "name": "USB-C Hub",
    "price": 1499,
    "in_stock": True
}

with open("new_product.json", "w", encoding="utf-8") as file:
    json.dump(product, file, indent=4)

print("Product data saved.")
```

Output:

```text
Product data saved.
```

The file `new_product.json` will contain:

```json
{
    "product_id": "P205",
    "name": "USB-C Hub",
    "price": 1499,
    "in_stock": true
}
```

**Important:** Opening a file with mode `"w"` creates the file if it does not exist and replaces its existing content if it does. Use it when replacing the stored JSON is intended.

### Save a List of Products

A list of dictionaries is a useful structure for a small product catalogue.

```python
import json

products = [
    {"product_id": "P101", "name": "Wireless Mouse", "price": 799},
    {"product_id": "P102", "name": "Keyboard", "price": 1299},
    {"product_id": "P103", "name": "Laptop Stand", "price": 999}
]

with open("products.json", "w", encoding="utf-8") as file:
    json.dump(products, file, indent=4)

print(f"Saved {len(products)} products.")
```

Output:

```text
Saved 3 products.
```

## 5. Update Data and Save It Again

A common workflow is to load JSON, modify the Python data, and save the updated data.

```python
import json

with open("product.json", "r", encoding="utf-8") as file:
    product = json.load(file)

product["price"] = 749
product["in_stock"] = False

with open("product.json", "w", encoding="utf-8") as file:
    json.dump(product, file, indent=4)

print("Product updated.")
```

Output:

```text
Product updated.
```

This example overwrites `product.json` with the updated values. In a real application, make sure you are editing the intended file and that overwriting it is acceptable.

## 6. Handle JSON Errors

Two common problems are malformed JSON and a missing file.

### Invalid JSON

The JSON text below is invalid because the property name is not enclosed in double quotes:

```json
{
    name: "Wireless Mouse"
}
```

Parsing invalid JSON raises `json.JSONDecodeError`.

```python
import json

invalid_text = '{"name": "Wireless Mouse",}'

try:
    product = json.loads(invalid_text)
except json.JSONDecodeError as error:
    print("Could not read JSON data.")
    print(type(error).__name__)
```

Output:

```text
Could not read JSON data.
JSONDecodeError
```

### Missing File

Opening a file that does not exist raises `FileNotFoundError`.

```python
import json

try:
    with open("missing_product.json", "r", encoding="utf-8") as file:
        product = json.load(file)
except FileNotFoundError:
    print("Product data file was not found.")
```

Output:

```text
Product data file was not found.
```

Handle the errors you expect and provide a useful message. Avoid catching every possible exception without a reason, because that can hide unrelated bugs.

## 7. Worked Example: Load a Product Catalogue

This example reads a JSON list and prints each product's name and price. Create `products.json` with the sample data before running the script.

```json
[
    {"product_id": "P101", "name": "Wireless Mouse", "price": 799},
    {"product_id": "P102", "name": "Keyboard", "price": 1299},
    {"product_id": "P103", "name": "Laptop Stand", "price": 999}
]
```

Python script:

```python
import json

with open("products.json", "r", encoding="utf-8") as file:
    products = json.load(file)

for product in products:
    print(f'{product["name"]}: ₹{product["price"]}')
```

Output:

```text
Wireless Mouse: ₹799
Keyboard: ₹1299
Laptop Stand: ₹999
```

This combines file handling, JSON parsing, lists, dictionaries, and a loop.

## 8. Practice Tasks

Complete the tasks in order. Each task builds on the ideas introduced in this lesson.

### Task 1 — Save a Product

Create a dictionary with:
- `product_id`: `"P301"`
- `name`: `"Phone Stand"`
- `price`: `399`
- `in_stock`: `True`

Write it to `phone_stand.json` using `json.dump()` and `indent=4`. Print `Product saved.` after writing.

Expected output:

```text
Product saved.
```

### Task 2 — Read and Display a Catalogue

Create a file named `catalogue.json` containing a list of two products:

```json
[
    {"name": "Keyboard", "price": 1299},
    {"name": "USB-C Hub", "price": 1499}
]
```

Read the file and print each product in this format:

```text
Keyboard costs ₹1299
USB-C Hub costs ₹1499
```

### Task 3 — Update a Product Safely

Create `stock.json` with this content:

```json
{
    "product_id": "P401",
    "name": "Laptop Stand",
    "quantity": 12
}
```

Load the file, change `quantity` to `9`, and write the updated dictionary back to the same file with indentation. Then load it again and print the saved quantity.

Expected output:

```text
Saved quantity: 9
```

## Summary

| Concept | Use |
|---|---|
| `json.dumps()` | Convert a Python object to a JSON string |
| `json.loads()` | Parse a JSON string into Python data |
| `json.dump()` | Write Python data to a JSON file |
| `json.load()` | Read and parse JSON from a file |
| `indent=4` | Format JSON for readability |
| `json.JSONDecodeError` | Handle invalid JSON text |
| `FileNotFoundError` | Handle a missing file |

JSON makes structured application data easy to save and reload. For eCOMMart, it can hold product catalogues, order details, and simple configuration data.

*Next: `01_File_Paths_and_os_path.md`*