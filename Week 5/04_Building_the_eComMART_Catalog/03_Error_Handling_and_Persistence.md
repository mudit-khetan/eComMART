# Error Handling and Persistence

## Learning objectives

By the end of this lesson, you will be able to:

- Explain why database applications need error handling.
- Distinguish invalid input from database errors and missing records.
- Handle common SQLite failures without hiding useful information.
- Explain why committed changes remain available after a program exits.
- Verify that product changes persist between program runs.
- Test failure cases without damaging the starter catalog.

## 1. Why reliability matters

Your eComMART catalog can now create, read, update, and delete products. But a useful application must do more than work when every input is correct.

Consider these situations:

- Someone enters a price as text instead of a number.
- A product lookup uses an ID that does not exist.
- A database file is missing or cannot be opened.
- A database operation fails before the change is committed.
- A product is added successfully, but the user is unsure whether the change was saved.

A reliable program should respond to these situations clearly. It should not report success when an operation failed, and it should not hide the information needed to diagnose a problem.

This lesson improves the CRUD backend from `02_Implementing_Product_CRUD_Operations.md`.

## 2. Three kinds of outcomes

It helps to distinguish between three different situations.

| Situation | Example | Appropriate response |
|---|---|---|
| Invalid input | A user enters a negative stock quantity | Reject the value and explain what is allowed |
| Missing record | Product ID `999999` is not in the table | Report that no matching product was found |
| Database error | The database file cannot be opened or a SQL statement fails | Handle the exception and provide a useful error message |

These situations should not all be treated as the same failure.

For example, a product ID that does not exist is a normal result of a search. It does not necessarily mean SQLite has failed. Similarly, a negative stock value can be rejected before a database operation is attempted.

## 3. Handle invalid user input

Python's `input()` function always returns text. If a user enters `3000`, the program receives the string `"3000"` rather than the integer `3000` or float `3000.0`.

Convert input explicitly and catch conversion errors.

```python
def read_price():
    """Ask for a non-negative price and return it as a float."""
    while True:
        raw_value = input("Enter product price: ").strip()

        try:
            price = float(raw_value)
        except ValueError:
            print("Please enter a valid number, such as 2999.00.")
            continue

        if price < 0:
            print("Price cannot be negative.")
            continue

        return price
```

### How it works

1. The program asks for a price.
2. `float(raw_value)` attempts to convert the text into a number.
3. If conversion fails, Python raises `ValueError`; the program displays a message and asks again.
4. If the price is negative, the program rejects it.
5. Only a valid, non-negative number is returned.

You can use the same pattern for stock, but convert it with `int()` and reject negative values. This keeps text such as `"five"` from reaching the database function as stock.

```python
def read_stock():
    """Ask for a non-negative whole number."""
    while True:
        raw_value = input("Enter stock quantity: ").strip()

        try:
            stock = int(raw_value)
        except ValueError:
            print("Please enter a whole number, such as 12.")
            continue

        if stock < 0:
            print("Stock cannot be negative.")
            continue

        return stock
```

The validation in the CRUD functions is still useful. Input conversion handles values entered through the menu, while function-level validation protects the backend if another part of the program calls it directly.

## 4. Handle missing records clearly

The read function from the previous lesson returns `None` when it cannot find a product. The calling code should check for that result before trying to display the record.

```python
product_id = 999999
product = get_product_by_id(product_id)

if product is None:
    print(f"No product found with ID {product_id}.")
else:
    print(product)
```

If the ID is not present, the program displays a helpful message. It does not need to raise a database exception for this normal case.

Update and delete functions can return `False` when no matching row was affected:

```python
updated = update_product(
    product_id=999999,
    name="Example Product",
    category="Accessories",
    price=299.00,
    stock=10,
)

if updated:
    print("Product updated.")
else:
    print("Update skipped: no matching product was found.")
```

This example assumes that the `update_product()` function from the previous lesson is available in the same module or has been imported. Its validation rules still apply.

## 5. Catch database errors without hiding them

SQLite operations can raise exceptions derived from `sqlite3.Error`. For example, a query may refer to a table that does not exist, or the program may be unable to open the database file.

At the application boundary, catch expected errors and show a useful message:

```python
import sqlite3


try:
    products = get_all_products()
    print(f"Loaded {len(products)} products.")

except sqlite3.Error as error:
    print(f"Could not read the product catalog: {error}")
```

