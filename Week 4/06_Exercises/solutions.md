# Week 4 Exercise Solutions: OOP and File Handling

## eCOMMart AI Squad | Week 4

> “Use these solutions to check your approach, understand the reasoning, and practise writing the code independently.”

## How to Use This File

- Try each exercise in `exercises.md` before checking its solution.
- Solutions are reference implementations; equivalent code is acceptable if it meets the requirements.
- Run the examples in VS Code or another Python environment.
- Some exercises build on classes from earlier tasks. Where needed, the relevant class is defined again so the example can run independently.
- File-based examples assume that you run the code from the folder containing the named data file, unless the solution creates a subfolder.

---

## Section 1 — Classes and Objects

### Exercise 1: Create a Product

```python
class Product:
    """Represent a product in the eCOMMart catalogue."""

    def __init__(self, product_id, name, price, quantity):
        """Initialize the product details."""
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity


mouse = Product("P101", "Wireless Mouse", 799, 25)
keyboard = Product("P102", "Keyboard", 1299, 18)

print(f"{mouse.name}: ₹{mouse.price}")
print(f"{keyboard.name}: ₹{keyboard.price}")
```

Output:

```text
Wireless Mouse: ₹799
Keyboard: ₹1299
```

### Exercise 2: Add a Stock Value Method

```python
class Product:
    """Represent a product in the eCOMMart catalogue."""

    def __init__(self, name, price, quantity):
        """Initialize product details."""
        self.name = name
        self.price = price
        self.quantity = quantity

    def stock_value(self):
        """Return the total value of the available stock."""
        return self.price * self.quantity


product = Product("Notebook", 500, 6)
print(product.stock_value())
```

Output:

```text
3000
```

### Exercise 3: Add a Product Summary

```python
class Product:
    """Represent a product in the eCOMMart catalogue."""

    def __init__(self, product_id, name, price, quantity):
        """Initialize product details."""
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def display(self):
        """Print a readable summary of the product."""
        print(
            f"{self.product_id} | {self.name} | "
            f"₹{self.price} | Stock: {self.quantity}"
        )


product = Product("P301", "Phone Stand", 399, 10)
product.display()
```

Output:

```text
P301 | Phone Stand | ₹399 | Stock: 10
```

### Exercise 4: Validate Product Values

```python
class Product:
    """Represent a product with basic value validation."""

    def __init__(self, name, price, quantity):
        """Validate and store the product details."""
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.name = name
        self.price = price
        self.quantity = quantity


try:
    product = Product("Keyboard", -100, 5)
except ValueError as error:
    print(error)
```

Output:

```text
Price cannot be negative.
```

---

## Section 2 — Encapsulation, Properties, and Special Methods

### Exercise 5: Protect a Product Price

```python
class Product:
    """Represent a product with a validated price."""

    def __init__(self, name, price):
        """Initialize the product using the price property."""
        self.name = name
        self.price = price

    @property
    def price(self):
        """Return the current product price."""
        return self._price

    @price.setter
    def price(self, value):
        """Set the price after rejecting negative values."""
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self._price = value


product = Product("Desk Lamp", 899)

try:
    product.price = -10
except ValueError as error:
    print(error)
```

Output:

```text
Price cannot be negative.
```

### Exercise 6: Add a String Representation

```python
class Product:
    """Represent a product with a readable string form."""

    def __init__(self, name, price):
        """Initialize the product details."""
        self.name = name
        self.price = price

    def __str__(self):
        """Return a human-readable product summary."""
        return f"{self.name} - ₹{self.price}"


product = Product("Desk Lamp", 899)
print(product)
```

Output:

```text
Desk Lamp - ₹899
```

### Exercise 7: Distinguish `__str__()` and `__repr__()`

```python
class Product:
    """Represent a product with display and debug formats."""

    def __init__(self, name, price):
        """Initialize the product details."""
        self.name = name
        self.price = price

    def __str__(self):
        """Return a human-readable product summary."""
        return f"{self.name} - ₹{self.price}"

    def __repr__(self):
        """Return a developer-oriented representation."""
        return f"Product(name={self.name!r}, price={self.price!r})"


product = Product("Desk Lamp", 899)
print(product)
print(repr(product))
```

