# Week 4 Exercises: OOP and File Handling

## eCOMMart AI Squad | Week 4

> “Build confidence by combining small, reusable pieces into complete programs.”

## Learning Goals

By completing these exercises, you will practise how to:

1. Define classes and create objects.
2. Use instance attributes and methods.
3. Apply encapsulation, inheritance, and composition.
4. Read and write text, JSON, and CSV files.
5. Load configuration, save application output, and handle common file errors.
6. Combine OOP and file handling in small eCOMMart scenarios.

---

## How to Work Through the Exercises

- Complete the exercises in order, or choose a section to practise a specific skill.
- Save each exercise in its own Python file if you are working in VS Code.
- Create any sample data files in the same project folder unless the task specifies a folder.
- Run your code and compare the actual output with the expected output.
- Use the standard Python library only; no third-party packages are required.
- The tasks below describe what to build. Sample data and expected output are included where useful; not every task has a single required implementation.

## Section 1 — Classes and Objects

### Exercise 1: Create a Product

Create a `Product` class with these attributes:
- `product_id`
- `name`
- `price`
- `quantity`

Create two product objects and print their names and prices.

Use these sample products:
- `P101`, `Wireless Mouse`, price `799`, quantity `25`
- `P102`, `Keyboard`, price `1299`, quantity `18`

Expected output:

```text
Wireless Mouse: ₹799
Keyboard: ₹1299
```

### Exercise 2: Add a Stock Value Method

Add a `stock_value()` method that returns `price * quantity`.

Create a product with price `500` and quantity `6`, then print its stock value.

Expected output:

```text
3000
```

### Exercise 3: Add a Product Summary

Add a `display()` method that prints the product ID, name, price, and quantity in one readable line.

For a product with ID `P301`, name `Phone Stand`, price `399`, and quantity `10`, one possible output is:

```text
P301 | Phone Stand | ₹399 | Stock: 10
```

### Exercise 4: Validate Product Values

Update the class so that a negative price or negative quantity raises `ValueError`. Try creating a product with a negative price and handle the error with `try` and `except`.

Expected output:

```text
Price cannot be negative.
```

Use a clear exception message of your own if it communicates the same issue.

---

## Section 2 — Encapsulation, Properties, and Special Methods

### Exercise 5: Protect a Product Price

Create a `Product` class with a `price` property. Reject a negative price in the setter by raising `ValueError`.

Try assigning `-10` and handle the error.

Expected output:

```text
Price cannot be negative.
```

### Exercise 6: Add a String Representation

Implement `__str__()` so printing a product displays a readable summary.

For a product named `Desk Lamp` with a price of `899`, your output could be:

```text
Desk Lamp - ₹899
```

### Exercise 7: Distinguish `__str__()` and `__repr__()`

Implement both methods:
- `__str__()` should be human-readable.
- `__repr__()` should be useful when inspecting or debugging an object.

Create an object and print it, then call `repr()` on it. Confirm that the outputs serve different purposes.

### Exercise 8: Add a Class Attribute

Add a class attribute named `category` with the value `"General"`.

Create two products and print their category. Briefly test what happens when you assign a `category` attribute directly to one instance.

---

## Section 3 — Inheritance and Composition

### Exercise 9: Create a Discounted Product

Create a `DiscountedProduct` class that inherits from `Product` and adds `discount_percent`. Use `super().__init__()` to initialize the shared product fields.

Add a `selling_price()` method.

For a product with a price of `1000` and a discount of `10%`, expected output:

```text
900.00
```

### Exercise 10: Override the Display Method

Override `display()` in `DiscountedProduct` so the output includes the discount percentage and selling price.

For a `Desk Lamp` priced at `1000` with a `10%` discount, one possible output is:

```text
Desk Lamp | Regular: ₹1000 | Discount: 10% | Selling: ₹900.00
```

### Exercise 11: Model an Order with Composition

Create:
- A `Product` class.
- An `OrderItem` class that contains a product and a quantity.
- An `Order` class that stores multiple order items.

Add a method that calculates the total order value.

Use these items:
- Wireless Mouse: price `799`, quantity ordered `2`
- Keyboard: price `1299`, quantity ordered `1`

Expected output:

```text
Order total: ₹2897
```

### Exercise 12: Build a Catalogue Manager

Create a `CatalogManager` class that stores product objects in a list. Add methods to add a product and find a product by ID. Return `None` if the ID is not found.

Test both a successful search and an unsuccessful search.

---

## Section 4 — Text File Handling

### Exercise 13: Read a Text File

Create `products.txt` with the following lines:

```text
Wireless Mouse
Keyboard
Laptop Stand
```

Read the file line by line and print each product name without extra whitespace.

Expected output:

```text
Wireless Mouse
Keyboard
Laptop Stand
```

### Exercise 14: Write a Report

Write these lines to `daily_report.txt`:

```text
eCOMMart Daily Report
Orders processed: 12
```

Use `with open(...)` and write mode. Print a confirmation after saving.

Expected output:

```text
Report saved.
```

### Exercise 15: Append an Activity Log

Append the line `Order ORD501 processed` to `activity.log`. Run the program twice and inspect the file to confirm that a new line is appended each time.

Expected output from one run:

```text
Activity recorded.
```

### Exercise 16: Count Lines

Read `products.txt` and count its non-empty lines. Print the count.

For the three-line sample file above, expected output:

```text
Product lines: 3
```

---

## Section 5 — JSON and CSV

### Exercise 17: Save Products as JSON

Create a list of two product dictionaries and save it to `products.json` using `json.dump()` with `indent=4`.

