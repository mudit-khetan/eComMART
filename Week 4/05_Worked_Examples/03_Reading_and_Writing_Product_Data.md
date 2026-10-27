# Reading and Writing Product Data

## eCOMMart AI Squad | Week 4

> “An object is useful during a program run; saved data lets the application restore that information later.”

## What We Will Cover

1. Convert product objects into data that can be saved.
2. Write product records to a JSON file.
3. Load JSON records and rebuild product objects.
4. Validate input data before creating objects.
5. Build a small save-and-load workflow for an eCOMMart catalogue.

---

## 1. Why Save Product Data?

A Python object exists in the program while the application is running. If the program stops, its in-memory objects are not automatically saved.

For example, a `Product` object may contain an identifier, name, price, and quantity. To keep those details for the next run, convert the relevant attributes into a serializable structure and write it to a file.

JSON is suitable for this small example because it can represent dictionaries, lists, strings, numbers, booleans, and `None`.

## 2. Define the Product Class

Start with a small class. This example uses the same core product fields as the earlier worked examples.

```python
class Product:
    """Represent a product in the eCOMMart catalogue."""

    def __init__(self, product_id, name, price, quantity):
        """Initialize the product's details."""
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def stock_value(self):
        """Return the value of the product's current stock."""
        return self.price * self.quantity
```

Create a few objects:

```python
products = [
    Product("P101", "Wireless Mouse", 799, 25),
    Product("P102", "Keyboard", 1299, 18),
    Product("P103", "Laptop Stand", 999, 12)
]

print(f"Products in memory: {len(products)}")
```

Output:

```text
Products in memory: 3
```

The objects are currently in memory. Next, convert their data into dictionaries.

## 3. Convert Objects into Dictionaries

JSON does not automatically know how to serialize a custom `Product` object. Create a dictionary containing the fields you want to save.

```python
def product_to_dict(product):
    """Convert a Product object into a JSON-compatible dictionary."""
    return {
        "product_id": product.product_id,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    }


products = [
    Product("P101", "Wireless Mouse", 799, 25),
    Product("P102", "Keyboard", 1299, 18)
]

records = [product_to_dict(product) for product in products]

print(records[0])
```

Output:

```text
{'product_id': 'P101', 'name': 'Wireless Mouse', 'price': 799, 'quantity': 25}
```

The dictionary contains ordinary Python values that the JSON module can serialize. The conversion function also makes it explicit which fields are saved.

## 4. Save Product Records to JSON

Use `json.dump()` to write a list of dictionaries to `products.json`.

```python
import json

def product_to_dict(product):
    """Convert a Product object into a JSON-compatible dictionary."""
    return {
        "product_id": product.product_id,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    }


products = [
    Product("P101", "Wireless Mouse", 799, 25),
    Product("P102", "Keyboard", 1299, 18)
]

records = [product_to_dict(product) for product in products]

with open("products.json", "w", encoding="utf-8") as file:
    json.dump(records, file, indent=4)

print(f"Saved {len(records)} products.")
```

Output:

```text
Saved 2 products.
```

The resulting file contains:

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
        "quantity": 18
    }
]
```

This example assumes the `Product` class from Section 2 is defined in the same script. In a single script, define the class and conversion function once, then use them in the save and load steps.

## 5. Load JSON and Rebuild Product Objects

Reading JSON gives you dictionaries and lists, not `Product` instances. Convert each record back into an object.

```python
import json

def product_from_dict(record):
    """Create a Product object from a dictionary of product fields."""
    return Product(
        record["product_id"],
        record["name"],
        record["price"],
        record["quantity"]
    )


with open("products.json", "r", encoding="utf-8") as file:
    records = json.load(file)

products = [product_from_dict(record) for record in records]