Output:

```text
Desk Lamp - ₹899
Product(name='Desk Lamp', price=899)
```

### Exercise 8: Add a Class Attribute

```python
class Product:
    """Represent a product with a default category."""

    category = "General"

    def __init__(self, name):
        """Initialize the product name."""
        self.name = name


mouse = Product("Wireless Mouse")
keyboard = Product("Keyboard")

print(mouse.category)
print(keyboard.category)

mouse.category = "Accessories"

print(mouse.category)
print(keyboard.category)
print(Product.category)
```

Output:

```text
General
General
Accessories
General
General
```

Assigning `mouse.category` creates or updates an instance attribute that shadows the class attribute. It does not change the class attribute or the other object's value.

---

## Section 3 — Inheritance and Composition

### Exercise 9: Create a Discounted Product

```python
class Product:
    """Represent a standard product."""

    def __init__(self, name, price):
        """Initialize the product details."""
        self.name = name
        self.price = price


class DiscountedProduct(Product):
    """Represent a product with a percentage discount."""

    def __init__(self, name, price, discount_percent):
        """Initialize shared product data and the discount."""
        super().__init__(name, price)
        self.discount_percent = discount_percent

    def selling_price(self):
        """Return the price after applying the discount."""
        return self.price * (1 - self.discount_percent / 100)


product = DiscountedProduct("Desk Lamp", 1000, 10)
print(f"{product.selling_price():.2f}")
```

Output:

```text
900.00
```

### Exercise 10: Override the Display Method

```python
class Product:
    """Represent a standard product."""

    def __init__(self, name, price):
        """Initialize the product details."""
        self.name = name
        self.price = price

    def display(self):
        """Print the product name and price."""
        print(f"{self.name} | Regular: ₹{self.price}")


class DiscountedProduct(Product):
    """Represent a product with a percentage discount."""

    def __init__(self, name, price, discount_percent):
        """Initialize product data and discount."""
        super().__init__(name, price)
        self.discount_percent = discount_percent

    def selling_price(self):
        """Return the discounted price."""
        return self.price * (1 - self.discount_percent / 100)

    def display(self):
        """Print the regular price, discount, and selling price."""
        print(
            f"{self.name} | Regular: ₹{self.price} | "
            f"Discount: {self.discount_percent}% | "
            f"Selling: ₹{self.selling_price():.2f}"
        )


product = DiscountedProduct("Desk Lamp", 1000, 10)
product.display()
```

Output:

```text
Desk Lamp | Regular: ₹1000 | Discount: 10% | Selling: ₹900.00
```

### Exercise 11: Model an Order with Composition

```python
class Product:
    """Represent a product that can be ordered."""

    def __init__(self, name, price):
        """Initialize the product name and price."""
        self.name = name
        self.price = price


class OrderItem:
    """Represent a product and the quantity ordered."""

    def __init__(self, product, quantity):
        """Store the product object and ordered quantity."""
        self.product = product
        self.quantity = quantity

    def subtotal(self):
        """Return the subtotal for this order item."""
        return self.product.price * self.quantity


class Order:
    """Represent an order containing multiple items."""

    def __init__(self):
        """Create an order with no items."""
        self.items = []

    def add_item(self, item):
        """Add an OrderItem to the order."""
        self.items.append(item)

    def total(self):
        """Return the sum of all item subtotals."""
        return sum(item.subtotal() for item in self.items)


mouse = Product("Wireless Mouse", 799)
keyboard = Product("Keyboard", 1299)

order = Order()
order.add_item(OrderItem(mouse, 2))
order.add_item(OrderItem(keyboard, 1))

print(f"Order total: ₹{order.total()}")
```

Output:

```text
Order total: ₹2897
```

### Exercise 12: Build a Catalogue Manager

```python
class Product:
    """Represent a catalogue product."""

    def __init__(self, product_id, name):
        """Initialize the product identifier and name."""
        self.product_id = product_id
        self.name = name


class CatalogManager:
    """Store products and find them by ID."""

    def __init__(self):
        """Create an empty product catalogue."""
        self.products = []

    def add_product(self, product):
        """Add a product to the catalogue."""
        self.products.append(product)

    def find_by_id(self, product_id):
        """Return a matching product, or None when not found."""
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None


catalog = CatalogManager()
catalog.add_product(Product("P101", "Wireless Mouse"))

found = catalog.find_by_id("P101")
print(found.name if found else "Product not found.")

missing = catalog.find_by_id("P999")
print(missing.name if missing else "Product not found.")
```

