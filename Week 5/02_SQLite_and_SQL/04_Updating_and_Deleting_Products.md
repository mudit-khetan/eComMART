# Updating and Deleting Products with SQL

## Learning objectives

By the end of this lesson, you will be able to:

- Explain when to use `UPDATE` and `DELETE`.
- Change values in an existing product record.
- Remove a specific product record.
- Use a `WHERE` clause to target the intended row.
- Verify a change before and after running a statement.
- Recognize why an unrestricted `UPDATE` or `DELETE` can damage a table.

## 1. The eComMART scenario

In the previous lesson, you learned how to retrieve product information using `SELECT` and narrow the results with `WHERE`. A catalog also needs a way to keep information accurate.

For example, an eComMART employee might need to:

- Correct a product's price.
- Record a change in available stock.
- Remove a product that should no longer be listed.

SQL uses two statements for these tasks:

| Statement | Purpose | Example |
|---|---|---|
| `UPDATE` | Changes values in existing records | Correct a product's stock |
| `DELETE` | Removes records from a table | Remove a discontinued product |

These statements change the database. Unlike `SELECT`, they do not simply display information.

## 2. Review the table

The lessons use one core table named `products`:

| Column | Meaning | Example |
|---|---|---|
| `product_id` | Unique identifier for a product | `101` |
| `name` | Product name | `Wireless Barcode Scanner` |
| `category` | Product category | `Scanners` |
| `price` | Price in the catalog | `3499.0` |
| `stock` | Number of units available | `24` |

The initial sample database contains these products:

| `product_id` | `name` | `category` | `price` | `stock` |
|---:|---|---|---:|---:|
| 101 | Wireless Barcode Scanner | Scanners | 3499.0 | 24 |
| 102 | Thermal Label Roll | Shipping Supplies | 450.0 | 120 |
| 103 | USB-C Docking Station | Accessories | 6799.0 | 8 |

Your database may contain extra rows if you added products during an earlier practice activity. The examples below use product IDs to identify records precisely.

## 3. Updating a product

### 3.1 Understand the structure

The general form of an `UPDATE` statement is:

```sql
UPDATE table_name
SET column_name = new_value
WHERE condition;
```

- `UPDATE products` identifies the table to change.
- `SET stock = 3` assigns a new value to the `stock` column.
- `WHERE product_id = 103` identifies the product that should be changed.

The `WHERE` clause is critical. It tells SQLite which records should be affected.

### 3.2 Example: correct the stock quantity

Suppose the warehouse team confirms that only three USB-C docking stations are available. First, inspect the current record:

```sql
SELECT product_id, name, stock
FROM products
WHERE product_id = 103;
```

Expected result before the update, if the database has not been changed:

| `product_id` | `name` | `stock` |
|---:|---|---:|
| 103 | USB-C Docking Station | 8 |

Now update the stock:

```sql
UPDATE products
SET stock = 3
WHERE product_id = 103;
```

Verify the change by running the same `SELECT` statement again. The expected stock value is now `3`.

**Important:** this example changes the shared practice database. If you want to preserve the original sample data for later lessons, use the disposable practice product in Section 5 instead.

### 3.3 Change more than one column

You can update several columns in one statement by separating assignments with commas:

```sql
UPDATE products
SET price = 6999.00,
    stock = 10
WHERE product_id = 103;
```

This changes both `price` and `stock` for product 103. It does not change the product's name or category.

Use this only when both new values are correct for your scenario. Do not run it merely to follow along if you want to keep the original sample values.

### 3.4 What happens without `WHERE`?

Consider this statement:

```sql
UPDATE products
SET stock = 0;
```

There is no condition to select a particular product. SQLite therefore sets the stock to zero for **every row** in `products`.

That may be appropriate for a carefully planned operation in a special situation, but it is not what you want when correcting one product. When practising, include a `WHERE` clause and check the condition before running the statement.

## 4. Deleting a product