print(f"Loaded {len(products)} products.")
print(products[0].name)
print(products[0].stock_value())
```

Output:

```text
Loaded 2 products.
Wireless Mouse
19975
```

This example assumes that `Product` is already defined and that the JSON file contains the expected fields. `product_from_dict()` is the reverse of `product_to_dict()`.

## 6. Validate Data Before Creating Objects

Saved files may be incomplete or contain values of unexpected types. Check records before trusting them.

```python
def product_from_dict(record):
    """Create a Product object from a dictionary of product fields."""
    required_fields = {"product_id", "name", "price", "quantity"}

    if not isinstance(record, dict):
        raise ValueError("Each product record must be a dictionary.")

    missing_fields = required_fields - record.keys()
    if missing_fields:
        raise ValueError(f"Missing fields: {', '.join(sorted(missing_fields))}")

    if not isinstance(record["name"], str) or not record["name"].strip():
        raise ValueError("Product name must be a non-empty string.")

    if not isinstance(record["price"], (int, float)) or isinstance(record["price"], bool):
        raise ValueError("Product price must be numeric.")

    if not isinstance(record["quantity"], int) or isinstance(record["quantity"], bool):
        raise ValueError("Product quantity must be an integer.")

    return Product(
        record["product_id"],
        record["name"],
        record["price"],
        record["quantity"]
    )
```

This validation checks that the record has the expected shape and basic types. The `Product` constructor also checks for negative price and quantity values.

For a real application, you may need additional checks, such as ensuring product IDs are unique and verifying that a price uses an acceptable precision.

## 7. Worked Example: Save and Reload a Catalogue

The complete flow is:

```text
Product objects
      |
      v
Convert objects to dictionaries
      |
      v
Write list of dictionaries to JSON
      |
      v
Read JSON into Python dictionaries
      |
      v
Convert dictionaries back to Product objects
```

The following example combines the main steps. Run it as one Python script.

```python
import json


class Product:
    """Represent a product in the eCOMMart catalogue."""

    def __init__(self, product_id, name, price, quantity):
        """Initialize the product's details."""
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def stock_value(self):
        """Return the value of the product's current stock."""
        return self.price * self.quantity


def product_to_dict(product):
    """Convert a Product object into a JSON-compatible dictionary."""
    return {
        "product_id": product.product_id,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    }


def product_from_dict(record):
    """Create a Product object from a dictionary of product fields."""
    return Product(
        record["product_id"],
        record["name"],
        record["price"],
        record["quantity"]
    )


products = [
    Product("P101", "Wireless Mouse", 799, 25),
    Product("P102", "Keyboard", 1299, 18)
]

records = [product_to_dict(product) for product in products]

with open("products.json", "w", encoding="utf-8") as file:
    json.dump(records, file, indent=4)

with open("products.json", "r", encoding="utf-8") as file:
    loaded_records = json.load(file)

loaded_products = [product_from_dict(record) for record in loaded_records]

print(f"Saved records: {len(records)}")
print(f"Reloaded products: {len(loaded_products)}")
print(f"First product: {loaded_products[0].name}")
```

Output:

```text
Saved records: 2
Reloaded products: 2
First product: Wireless Mouse
```

The JSON file acts as the bridge between one run of the program and a later run. For this training example, the file is written in the current working directory.

## 8. Practice Tasks

Complete the tasks in order. Each task builds on the ideas introduced in this lesson.

### Task 1 — Convert a Product to a Dictionary

Create a `Product` class with `product_id`, `name`, `price`, and `quantity`. Write a `product_to_dict()` function that returns those four fields in a dictionary.

For a `Phone Stand` with ID `P301`, price `399`, and quantity `10`, print the returned dictionary.

Expected output:

```text
{'product_id': 'P301', 'name': 'Phone Stand', 'price': 399, 'quantity': 10}
```

### Task 2 — Save Multiple Records

Create two product dictionaries and save them as a list to `task_products.json` using `json.dump()` with `indent=4`. Print the number of records saved.

Expected output:

```text
Saved records: 2
```

### Task 3 — Reload Product Objects

Read the list from `task_products.json`. Use a `product_from_dict()` function to create a `Product` object for each record. Print the number of objects and the first product's name.

Expected output:

```text
Reloaded products: 2
First product: Phone Stand
```

## Summary

| Concept | Purpose |
|---|---|
| `product_to_dict()` | Converts object attributes into serializable data |
| `json.dump()` | Writes the records to a JSON file |
| `json.load()` | Reads JSON data back into Python |
| `product_from_dict()` | Reconstructs an object from a dictionary |
| Validation | Checks data shape and field values before use |
| Save-and-load workflow | Preserves product data between program runs |

Custom objects are not automatically stored as JSON. Convert their relevant attributes into dictionaries, save those dictionaries, and rebuild objects when the data is loaded again.

*Next: `04_Config_Driven_Application.md`*
