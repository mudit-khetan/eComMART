# Mini OOP Agent Tool

## eCOMMart AI Squad | Week 4

> “A small, well-defined tool can give an AI workflow a reliable action to call and a clear result to use.”

## What We Will Cover

1. Model a simple tool with a Python class.
2. Separate tool input, validation, and execution.
3. Return structured results from a tool.
4. Save tool results to a JSON file.
5. Build and test a mini eCOMMart stock-check tool.

---

## 1. What Is a Tool in an AI Workflow?

In an AI workflow, a **tool** is a function or operation that a system can call to perform a specific task, such as looking up an order, checking stock, or saving a report.

This lesson builds a small Python tool. It does **not** connect to a real AI model or automatically decide when to call the tool. It demonstrates the software component that could be called by a larger application.

For eCOMMart, a stock-check tool can accept a product ID, search a catalogue, and return a structured result.

```text
Input: product ID
       |
       v
Validate input
       |
       v
Search product catalogue
       |
       v
Return result dictionary
```

## 2. Prepare the Product Model

Use a small `Product` class to keep the fields required by the tool together.

```python
class Product:
    """Represent a product in the eCOMMart catalogue."""

    def __init__(self, product_id, name, price, quantity):
        """Initialize the product's catalogue details."""
        if not product_id:
            raise ValueError("Product ID is required.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity


products = [
    Product("P101", "Wireless Mouse", 799, 25),
    Product("P102", "Keyboard", 1299, 6),
    Product("P103", "Laptop Stand", 999, 4)
]

print(f"Catalogue products: {len(products)}")
```

Output:

```text
Catalogue products: 3
```

This is an in-memory catalogue for the exercise. The data is created in the script rather than loaded from a database or an external service.

## 3. Build the Stock-Check Tool

The `StockCheckTool` class receives a list of products and provides a method to look up one product by ID.

```python
class StockCheckTool:
    """Look up product stock in an in-memory catalogue."""

    def __init__(self, products):
        """Store the catalogue products used by this tool."""
        self.products = products

    def run(self, product_id):
        """Return stock details for a matching product ID."""
        if not isinstance(product_id, str) or not product_id.strip():
            return {
                "success": False,
                "error": "A valid product ID is required."
            }

        for product in self.products:
            if product.product_id == product_id:
                return {
                    "success": True,
                    "product_id": product.product_id,
                    "name": product.name,
                    "quantity": product.quantity,
                    "in_stock": product.quantity > 0
                }

        return {
            "success": False,
            "error": f"Product {product_id} was not found."
        }
```

The `run()` method always returns a dictionary. A successful result contains product details, while an unsuccessful result contains an error message.

Returning structured data is more flexible than printing inside the tool because another part of the program can inspect the values, display them, or save them.

## 4. Call the Tool

Create a tool instance and call `run()` with a product ID.

```python
tool = StockCheckTool(products)

result = tool.run("P102")

print(result)
```

Output:

```text
{'success': True, 'product_id': 'P102', 'name': 'Keyboard', 'quantity': 6, 'in_stock': True}
```

You can use the result's fields independently:

```python
result = tool.run("P103")

if result["success"]:
    print(result["name"])
    print(f'Quantity available: {result["quantity"]}')
else:
    print(result["error"])
```

Output:

```text
Laptop Stand
Quantity available: 4
```

The caller decides how to present the returned information. This separation keeps the tool focused on its task.

## 5. Test Missing Products and Invalid Input

A tool should return a predictable result when it cannot complete a request.

```python
tool = StockCheckTool(products)

missing_result = tool.run("P999")
print(missing_result)

invalid_result = tool.run("   ")
print(invalid_result)
```

Output:

```text
{'success': False, 'error': 'Product P999 was not found.'}
{'success': False, 'error': 'A valid product ID is required.'}
```

The input check prevents a blank or whitespace-only ID from being treated as a meaningful search. The lookup result makes it clear when no matching product exists.

## 6. Add a Low-Stock Tool

A second tool can find products whose quantities fall below a supplied threshold. It reuses the same `Product` objects.

```python
class LowStockTool:
    """Find products with quantities below a threshold."""

    def __init__(self, products):
        """Store the catalogue products used by this tool."""
        self.products = products

    def run(self, threshold):
        """Return a list of products below the requested threshold."""
        if not isinstance(threshold, int) or isinstance(threshold, bool):
            return {
                "success": False,
                "error": "Threshold must be an integer."
            }

        if threshold < 0:
            return {
                "success": False,
                "error": "Threshold cannot be negative."
            }

        low_stock = [
            {
                "product_id": product.product_id,
                "name": product.name,
                "quantity": product.quantity
            }
            for product in self.products
            if product.quantity < threshold
        ]

        return {
            "success": True,
            "threshold": threshold,
            "products": low_stock,
            "count": len(low_stock)
        }


low_stock_tool = LowStockTool(products)
result = low_stock_tool.run(10)

print(f'Products below threshold: {result["count"]}')
for product in result["products"]:
    print(f'{product["name"]}: {product["quantity"]}')
```