Print a confirmation after saving.

Expected output:

```text
Product data saved.
```

### Exercise 18: Load JSON into Product Objects

Read a list of product dictionaries from `products.json` and convert each record into a `Product` object.

Print the number of objects loaded and the first product's name.

For a file with two products, expected output:

```text
Products loaded: 2
First product: Wireless Mouse
```

### Exercise 19: Read a CSV Catalogue

Create `products.csv`:

```csv
product_id,name,price,quantity
P101,Wireless Mouse,799,25
P102,Keyboard,1299,18
```

Use `csv.DictReader` to print each product's name and price.

Expected output:

```text
Wireless Mouse: ₹799
Keyboard: ₹1299
```

### Exercise 20: Calculate Total Stock Value from CSV

Use `csv.DictReader` to read `price` and `quantity`, convert both values to integers, and calculate the total stock value.

For the sample file above, expected output:

```text
Total stock value: ₹43357
```

### Exercise 21: Append a CSV Record

Use `csv.writer` to append one new product record to an existing CSV file. Do not add a second header row. Print a confirmation after writing.

Expected output:

```text
Product appended.
```

---

## Section 6 — Configuration, Output, and Errors

### Exercise 22: Load a Configuration File

Create `config.json`:

```json
{
    "store_name": "eCOMMart",
    "delivery_fee": 49,
    "free_delivery_threshold": 999
}
```

Load the file and print the store name and delivery fee.

Expected output:

```text
Store: eCOMMart
Delivery fee: ₹49
```

### Exercise 23: Calculate Delivery from Configuration

Use the configuration from Exercise 22 to calculate the delivery fee for an order total of `1200`. Apply free delivery when the order total reaches the configured threshold.

Expected output:

```text
Delivery fee: ₹0
```

### Exercise 24: Save a Low-Stock Report

Given a list of product dictionaries, select products with quantities below a configured threshold. Write a report to `reports/low_stock.txt`, creating the directory if needed.

For a threshold of `10` and these quantities:
- Keyboard: `6`
- Laptop Stand: `4`
- Wireless Mouse: `25`

The report should include the first two products and exclude Wireless Mouse.

### Exercise 25: Handle a Missing File

Try to read `missing_products.json`. Catch `FileNotFoundError` and print a helpful message.

Expected output:

```text
Product data file was not found.
```

### Exercise 26: Handle Invalid JSON

Use `json.loads()` with this invalid JSON text:

```python
invalid_text = '{"name": "Keyboard",}'
```

Catch `json.JSONDecodeError` and print a helpful message.

Expected output:

```text
Invalid JSON data.
```

### Exercise 27: Handle an Invalid Numeric Value

Attempt to convert `"unknown"` to an integer. Catch `ValueError` and print a clear message.

Expected output:

```text
Quantity must be numeric.
```

---

## Section 7 — Mini Projects

### Exercise 28: Product Catalogue File Manager

Build a small application that:
1. Defines a `Product` class.
2. Stores several products in a list.
3. Converts products to dictionaries.
4. Saves the list to `products.json`.
5. Loads the JSON data and rebuilds the objects.
6. Displays the loaded products.

**Acceptance criteria**
- The JSON file contains a list of product records.
- The application can load the saved file in a later run.
- Invalid or missing data is handled with a useful message.

### Exercise 29: Low-Stock Report Generator

Build a report generator that:
1. Loads its threshold and file paths from `config.json`.
2. Loads products from a JSON file.
3. Finds products below the threshold.
4. Saves a text report in a `reports` folder.
5. Prints how many products were included.

**Acceptance criteria**
- Changing the threshold in the configuration changes the result.
- The output directory is created if it does not exist.
- The report is readable and has a clear heading.

### Exercise 30: Mini OOP Stock-Check Tool

Build a `StockCheckTool` class that accepts a product ID and returns a dictionary.

A successful result should include:
- `success`
- `product_id`
- `name`
- `quantity`
- `in_stock`

An unsuccessful result should include:
- `success: False`
- An `error` message

Save one result to a JSON file and test a valid ID, an unknown ID, and blank input.

**Acceptance criteria**
- The tool returns structured data instead of printing from inside `run()`.
- Invalid input does not crash the program.
- The result can be saved using `json.dump()`.

---

## Final Challenge — eCOMMart Catalogue Assistant

Combine the key ideas from Week 4 into one small application.

Your application should:

1. Define a `Product` class with attributes and useful methods.
2. Use inheritance for a specialised product type, or composition to model an order.
3. Load configuration from JSON.
4. Load product records from JSON or CSV.
5. Validate required fields and handle common file errors.
6. Find low-stock products using the configured threshold.
7. Save a text or JSON report.
8. Include a small stock-check tool that returns structured data.
9. Demonstrate the program with at least three products.

### Suggested Project Structure

```text
ecommart_week4/
├── app.py
├── config.json
├── products.json
└── reports/
    └── low_stock.txt
```

### Completion Checklist

- [ ] Classes and objects are used meaningfully.
- [ ] Each method has a clear responsibility.
- [ ] At least one method returns a value that is used by its caller.
- [ ] Data is loaded from a file.
- [ ] Data or a report is saved to a file.
- [ ] Configuration affects program behaviour.
- [ ] Missing files and invalid JSON are handled.
- [ ] The output is checked against sample data.
- [ ] The code is organised and readable.

## Summary

These exercises move from individual concepts to complete workflows. Practise the small tasks first, then use the mini projects to combine OOP, file handling, JSON, CSV, configuration, and error handling in an eCOMMart scenario.

*Next: `solutions.md`*
