# Week 5 Solutions: SQL and Python Database Practice

**Week 5 · Practice and Review · Reference Solutions**

This file provides reference solutions for the Week 5 practice activities. Try each task independently before comparing your work. Your code does not have to match these examples exactly; it should meet the same requirements and produce the correct results.

The examples use the eComMART `products` table:

```sql
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
);
```

Starter products:

| Product ID | Name | Category | Price | Stock |
|---:|---|---|---:|---:|
| 101 | Wireless Barcode Scanner | Scanners | 3499.00 | 24 |
| 102 | Thermal Label Roll | Shipping Supplies | 450.00 | 120 |
| 103 | USB-C Docking Station | Accessories | 6799.00 | 8 |

> **Important:** These are teaching examples, not a single script to paste together. Some snippets assume that the table already exists. Run the setup script first, and use a disposable practice product for update/delete exercises.

---

## 1. Guided SQL practice — reference answers

### Task 1: Retrieve all products

```sql
SELECT product_id, name, category, price, stock
FROM products
ORDER BY product_id;
```

Why it works:
- `SELECT` specifies which columns to return.
- `FROM products` identifies the table.
- `ORDER BY product_id` makes the output predictable.

### Task 2: Find products in one category

```sql
SELECT product_id, name, category, price, stock
FROM products
WHERE category = 'Accessories'
ORDER BY name;
```

Text comparisons use quotes around the text value.

### Task 3: Find products below a price limit

```sql
SELECT product_id, name, price
FROM products
WHERE price < 5000
ORDER BY price;
```

The comparison operator `<` excludes products priced exactly at 5000.

### Task 4: Find products that need restocking

```sql
SELECT product_id, name, stock
FROM products
WHERE stock < 10
ORDER BY stock;
```

With the starter data, USB-C Docking Station appears because its stock is 8.

### Task 5: Add a practice product

```sql
INSERT INTO products (name, category, price, stock)
VALUES ('Practice USB Hub', 'Accessories', 1299.00, 15);
```

Because `product_id` is an `INTEGER PRIMARY KEY`, SQLite can assign the ID automatically. Check the inserted row with a `SELECT` query.

### Task 6: Update the practice product

```sql
UPDATE products
SET price = 1199.00, stock = 20
WHERE name = 'Practice USB Hub';
```

Always include a suitable `WHERE` clause. Without it, every row could be updated.

For a repeatable classroom exercise, use the product's actual ID in the `WHERE` clause once you have retrieved it.

### Task 7: Delete the practice product

```sql
DELETE FROM products
WHERE name = 'Practice USB Hub';
```

Delete only a disposable practice row. Check the result with `SELECT` afterward.

---

## 2. Guided Python database practice — reference patterns

### Connect to the database

Save Python examples inside the `Examples` directory. This path points to the database beside the Python file:

```python
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent / "ecommart.db"

def get_connection():
    return sqlite3.connect(DATABASE_PATH)
```

A successful call returns a SQLite connection. Remember that connecting to a new filename can create a new, empty database file. Confirm that the path is correct if your expected products are missing.

### Read and display products

```python
def view_all_products():
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT product_id, name, category, price, stock
            FROM products
            ORDER BY product_id
        """)
        products = cursor.fetchall()

        if not products:
            print("No products found.")
            return

        for product_id, name, category, price, stock in products:
            print(
                f"ID: {product_id} | "
                f"Name: {name} | "
                f"Category: {category} | "
                f"Price: ₹{price:,.2f} | "
                f"Stock: {stock}"
            )
    finally:
        connection.close()
```

`fetchall()` returns all matching rows as a list of tuples. Each tuple follows the column order in the `SELECT` statement.

### Retrieve one product by ID

```python
def get_product_by_id(product_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT product_id, name, category, price, stock
            FROM products
            WHERE product_id = ?
            """,
            (product_id,)
        )
        return cursor.fetchone()
    finally:
        connection.close()
```

The trailing comma in `(product_id,)` is important: it creates a one-item tuple. The `?` placeholder keeps the supplied value separate from the SQL text.

### Insert a product safely

```python
def add_product(name, category, price, stock):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO products (name, category, price, stock)
            VALUES (?, ?, ?, ?)
            """,
            (name, category, price, stock)
        )
        connection.commit()
        print(f"Product added with ID {cursor.lastrowid}.")
        return cursor.lastrowid
    except sqlite3.Error as error:
        connection.rollback()
        print(f"Could not add product: {error}")
        return None
    finally:
        connection.close()
```

`commit()` saves the change. `rollback()` cancels an uncommitted transaction if a database error occurs. The connection is closed in `finally`, including when an error is raised.

This function assumes the caller has already validated `name`, `category`, `price`, and `stock`.

### Update a product

```python
def update_product(product_id, name, category, price, stock):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE products
            SET name = ?, category = ?, price = ?, stock = ?
            WHERE product_id = ?
            """,
            (name, category, price, stock, product_id)
        )

        if cursor.rowcount == 0:
            connection.rollback()
            print(f"No product found with ID {product_id}.")
            return False

        connection.commit()
        print(f"Product {product_id} updated.")
        return True
    except sqlite3.Error as error:
        connection.rollback()
        print(f"Could not update product: {error}")
        return False
    finally:
        connection.close()
```

