# Guided Python Database Practice

## Learning objectives

By the end of this lesson, you will be able to:

- Connect Python code to the eComMART SQLite database.
- Write functions that execute parameterized SQL queries.
- Interpret rows returned by `fetchone()` and `fetchall()`.
- Validate input before inserting or updating products.
- Handle missing records and database errors.
- Test CRUD operations while keeping the starter data safe.

This lesson builds on `01_Guided_SQL_Practice.md` and the CRUD module from `02_Implementing_Product_CRUD_Operations.md`. It focuses on the Python side: how you call SQL from a program, use the returned values, and report the outcome.

## 1. Prepare your files

The examples assume this structure:

```text
Week 5/
└── Examples/
    ├── setup_database.py
    ├── ecommart.db
    ├── product_catalog.py
    └── python_database_practice.py
```

If the database has not been created yet, run the setup script from the `Week 5` folder:

```bash
python "Examples/setup_database.py"
```

Create `Examples/python_database_practice.py`. The examples use this database path:

```python
from pathlib import Path
import sqlite3

DATABASE_PATH = Path(__file__).resolve().parent / "ecommart.db"
```

If your files are stored elsewhere, adjust the path deliberately. A wrong path may cause SQLite to open or create a different database file.

## 2. Exercise 1 — Retrieve all products

**Task:** Write a function named `list_products()` that returns all product records in ascending `product_id` order.

Try it before reading the answer.

### Suggested answer

```python
def list_products():
    """Return all products ordered by product ID."""
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.execute(
            """
            SELECT product_id, name, category, price, stock
            FROM products
            ORDER BY product_id
            """
        )
        return cursor.fetchall()

    finally:
        connection.close()
```

Call the function:

```python
products = list_products()

for product in products:
    print(product)
```

Each row is returned as a tuple. With the original starter data, the function returns three rows. Your results may differ if you changed the database during earlier exercises.

**Why this matters:** the function returns data instead of printing inside the database operation. The calling code decides how to display the results.

## 3. Exercise 2 — Find one product by ID

**Task:** Write a function named `find_product(product_id)` that returns one matching record or `None` if the product does not exist.

### Suggested answer

```python
def find_product(product_id):
    """Return one product tuple, or None when no product matches."""
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.execute(
            """
            SELECT product_id, name, category, price, stock
            FROM products
            WHERE product_id = ?
            """,
            (product_id,),
        )
        return cursor.fetchone()

    finally:
        connection.close()
```

Try it:

```python
product = find_product(101)

if product is None:
    print("Product not found.")
else:
    product_id, name, category, price, stock = product
    print(f"{name} costs ₹{price:.2f} and has {stock} units in stock.")
```

For the original starter database, product 101 is the Wireless Barcode Scanner.

Now test an ID you know is not present:

```python
product = find_product(999999)

if product is None:
    print("No product found with that ID.")
```

**Why this matters:** `fetchone()` may return `None`. Always check before unpacking the result.

## 4. Exercise 3 — Filter results using a parameter

**Task:** Write a function that returns products below a supplied price limit. It must use a parameterized query.

### Suggested answer

```python
def find_products_below_price(max_price):
    """Return products whose price is below max_price."""
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.execute(
            """
            SELECT product_id, name, price, stock
            FROM products
            WHERE price < ?
            ORDER BY price
            """,
            (max_price,),
        )
        return cursor.fetchall()

    finally:
        connection.close()
```

Call it:

```python
for product in find_products_below_price(3000):
    print(product)
```

With the original starter data, the Thermal Label Roll is returned.

The `?` placeholder separates the SQL statement from the value. Do not construct the query by joining the price into a string.

## 5. Exercise 4 — Validate input before adding a product

**Task:** Write a helper that rejects a blank product name, blank category, negative price, or negative stock. Then use it before inserting a product.

### Suggested answer

```python
def validate_product(name, category, price, stock):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Product name cannot be empty.")

    if not isinstance(category, str) or not category.strip():
        raise ValueError("Category cannot be empty.")

    if isinstance(price, bool) or not isinstance(price, (int, float)):
        raise ValueError("Price must be a number.")

    if price < 0:
        raise ValueError("Price cannot be negative.")

    if isinstance(stock, bool) or not isinstance(stock, int):
        raise ValueError("Stock must be a whole number.")

    if stock < 0:
        raise ValueError("Stock cannot be negative.")
```