This tells the user that the operation failed while preserving the error message for diagnosis.

Do not use an empty `except` block:

```python
# Avoid this pattern:
try:
    products = get_all_products()
except sqlite3.Error:
    pass
```

Silently ignoring an error makes it difficult to know why the catalog did not load. The application may continue as if everything worked, even though no data was retrieved.

Also avoid catching every possible exception unless there is a clear reason. Handle the errors you expect, and let unexpected programming errors remain visible during development.

## 6. Understand persistence

A database is useful because the records are stored beyond the lifetime of a single Python process.

**Persistence** means that saved data remains available after the program finishes and is started again.

For the eComMART project:

- `ecommart.db` is the file that stores the SQLite database.
- A successful insert or update must be committed to save the change.
- Closing the Python script does not erase committed records.
- Opening the same database file in a later run lets the program read the saved records again.

This differs from a normal Python list. A list created in memory disappears when the process ends unless you explicitly save its contents somewhere.

## 7. Test persistence with a disposable product

Use a product that is safe to create and delete. The example below creates a record, commits it, and closes the connection. It then opens a new connection and checks that the record still exists.

Save this as `Examples/persistence_check.py`:

```python
from pathlib import Path
import sqlite3

DATABASE_PATH = Path(__file__).resolve().parent / "ecommart.db"


def main():
    practice_name = "Persistence Test Adapter"
    practice_category = "Practice"
    practice_price = 199.00
    practice_stock = 4

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.execute(
            """
            INSERT INTO products (name, category, price, stock)
            VALUES (?, ?, ?, ?)
            """,
            (
                practice_name,
                practice_category,
                practice_price,
                practice_stock,
            ),
        )

        practice_id = cursor.lastrowid
        connection.commit()
        print(f"Saved practice product with ID {practice_id}.")

    except sqlite3.Error as error:
        connection.rollback()
        print(f"Could not save practice product: {error}")
        return

    finally:
        connection.close()

    # Open a new connection to verify that the committed record remains.
    check_connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = check_connection.execute(
            """
            SELECT product_id, name, category, price, stock
            FROM products
            WHERE product_id = ?
            """,
            (practice_id,),
        )
        product = cursor.fetchone()

        if product is None:
            print("Persistence check failed: record was not found.")
        else:
            print("Persistence check passed:")
            print(product)

    finally:
        check_connection.close()


if __name__ == "__main__":
    main()
```

Run it from the Week 5 folder:

```bash
python "Examples/persistence_check.py"
```

The output should confirm that the practice product was saved and then retrieved through a separate connection. The assigned ID may differ each time you run the script.

**Important:** each successful run adds another practice product. After verifying the result, remove the specific practice record using the ID printed by the script, or extend the script with a cleanup step if you want it to clean up automatically. Do not delete records by guessing an ID.

## 8. Clean up the practice record safely

If you want the persistence test to remove its own temporary record after verification, add this code after the verification block, once `check_connection` has been closed:

```python
cleanup_connection = sqlite3.connect(DATABASE_PATH)

try:
    cursor = cleanup_connection.execute(
        "DELETE FROM products WHERE product_id = ?",
        (practice_id,),
    )

    cleanup_connection.commit()

    if cursor.rowcount == 1:
        print("Practice record cleaned up.")
    else:
        print("Practice record was already missing.")

except sqlite3.Error as error:
    cleanup_connection.rollback()
    print(f"Could not clean up practice record: {error}")

finally:
    cleanup_connection.close()
```

This uses the ID assigned during the current run, so it targets only the record created by the test. If you add this cleanup block to the script, rerunning it will create, verify, and then remove a practice record each time.

## 9. Understand commit and rollback in failure cases

When you modify data, use a transaction so that the application can save successful changes or undo changes that have not been committed.

A simplified pattern is:

```python
connection = sqlite3.connect(DATABASE_PATH)

try:
    connection.execute(
        "UPDATE products SET stock = ? WHERE product_id = ?",
        (6, 170),
    )

    connection.commit()
    print("Change saved.")

except sqlite3.Error as error:
    connection.rollback()
    print(f"Change failed: {error}")

finally:
    connection.close()
```

This example updates product ID `170`, so use it only if that is the intended practice record. If the ID does not exist, SQLite does not necessarily raise an error: an update that matches zero rows is valid SQL. For that reason, code should check `cursor.rowcount` when it needs to confirm that a record was actually changed.