Output:

```text
Products below threshold: 2
Keyboard: 6
Laptop Stand: 4
```

The result is structured as a dictionary containing a list of product dictionaries. The caller can display the results or pass them to another operation.

## 7. Save a Tool Result to JSON

A tool's result can be saved for auditing or later processing. Use `json.dump()` to write the result dictionary to a file.

```python
import json

tool = StockCheckTool(products)
result = tool.run("P101")

with open("stock_check_result.json", "w", encoding="utf-8") as file:
    json.dump(result, file, indent=4)

print("Tool result saved.")
```

Output:

```text
Tool result saved.
```

The file `stock_check_result.json` contains:

```json
{
    "success": true,
    "product_id": "P101",
    "name": "Wireless Mouse",
    "quantity": 25,
    "in_stock": true
}
```

This works because the tool returns only JSON-compatible values: dictionaries, strings, integers, and Booleans. It does not try to serialize the custom `Product` object itself.

## 8. Complete Mini Example

The following script combines the model and the stock-check tool. Run it as one file.

```python
import json


class Product:
    """Represent a product in the eCOMMart catalogue."""

    def __init__(self, product_id, name, price, quantity):
        """Initialize the product's catalogue details."""
        if not product_id:
            raise ValueError("Product ID is required.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity


class StockCheckTool:
    """Look up product stock in an in-memory catalogue."""

    def __init__(self, products):
        """Store the catalogue products used by this tool."""
        self.products = products

    def run(self, product_id):
        """Return stock details for a matching product ID."""
        if not isinstance(product_id, str) or not product_id.strip():
            return {
                "success": False,
                "error": "A valid product ID is required."
            }

        for product in self.products:
            if product.product_id == product_id:
                return {
                    "success": True,
                    "product_id": product.product_id,
                    "name": product.name,
                    "quantity": product.quantity,
                    "in_stock": product.quantity > 0
                }

        return {
            "success": False,
            "error": f"Product {product_id} was not found."
        }


products = [
    Product("P101", "Wireless Mouse", 799, 25),
    Product("P102", "Keyboard", 1299, 6),
    Product("P103", "Laptop Stand", 999, 4)
]

stock_tool = StockCheckTool(products)
result = stock_tool.run("P102")

if result["success"]:
    print(f'Product: {result["name"]}')
    print(f'Quantity: {result["quantity"]}')
    print(f'In stock: {result["in_stock"]}')
else:
    print(result["error"])

with open("stock_check_result.json", "w", encoding="utf-8") as file:
    json.dump(result, file, indent=4)

print("Tool result saved.")
```

Output:

```text
Product: Keyboard
Quantity: 6
In stock: True
Tool result saved.
```

This example demonstrates a small, testable tool component. A larger application could call the same class from a command-line interface, web service, or AI orchestration layer.

## 9. Practice Tasks

Complete the tasks in order. Each task builds on the ideas introduced in this lesson.

### Task 1 — Return a Structured Result

Create a `Product` class and a `StockCheckTool` with a `run(product_id)` method. When the ID matches, return a dictionary containing `success`, `name`, and `quantity`.

For product `P201`, named `Phone Stand` with quantity `12`, expected output when printing the result:

```text
{'success': True, 'name': 'Phone Stand', 'quantity': 12}
```

### Task 2 — Handle an Unknown ID

Extend your tool so an unknown product ID returns:

```python
{"success": False, "error": "Product not found."}
```

Call the tool with an unknown ID and print the result.

Expected output:

```text
{'success': False, 'error': 'Product not found.'}
```

### Task 3 — Save the Result

Call your stock-check tool for a valid product. Save the returned dictionary to `task_stock_result.json` with `json.dump()` and `indent=4`. Print a confirmation after the file has been written.

Expected output:

```text
Tool result saved.
```

## Summary

| Concept | Purpose |
|---|---|
| Tool class | Packages a specific operation behind a method |
| `run()` | Executes the tool's task using supplied input |
| Input validation | Rejects blank or unsuitable inputs |
| Structured dictionary result | Lets the caller inspect success, data, or errors |
| Separate caller and tool logic | Keeps the tool reusable |
| `json.dump()` | Saves a JSON-compatible result for later use |

This mini tool is a local Python example, not a live AI integration. It demonstrates the core design pattern: accept input, validate it, perform one defined task, and return a structured result.

*Next: `06_Exercises/exercises.md`*