Now write an insert function:

```python
def add_product(name, category, price, stock):
    """Insert a product and return the generated ID."""
    validate_product(name, category, price, stock)

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.execute(
            """
            INSERT INTO products (name, category, price, stock)
            VALUES (?, ?, ?, ?)
            """,
            (name.strip(), category.strip(), float(price), stock),
        )

        product_id = cursor.lastrowid
        connection.commit()
        return product_id

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()
```

Try the validation separately:

```python
try:
    validate_product("   ", "Accessories", 299.00, 10)
except ValueError as error:
    print(error)
```

Expected message:

```text
Product name cannot be empty.
```

No database operation is attempted in that validation test.

## 6. Exercise 5 — Update a product safely

**Task:** Write a function that updates a product's stock. It should reject negative stock and return `True` if a matching product was affected or `False` if no matching product exists.

### Suggested answer

```python
def update_stock(product_id, new_stock):
    if isinstance(new_stock, bool) or not isinstance(new_stock, int):
        raise ValueError("Stock must be a whole number.")

    if new_stock < 0:
        raise ValueError("Stock cannot be negative.")

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.execute(
            """
            UPDATE products
            SET stock = ?
            WHERE product_id = ?
            """,
            (new_stock, product_id),
        )

        if cursor.rowcount != 1:
            connection.rollback()
            return False

        connection.commit()
        return True

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()
```

Test it with a confirmed disposable product ID:

```python
try:
    if update_stock(170, 12):
        print("Stock updated.")
    else:
        print("No matching product was found.")
except (ValueError, sqlite3.Error) as error:
    print(f"Could not update stock: {error}")
```

The example uses ID `170` because earlier practice lessons use that ID for a disposable product. If it does not exist in your database, the function returns `False`. Use an ID you have verified instead.

**Important:** the SQL uses `WHERE product_id = ?`. Without the condition, every product's stock could be changed.

## 7. Exercise 6 — Delete a disposable product

**Task:** Write a function that deletes one product by ID and returns `True` if a row was deleted.

### Suggested answer

```python
def delete_product(product_id):
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.execute(
            "DELETE FROM products WHERE product_id = ?",
            (product_id,),
        )

        if cursor.rowcount != 1:
            connection.rollback()
            return False

        connection.commit()
        return True

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()
```

Before using it, check the target:

```python
product = find_product(170)
print(product)
```

Only delete it if you have confirmed that it is your disposable practice record. Then:

```python
if delete_product(170):
    print("Practice product deleted.")
else:
    print("No matching product was found.")
```

Verify that `find_product(170)` returns `None` afterwards.

If ID `170` belongs to a real product in your database, do not delete it. Substitute the ID of a practice record you created.

## 8. Exercise 7 — Convert terminal input safely

**Task:** Ask the user for a price limit, convert it to a number, reject invalid input, and display matching products.

### Suggested answer

```python
def run_price_search():
    raw_value = input("Show products priced below: ").strip()

    try:
        max_price = float(raw_value)
    except ValueError:
        print("Please enter a valid number, such as 3000.")
        return

    if max_price < 0:
        print("Price limit cannot be negative.")
        return

    products = find_products_below_price(max_price)

    if not products:
        print("No products matched that price limit.")
        return

    for product_id, name, price, stock in products:
        print(f"{product_id} | {name} | ₹{price:.2f} | Stock: {stock}")
```

Call `run_price_search()` to test it. Try `3000`, then try text such as `three thousand` to see how the program handles invalid input.

This function validates the input before running the query. It also checks whether the query returned any rows.

## 9. Exercise 8 — Check persistence

**Task:** Add a disposable product, close the connection, open a new connection, and confirm that the record can be retrieved.

You can use `add_product()` and `find_product()` from earlier exercises:

```python
practice_id = add_product(
    name="Python Practice Mouse",
    category="Practice",
    price=399.00,
    stock=6,
)

print(f"Saved product ID: {practice_id}")

# find_product opens a new connection to the same database file.
saved_product = find_product(practice_id)

if saved_product is None:
    print("Persistence check failed.")
else:
    print("Persistence check passed:")
    print(saved_product)
```