For operations that involve multiple related updates, perform all required changes in the same transaction and commit only after they succeed. If a database error occurs before the commit, roll back the uncommitted work.

**Key distinction:** a rollback cannot undo a change that has already been committed. Make the commit decision at the right point in the operation.

## 10. A safer wrapper for a database operation

The following function demonstrates a reusable pattern for updating stock. It validates the value, checks the matching row, commits on success, rolls back on a database error, and closes the connection.

```python
from pathlib import Path
import sqlite3

DATABASE_PATH = Path(__file__).resolve().parent / "ecommart.db"


def set_product_stock(product_id, new_stock):
    """Set stock for one product; return True if a row was affected."""
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

Example use:

```python
try:
    if set_product_stock(170, 12):
        print("Stock was updated.")
    else:
        print("No matching product was found.")

except (ValueError, sqlite3.Error) as error:
    print(f"Could not update stock: {error}")
```

The example uses practice product ID `170`. Replace it with a confirmed product ID if needed. The caller distinguishes a missing record (`False`) from an error (`ValueError` or `sqlite3.Error`).

## 11. Common errors and fixes

| Problem | Likely cause | What to do |
|---|---|---|
| `ValueError` when converting price or stock | The input is not in the expected numeric format | Ask again and show an example of valid input |
| `no such table: products` | The script opened an empty or incorrect database file | Run the setup script and check the database path |
| A lookup returns `None` | No row matches the supplied ID | Show a not-found message |
| Update reports success but the value looks unchanged | The new value may equal the old value | Verify the current record and understand what `rowcount` reports |
| Data disappears after a test | The transaction may not have been committed, or a different database file was opened | Check `commit()` and confirm the path |
| Duplicate practice products appear | The persistence test was run multiple times | Use the printed ID for cleanup or add the cleanup block |
| Errors are hidden | The code catches exceptions without reporting them | Display a helpful message and preserve the error details during development |
| The wrong product is deleted | The target ID was not checked | Query the record before deletion and use the exact ID |

## 12. Guided practice

### Task A — Handle invalid numeric input

Write a function that asks for a non-negative stock quantity. It should reject text that cannot be converted to an integer and reject negative numbers.

### Task B — Check a missing product

Look up a product ID that you know does not exist. Display a message when the returned value is `None`.

### Task C — Verify persistence

Add a disposable product using a parameterized insert and commit it. Close the connection, open a new connection, and query the product by the ID assigned by SQLite.

### Task D — Clean up safely

Delete only the record created by Task C. Use its exact returned ID and check `rowcount` before reporting success.

### Suggested approach

- Use `try`/`except ValueError` around input conversion.
- Use `if product is None` for a missing lookup.
- Commit after the insert succeeds.
- Open a new connection for the persistence check.
- Use the saved ID in the cleanup query and close each connection.

## 13. Knowledge check

1. What is persistence?
2. Why should a program catch `ValueError` when converting user input?
3. Is a missing product always a database error?
4. Why must a successful insert or update be committed?
5. What does `rollback()` do?
6. Why is it important to check the database path?
7. Why should errors not be silently ignored?

### Answers

1. Saved data remains available after the program ends and is started again.
2. The user may enter text that cannot be converted to the required number type.
3. No. A query that returns no matching record is a normal result that the program should handle.
4. A commit makes the transaction's changes permanent.
5. It undoes uncommitted changes in the current transaction.
6. A wrong path can cause the program to open or create a different, empty database file.
7. Silent failures make it difficult to diagnose problems and may cause the application to report incorrect results.

## 14. Lesson recap

- Handle invalid input, missing records, and database errors differently.
- Convert user input deliberately and validate it before saving.
- Use `None` or a documented status to represent a missing record.
- Catch expected database exceptions and provide useful messages.
- Commit changes that should persist and roll back failed, uncommitted operations.
- Verify persistence by reopening the same database file and querying the saved record.
- Test with disposable data and clean it up using the exact ID created by the test.

## What comes next?

In `04_Preparing_for_Agentic_AI.md`, you will see how the persistence, state, and error-handling ideas from this lesson connect to how AI agents remember information across a task. Then, in `05_Practice_and_Review/01_Guided_SQL_Practice.md`, you will review the SQL skills from this week with a structured set of exercises using the eComMART `products` table.