The `WHERE product_id = ?` clause limits the update to one product. `rowcount` helps determine whether any row matched the ID.

### Delete a product

```python
def delete_product(product_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM products WHERE product_id = ?",
            (product_id,)
        )

        if cursor.rowcount == 0:
            connection.rollback()
            print(f"No product found with ID {product_id}.")
            return False

        connection.commit()
        print(f"Product {product_id} deleted.")
        return True
    except sqlite3.Error as error:
        connection.rollback()
        print(f"Could not delete product: {error}")
        return False
    finally:
        connection.close()
```

Ask for user confirmation in the menu code before calling this function.

---

## 3. Validation patterns

Database constraints help protect stored data, but the application should also provide clear messages before attempting a write.

### Validate text

```python
name = input("Product name: ").strip()

if not name:
    print("Product name cannot be blank.")
```

Use the same idea for category.

### Validate price

```python
try:
    price = float(input("Price: "))

    if price <= 0:
        print("Price must be greater than zero.")
except ValueError:
    print("Enter a valid numeric price.")
```

### Validate stock

```python
try:
    stock = int(input("Stock quantity: "))

    if stock < 0:
        print("Stock cannot be negative.")
except ValueError:
    print("Stock must be a whole number.")
```

These snippets show the validation logic. In a complete program, place the logic in helper functions or repeat it carefully for both add and update operations.

---

## 4. Independent product catalog — implementation guidance

For the independent challenge, use these responsibilities:

| Function | Responsibility |
|---|---|
| `get_connection()` | Return a connection to the correct database file |
| `view_all_products()` | Retrieve and display every product |
| `get_product_by_id(product_id)` | Return one matching row, or `None` |
| `add_product(...)` | Insert a validated product |
| `update_product(...)` | Update an existing product |
| `delete_product(product_id)` | Delete a product when requested and confirmed |
| `main()` | Display the menu and dispatch user choices |

A clear menu loop follows this general pattern:

```python
def main():
    while True:
        print("\n========== eComMART Product Catalog ==========")
        print("1. View all products")
        print("2. Search for a product by ID")
        print("3. Add a product")
        print("4. Update a product")
        print("5. Delete a product")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_all_products()
        elif choice == "2":
            # Read an ID, validate it, then search.
            pass
        elif choice == "3":
            # Collect and validate product details, then add.
            pass
        elif choice == "4":
            # Collect an ID and replacement details, then update.
            pass
        elif choice == "5":
            # Collect an ID and ask for confirmation before deleting.
            pass
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Choose a number from 1 to 6.")


if __name__ == "__main__":
    main()
```

The `pass` statements are deliberate placeholders in this outline. Replace each one with the required interaction. Do not leave them in the finished program.

### Test the application

At minimum, verify that:

1. The three starter products can be listed.
2. Searching for ID `101` finds Wireless Barcode Scanner.
3. Searching for ID `999` reports that no product was found.
4. A valid practice product can be added.
5. Blank names, blank categories, invalid prices, and invalid stock values are rejected.
6. An existing product can be updated.
7. An unknown ID is not accidentally inserted during an update.
8. Cancelling a deletion leaves the product unchanged.
9. Confirming a deletion removes the selected practice product.
10. Changes remain after you close and reopen the application.

Use a disposable practice product for destructive tests.

---

## 5. Common mistakes and how to correct them

| Mistake | Why it causes trouble | Correction |
|---|---|---|
| Forgetting `commit()` | A change may not be saved as intended | Commit after a successful write |
| Using a different database path | The program may open a new empty database | Build the path from `__file__` |
| Omitting `WHERE` from `UPDATE` or `DELETE` | More rows than intended can be changed | Filter by the target product ID |
| Writing SQL with string concatenation | User input can alter the SQL statement | Use `?` placeholders and a tuple of values |
| Passing `(product_id)` instead of `(product_id,)` | The former is an integer in parentheses, not a tuple | Include the trailing comma |
| Treating `fetchone()` as a guaranteed row | It returns `None` when no row matches | Check for `None` before displaying fields |
| Assuming a connection context manager closes the connection | SQLite's context manager handles transactions, not automatic closing | Close connections explicitly, such as in `finally` |
| Catching every exception without explanation | Real programming errors become difficult to diagnose | Catch expected errors and display a useful message |

---

## 6. Final review

Before you consider the work complete, confirm:

- [ ] I can explain the difference between a file and a database.
- [ ] I understand tables, rows, columns, and primary keys.
- [ ] I can write basic `SELECT`, `INSERT`, `UPDATE`, and `DELETE` statements.
- [ ] I can connect Python to SQLite and read query results.
- [ ] I use parameterized SQL for user-supplied values.
- [ ] I validate input and handle missing records.
- [ ] I close connections reliably.
- [ ] I tested persistence by restarting the application.
- [ ] I can explain what happens from menu input through to the database result.

If you can explain the code rather than only run it, you are ready to move from guided practice to building small database-backed Python applications.