Output:

```text
Wireless Mouse
Product not found.
```

---

## Section 4 — Text File Handling

### Exercise 13: Read a Text File

Create `products.txt` containing the three sample lines from the exercise.

```python
with open("products.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())
```

Output:

```text
Wireless Mouse
Keyboard
Laptop Stand
```

### Exercise 14: Write a Report

```python
report = "eCOMMart Daily Report\nOrders processed: 12\n"

with open("daily_report.txt", "w", encoding="utf-8") as file:
    file.write(report)

print("Report saved.")
```

Output:

```text
Report saved.
```

### Exercise 15: Append an Activity Log

```python
with open("activity.log", "a", encoding="utf-8") as file:
    file.write("Order ORD501 processed\n")

print("Activity recorded.")
```

Output:

```text
Activity recorded.
```

Append mode preserves existing content and adds the new line. Running this script twice adds the line twice.

### Exercise 16: Count Lines

```python
with open("products.txt", "r", encoding="utf-8") as file:
    product_lines = [line.strip() for line in file if line.strip()]

print(f"Product lines: {len(product_lines)}")
```

Output for the three-line sample file:

```text
Product lines: 3
```

---

## Section 5 — JSON and CSV

### Exercise 17: Save Products as JSON

```python
import json

products = [
    {"product_id": "P101", "name": "Wireless Mouse", "price": 799, "quantity": 25},
    {"product_id": "P102", "name": "Keyboard", "price": 1299, "quantity": 18}
]

with open("products.json", "w", encoding="utf-8") as file:
    json.dump(products, file, indent=4)

print("Product data saved.")
```

Output:

```text
Product data saved.
```

### Exercise 18: Load JSON into Product Objects

```python
import json


class Product:
    """Represent a product loaded from JSON."""

    def __init__(self, product_id, name, price, quantity):
        """Initialize the product details."""
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity


with open("products.json", "r", encoding="utf-8") as file:
    records = json.load(file)

products = [
    Product(
        record["product_id"],
        record["name"],
        record["price"],
        record["quantity"]
    )
    for record in records
]

print(f"Products loaded: {len(products)}")
print(f"First product: {products[0].name}")
```

Output for the sample file created in Exercise 17:

```text
Products loaded: 2
First product: Wireless Mouse
```

### Exercise 19: Read a CSV Catalogue

Create `products.csv` with the header and rows from the exercise.

```python
import csv

with open("products.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for product in reader:
        print(f'{product["name"]}: ₹{product["price"]}')
```

Output:

```text
Wireless Mouse: ₹799
Keyboard: ₹1299
```

### Exercise 20: Calculate Total Stock Value from CSV

```python
import csv

total_value = 0

with open("products.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for product in reader:
        total_value += int(product["price"]) * int(product["quantity"])

print(f"Total stock value: ₹{total_value}")
```

Output:

```text
Total stock value: ₹43357
```

Calculation: `799 × 25 = 19975` and `1299 × 18 = 23382`; total `43357`.

### Exercise 21: Append a CSV Record

This example assumes `products.csv` already exists with the four columns shown in the exercise.

```python
import csv

new_product = ["P103", "Laptop Stand", 999, 12]

with open("products.csv", "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(new_product)

print("Product appended.")
```

Output:

```text
Product appended.
```

Do not call `writeheader()` when appending a data row to a file that already has its header.

---

## Section 6 — Configuration, Output, and Errors

### Exercise 22: Load a Configuration File

Create `config.json` with the configuration from the exercise.

```python
import json

with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

print(f'Store: {config["store_name"]}')
print(f'Delivery fee: ₹{config["delivery_fee"]}')
```

Output:

```text
Store: eCOMMart
Delivery fee: ₹49
```

### Exercise 23: Calculate Delivery from Configuration

```python
import json

with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

order_total = 1200

if order_total >= config["free_delivery_threshold"]:
    delivery_fee = 0
else:
    delivery_fee = config["delivery_fee"]

print(f"Delivery fee: ₹{delivery_fee}")
```