Once you have verified the result, delete only that practice record:

```python
if delete_product(practice_id):
    print("Practice product cleaned up.")
```

The ID is captured from the insert, so the cleanup targets the exact record created during this test.

## 10. Complete practice script

This version combines the most important read and search functions into one runnable file. It is a compact reference for the patterns you practised above.

Save it as `Examples/python_database_practice.py`:

```python
from pathlib import Path
import sqlite3

DATABASE_PATH = Path(__file__).resolve().parent / "ecommart.db"


def list_products():
    connection = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = connection.execute(
            """
            SELECT product_id, name, category, price, stock
            FROM products
            ORDER BY product_id
            """
        )
        return cursor.fetchall()
    finally:
        connection.close()


def find_product(product_id):
    connection = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = connection.execute(
            """
            SELECT product_id, name, category, price, stock
            FROM products
            WHERE product_id = ?
            """,
            (product_id,),
        )
        return cursor.fetchone()
    finally:
        connection.close()


def find_products_below_price(max_price):
    if isinstance(max_price, bool) or not isinstance(max_price, (int, float)):
        raise ValueError("Price limit must be a number.")

    if max_price < 0:
        raise ValueError("Price limit cannot be negative.")

    connection = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = connection.execute(
            """
            SELECT product_id, name, price, stock
            FROM products
            WHERE price < ?
            ORDER BY price
            """,
            (max_price,),
        )
        return cursor.fetchall()
    finally:
        connection.close()


def main():
    try:
        print("eComMART Product Catalog")
        print("-" * 30)

        products = list_products()

        if not products:
            print("No products are currently listed.")
        else:
            for product in products:
                print(product)

        raw_value = input("\nShow products priced below: ").strip()

        try:
            max_price = float(raw_value)
        except ValueError:
            print("Please enter a valid number.")
            return

        matches = find_products_below_price(max_price)

        if not matches:
            print("No products matched.")
        else:
            print("\nMatching products:")
            for product_id, name, price, stock in matches:
                print(f"{product_id} | {name} | ₹{price:.2f} | Stock: {stock}")

    except (sqlite3.Error, ValueError) as error:
        print(f"Could not complete the request: {error}")


if __name__ == "__main__":
    main()
```

Run it from the Week 5 folder:

```bash
python "Examples/python_database_practice.py"
```

This complete script is read-only: it lists and searches records but does not insert, update, or delete anything.

## 11. Common mistakes

| Mistake | Better approach |
|---|---|
| Forgetting to close a connection | Close it in `finally` |
| Passing a string where a numeric value is expected | Convert and validate user input |
| Assuming `fetchone()` always returns a row | Check whether the result is `None` |
| Joining user input into SQL | Use parameter placeholders |
| Forgetting to commit a change | Commit only after a successful write operation |
| Reporting success when no row matched | Check `cursor.rowcount` for update/delete operations |
| Deleting a record without inspecting it | Verify the target product and use a disposable practice row |
| Catching errors without displaying any message | Show a helpful message and retain diagnostic details |

## 12. Knowledge check

1. What does `fetchall()` return?
2. What does `fetchone()` return when there is no matching row?
3. Why should values be passed separately using SQL placeholders?
4. Why should an update check `cursor.rowcount`?
5. Why must an insert be committed?
6. Why is it useful to capture the new ID returned by an insert?
7. How can you check that a saved product persists after the first connection closes?

### Answers

1. A list of the remaining result rows, usually tuples.
2. `None`.
3. Parameterization separates SQL instructions from data values and helps prevent SQL injection.
4. It helps determine whether the intended row was affected.
5. A commit makes the transaction's changes permanent.
6. The ID can be used to retrieve, update, or clean up that exact record.
7. Open a new connection to the same database file and query the product by its ID.

## 13. Lesson recap

- Python functions can wrap database queries and return useful results.
- Use parameterized SQL for values.
- Validate input before writing to the database.
- Handle missing records separately from database errors.
- Commit successful writes and roll back failed uncommitted operations.
- Test persistence by reopening the same database.
- Use disposable records for update and delete exercises.

## What comes next?

In `03_Independent_Product_Catalog_Challenge.md`, you will combine the skills from the week to build and test a small product catalog workflow with less step-by-step guidance.