### 4.1 Understand the structure

The general form is:

```sql
DELETE FROM table_name
WHERE condition;
```

For example:

```sql
DELETE FROM products
WHERE product_id = 150;
```

This removes the record whose `product_id` is `150`, if that record exists.

A deletion removes the entire row, not just one column. If you only need to change the stock or price, use `UPDATE` instead.

### 4.2 Check before deleting

Before deleting a row, inspect the target:

```sql
SELECT product_id, name, category, price, stock
FROM products
WHERE product_id = 150;
```

Confirm that the result is the disposable practice record you intended to remove. Then run:

```sql
DELETE FROM products
WHERE product_id = 150;
```

Finally, run the `SELECT` statement again. If the deletion worked, it should return no rows for ID `150`.

### 4.3 What happens without `WHERE`?

```sql
DELETE FROM products;
```

This removes **all rows** from the `products` table. The table structure remains, but the product records are gone.

Do not run this statement during the lesson. It is shown to explain the risk of leaving out the condition.

## 5. Guided practice: add, update, and delete a disposable product

This activity uses product ID `150` so you can practise changes without altering the three original sample products. If ID `150` is already in your database, choose another unused ID and substitute it consistently in every statement below.

**A note on practice IDs across Week 5:** different lessons in this course use different disposable IDs for their own practice activities (for example, `150` here, `160`/`161` later in the Python transactions lesson, and others in the Practice and Review section). This is deliberate, so that completing one lesson's practice activity does not leave behind a record that collides with a later lesson's practice ID. You do not need to delete a practice record from an earlier lesson before starting a new one, as long as each lesson's instructions are followed using its own stated ID.

### Step 1 — Add the practice product

```sql
INSERT INTO products (product_id, name, category, price, stock)
VALUES (150, 'Practice Ethernet Switch', 'Networking', 2499.00, 12);
```

If you receive a primary-key error, that ID is already in use. Choose another unused ID rather than deleting an existing product.

### Step 2 — Verify the new row

```sql
SELECT product_id, name, price, stock
FROM products
WHERE product_id = 150;
```

You should see the practice product with a price of `2499.0` and stock of `12`.

### Step 3 — Update the price

Suppose the supplier sends a revised price of ₹2,299:

```sql
UPDATE products
SET price = 2299.00
WHERE product_id = 150;
```

Verify it:

```sql
SELECT product_id, name, price
FROM products
WHERE product_id = 150;
```

The price should now be `2299.0`.

### Step 4 — Update the stock

Suppose the warehouse receives five more units:

```sql
UPDATE products
SET stock = 17
WHERE product_id = 150;
```

Verify the new stock with a `SELECT` query. It should be `17`.

### Step 5 — Delete only the practice product

First check the row:

```sql
SELECT product_id, name
FROM products
WHERE product_id = 150;
```

After confirming that it is your practice product, delete it:

```sql
DELETE FROM products
WHERE product_id = 150;
```

Verify the deletion:

```sql
SELECT product_id, name
FROM products
WHERE product_id = 150;
```

The final query should return no rows. The original sample products should still be present and unchanged.

If you used a different ID, replace `150` in all the statements above with your chosen ID.

## 6. Using UPDATE and DELETE from Python

When Python executes SQL statements, use placeholders for values instead of combining SQL and user input into a string. The next lessons explore Python database connections in more detail; this short example previews the pattern.

Save this as `Examples/update_product.py` if you want to run it from the course's `Examples` folder. It assumes you have already run `setup_database.py`, which creates `ecommart.db` in that same folder.