Output:

```text
Delivery fee: ₹0
```

### Exercise 24: Save a Low-Stock Report

```python
import json
import os

config = {
    "store_name": "eCOMMart",
    "low_stock_threshold": 10
}

products = [
    {"name": "Keyboard", "quantity": 6},
    {"name": "Laptop Stand", "quantity": 4},
    {"name": "Wireless Mouse", "quantity": 25}
]

low_stock = [
    product for product in products
    if product["quantity"] < config["low_stock_threshold"]
]

lines = [f'{config["store_name"]} Low-Stock Report']
for product in low_stock:
    lines.append(f'{product["name"]}: {product["quantity"]} remaining')

report_text = "\n".join(lines) + "\n"

os.makedirs("reports", exist_ok=True)
with open(os.path.join("reports", "low_stock.txt"), "w", encoding="utf-8") as file:
    file.write(report_text)

print(f"Products included: {len(low_stock)}")
```

Output:

```text
Products included: 2
```

The saved report contains:

```text
eCOMMart Low-Stock Report
Keyboard: 6 remaining
Laptop Stand: 4 remaining
```

### Exercise 25: Handle a Missing File

```python
try:
    with open("missing_products.json", "r", encoding="utf-8") as file:
        content = file.read()
except FileNotFoundError:
    print("Product data file was not found.")
```

Output if the file is missing:

```text
Product data file was not found.
```

### Exercise 26: Handle Invalid JSON

```python
import json

invalid_text = '{"name": "Keyboard",}'

try:
    data = json.loads(invalid_text)
except json.JSONDecodeError:
    print("Invalid JSON data.")
```

Output:

```text
Invalid JSON data.
```

### Exercise 27: Handle an Invalid Numeric Value

```python
quantity_text = "unknown"

try:
    quantity = int(quantity_text)
except ValueError:
    print("Quantity must be numeric.")
```

Output:

```text
Quantity must be numeric.
```

---

## Section 7 — Mini Projects

### Exercise 28: Product Catalogue File Manager

The following is one possible solution. It saves a catalogue to JSON, then loads and displays the saved records.

```python
import json


class Product:
    """Represent a product in the catalogue."""

    def __init__(self, product_id, name, price, quantity):
        """Initialize the product details."""
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def display(self):
        """Print a summary of the product."""
        print(f"{self.product_id} | {self.name} | ₹{self.price} | Stock: {self.quantity}")


def product_to_dict(product):
    """Convert a Product object into a dictionary."""
    return {
        "product_id": product.product_id,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    }


def product_from_dict(record):
    """Build a Product object from a dictionary."""
    return Product(
        record["product_id"],
        record["name"],
        record["price"],
        record["quantity"]
    )


products = [
    Product("P101", "Wireless Mouse", 799, 25),
    Product("P102", "Keyboard", 1299, 18),
    Product("P103", "Laptop Stand", 999, 12)
]

with open("products.json", "w", encoding="utf-8") as file:
    json.dump([product_to_dict(p) for p in products], file, indent=4)

try:
    with open("products.json", "r", encoding="utf-8") as file:
        records = json.load(file)
    loaded_products = [product_from_dict(record) for record in records]
except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError) as error:
    print(f"Could not load catalogue: {error}")
else:
    print(f"Products loaded: {len(loaded_products)}")
    for product in loaded_products:
        product.display()
```

Output:

```text
Products loaded: 3
P101 | Wireless Mouse | ₹799 | Stock: 25
P102 | Keyboard | ₹1299 | Stock: 18
P103 | Laptop Stand | ₹999 | Stock: 12
```

### Exercise 29: Low-Stock Report Generator

This example reads a JSON configuration and product list, filters the products, and writes a report.

Create `config.json`:

```json
{
    "store_name": "eCOMMart",
    "low_stock_threshold": 10,
    "products_file": "products.json",
    "report_file": "reports/low_stock.txt"
}
```

Create `products.json` containing a list of product dictionaries, then run:

```python
import json
import os


def load_json(path):
    """Load JSON data from the specified path."""
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def create_low_stock_report(config, products):
    """Return a report string and the low-stock products."""
    threshold = config["low_stock_threshold"]
    low_stock = [
        product for product in products
        if product["quantity"] < threshold
    ]

    lines = [f'{config["store_name"]} Low-Stock Report']
    for product in low_stock:
        lines.append(f'{product["name"]}: {product["quantity"]} remaining')

    return low_stock, "\n".join(lines) + "\n"


try:
    config = load_json("config.json")
    products = load_json(config["products_file"])
    low_stock, report_text = create_low_stock_report(config, products)

    report_path = config["report_file"]
    report_folder = os.path.dirname(report_path)
    if report_folder:
        os.makedirs(report_folder, exist_ok=True)

    with open(report_path, "w", encoding="utf-8") as file:
        file.write(report_text)
except FileNotFoundError:
    print("A required input file was not found.")
except json.JSONDecodeError:
    print("A JSON file contains invalid data.")
else:
    print(f"Products included: {len(low_stock)}")
    print(f"Report saved to {report_path}")
```

Example output for two products below the threshold:

```text
Products included: 2
Report saved to reports/low_stock.txt
```

### Exercise 30: Mini OOP Stock-Check Tool

```python
import json


class Product:
    """Represent a product in the catalogue."""

    def __init__(self, product_id, name, quantity):
        """Initialize the product fields used by the stock tool."""
        self.product_id = product_id
        self.name = name
        self.quantity = quantity


class StockCheckTool:
    """Look up product stock and return structured results."""

    def __init__(self, products):
        """Store the catalogue products."""
        self.products = products

    def run(self, product_id):
        """Return product stock information or an error result."""
        if not isinstance(product_id, str) or not product_id.strip():
            return {"success": False, "error": "A valid product ID is required."}

        for product in self.products:
            if product.product_id == product_id:
                return {
                    "success": True,
                    "product_id": product.product_id,
                    "name": product.name,
                    "quantity": product.quantity,
                    "in_stock": product.quantity > 0
                }

        return {"success": False, "error": "Product not found."}


products = [
    Product("P101", "Wireless Mouse", 25),
    Product("P102", "Keyboard", 6)
]

tool = StockCheckTool(products)

for product_id in ["P101", "P999", "   "]:
    result = tool.run(product_id)
    print(result)

with open("stock_check_result.json", "w", encoding="utf-8") as file:
    json.dump(tool.run("P101"), file, indent=4)

print("Tool result saved.")
```

Output:

```text
{'success': True, 'product_id': 'P101', 'name': 'Wireless Mouse', 'quantity': 25, 'in_stock': True}
{'success': False, 'error': 'Product not found.'}
{'success': False, 'error': 'A valid product ID is required.'}
Tool result saved.
```

---

## Final Challenge — Suggested Solution Outline

A complete catalogue assistant can use the same building blocks from the examples above:

1. Define `Product` and, if useful, a specialised product class.
2. Load the configuration with `json.load()`.
3. Load product records and convert them into objects.
4. Filter products using the configured low-stock threshold.
5. Save a report after creating its output directory.
6. Provide a `StockCheckTool` that returns a dictionary.
7. Catch expected errors such as `FileNotFoundError` and `json.JSONDecodeError`.

A sensible project structure is:

```text
ecommart_week4/
├── app.py
├── config.json
├── products.json
└── reports/
    └── low_stock.txt
```

Use the acceptance checklist in `exercises.md` to test the finished program. The exact design can vary as long as the required behaviours work.

## Final Review Checklist

- [ ] I can explain the difference between a class and an object.
- [ ] I can write an `__init__()` method and use `self`.
- [ ] I can add methods, properties, and useful string representations.
- [ ] I can explain when inheritance or composition is appropriate.
- [ ] I can read and write text, JSON, and CSV files.
- [ ] I can load configuration and use its values in program logic.
- [ ] I can handle missing files, invalid JSON, and invalid numeric values.
- [ ] I can save and reload product records.
- [ ] I can build a small class-based tool that returns structured data.

## Summary

These solutions are reference implementations for the Week 4 exercises. Focus on understanding why each class, method, file operation, and exception handler is used. Then try modifying the examples—for instance, add a product field, change the report threshold, or introduce another tool input—to confirm that you can apply the concepts independently.