```python
from pathlib import Path
import sqlite3

DATABASE_PATH = Path(__file__).resolve().parent / "ecommart.db"


def update_product_stock(product_id: int, new_stock: int) -> None:
    """Update stock for one product and report whether a row was affected."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.execute(
            """
            UPDATE products
            SET stock = ?
            WHERE product_id = ?
            """,
            (new_stock, product_id),
        )

        if cursor.rowcount == 1:
            print(f"Updated stock for product {product_id}.")
        else:
            print(f"No product found with ID {product_id}.")


def delete_product(product_id: int) -> None:
    """Delete one product by its ID."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.execute(
            "DELETE FROM products WHERE product_id = ?",
            (product_id,),
        )

        if cursor.rowcount == 1:
            print(f"Deleted product {product_id}.")
        else:
            print(f"No product found with ID {product_id}.")


if __name__ == "__main__":
    # This updates the sample record with ID 103.
    # Change the ID or use the disposable practice record if preferred.
    update_product_stock(product_id=103, new_stock=3)

    # Delete only the disposable practice record, if you created it.
    # This does nothing if ID 150 does not exist.
    delete_product(product_id=150)
```

### Read the Python example

- `DATABASE_PATH` points to the database file beside this script, so the script does not depend on the terminal's current folder.
- `?` is a parameter placeholder. The tuple supplies the values in the same order as the placeholders.
- `WHERE product_id = ?` limits the operation to the selected ID.
- `cursor.rowcount` reports how many rows the statement affected. In this example, `1` means one row was affected; `0` means no matching row was found.
- The `with sqlite3.connect(...) as connection:` block commits successful changes when the block exits normally and rolls back a transaction if an exception escapes it. The connection context manager does **not** close the connection by itself; for a short script like this, Python will clean up the connection when it is no longer referenced, but explicit closing is preferable in longer-lived applications. You will learn a clearer connection-management pattern in the Python integration lessons.

**Before running:** the example updates product 103's stock to `3`. If you want to keep your sample database unchanged, change the call to use the disposable product ID you created in Section 5, or comment out the `update_product_stock(...)` line. The delete call targets only ID `150`.

Run from the course folder or any directory using the script path:

```bash
python "Examples/update_product.py"
```

If your system uses `python3`, run:

```bash
python3 "Examples/update_product.py"
```

## 7. Common mistakes and how to avoid them

| Mistake | What can happen | Safer approach |
|---|---|---|
| Forgetting `WHERE` in `UPDATE` | Every row may receive the new value | Include and inspect a condition |
| Forgetting `WHERE` in `DELETE` | Every row may be removed | Preview the target with `SELECT` first |
| Using the wrong product ID | The wrong record may change or no row may match | Query by ID before changing data |
| Putting text values in SQL without quotes | SQL syntax errors may occur | Use single quotes in SQL literals, or parameters from Python |
| Building SQL by concatenating user input | Can cause errors and SQL injection risks | Use parameterized queries |
| Assuming a successful statement changed a row | The condition may match no records | Check the result with `SELECT` or inspect `rowcount` |

## 8. Knowledge check

Try to answer these before checking the explanations.

1. Which SQL statement changes a product's price?
2. Why is `WHERE product_id = 102` important in an update?
3. What happens if you run `DELETE FROM products;` without a `WHERE` clause?
4. How can you confirm that an update worked?
5. Why is `WHERE product_id = ?` with a parameter safer than constructing a query with string concatenation?

### Answers

1. `UPDATE`.
2. It targets the product with ID `102` rather than changing every row.
3. All product records are deleted, while the table itself remains.
4. Run a `SELECT` query for the affected record, or inspect the affected-row count in Python.
5. Parameters keep values separate from SQL syntax and help prevent SQL injection.

## 9. Lesson recap

- Use `UPDATE` to change one or more column values in existing records.
- Use `DELETE` to remove a record.
- A carefully chosen `WHERE` clause helps target the intended product.
- Preview the target record before a destructive operation and verify the result afterward.
- In Python, use parameterized SQL rather than concatenating input into query strings.
- Practise with a disposable row so the original sample data remains available for later lessons.

## What comes next?

In `01_Connecting_Python_to_SQLite.md`, you will learn how Python opens a SQLite database, what a connection and cursor do, and how to manage database access in a small application.
