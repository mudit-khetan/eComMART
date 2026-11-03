# Guided SQL Practice

## Learning objectives

By the end of this practice lesson, you will be able to:

- Write SQL statements to retrieve, filter, sort, and summarize product records.
- Insert a new product using the `products` table schema.
- Update and delete a specific record safely.
- Explain the effect of a `WHERE` clause.
- Check query results and recognise common SQL mistakes.

This lesson is a practice set. Try each task before reading its answer. All exercises use the eComMART `products` table introduced earlier in Week 5.

## 1. Prepare the database

The core table has these columns:

| Column | Meaning |
|---|---|
| `product_id` | Unique product identifier |
| `name` | Product name |
| `category` | Product category |
| `price` | Catalog price |
| `stock` | Available units |

If you have not created the database yet, run the setup script from the `Week 5` folder:

```bash
python "Examples/setup_database.py"
```

The starter records are:

| `product_id` | `name` | `category` | `price` | `stock` |
|---:|---|---|---:|---:|
| 101 | Wireless Barcode Scanner | Scanners | 3499.00 | 24 |
| 102 | Thermal Label Roll | Shipping Supplies | 450.00 | 120 |
| 103 | USB-C Docking Station | Accessories | 6799.00 | 8 |

Your data may differ if you have already completed update or delete activities. If you need to compare answers exactly, use a fresh copy of the database created by the setup script. Do not overwrite a database containing work you want to keep.

You can practise in a SQLite tool or use Python to execute SQL. These exercises show SQL statements first so that the focus remains on SQL itself.

## 2. How to use this practice set

For each task:

1. Read the scenario.
2. Write the SQL statement without looking at the answer.
3. Run the statement against the `products` table.
4. Check the returned rows or affected-row count.
5. Compare your result with the answer and explanation.

**Safety rule:** for `UPDATE` and `DELETE`, inspect the target record with `SELECT` first. Use a disposable practice record for destructive exercises.

## 3. Level 1 — Read and understand data

### Task 1 — Display the full catalog

**Scenario:** A catalog manager wants to view all product fields.

Write a query that returns every column from `products`, ordered by `product_id` in ascending order.

**Hint:**

Use `SELECT`, `FROM`, and `ORDER BY`.

**Answer:**

```sql
SELECT product_id, name, category, price, stock
FROM products
ORDER BY product_id ASC;
```

**Explanation:** `ASC` means ascending order. It is the default for `ORDER BY`, but writing it explicitly makes the intended order clear.

### Task 2 — Show only product names and prices

**Scenario:** A buyer wants a compact price list.

Return only `name` and `price`, ordered from lowest price to highest price.

**Answer:**

```sql
SELECT name, price
FROM products
ORDER BY price ASC;
```

**Explanation:** Selecting only the required columns avoids returning information the buyer does not need.

### Task 3 — Find a product by ID

**Scenario:** An employee needs the record for product ID `102`.

Return all columns for that product.

**Answer:**

```sql
SELECT product_id, name, category, price, stock
FROM products
WHERE product_id = 102;
```

**Expected result for the original starter data:** the Thermal Label Roll record.

**Explanation:** `WHERE` filters the table to rows matching the condition. Because `product_id` is a primary key, at most one row should match.

### Task 4 — Find products below ₹3,000

**Scenario:** A buyer is preparing a list of lower-priced items.

Return `product_id`, `name`, and `price` for products costing less than `3000`.

**Answer:**

```sql
SELECT product_id, name, price
FROM products
WHERE price < 3000
ORDER BY price ASC;
```

For the original starter data, the Thermal Label Roll matches.

### Task 5 — Find products with low stock

**Scenario:** The warehouse team wants to review products with fewer than 10 units available.

Return `product_id`, `name`, and `stock`, ordered from lowest stock to highest.

**Answer:**

```sql
SELECT product_id, name, stock
FROM products
WHERE stock < 10
ORDER BY stock ASC;
```

For the original starter data, the USB-C Docking Station matches because its stock is `8`.

### Task 6 — Filter by category

**Scenario:** The catalog manager wants all products in `Accessories`.

Return all columns for matching products.

**Answer:**

```sql
SELECT product_id, name, category, price, stock
FROM products
WHERE category = 'Accessories'
ORDER BY product_id;
```

**Explanation:** SQL text values are written in single quotes. When a value comes from Python input, use a parameterized query rather than building the SQL string with concatenation.

## 4. Level 2 — Combine conditions and sort results

### Task 7 — Products in a price range

**Scenario:** A buyer wants products costing at least ₹500 but less than ₹5,000.

Return `name` and `price`.

**Answer:**

```sql
SELECT name, price
FROM products
WHERE price >= 500 AND price < 5000
ORDER BY price;
```

**Explanation:** `AND` requires both conditions to be true.

### Task 8 — Products with substantial stock or a low price

**Scenario:** A buyer wants products with at least 20 units available or a price below ₹500.

Return `name`, `price`, and `stock`.

**Answer:**

```sql
SELECT name, price, stock
FROM products
WHERE stock >= 20 OR price < 500
ORDER BY name;
```

**Explanation:** `OR` means either condition can match. The parentheses are not required here because there is only one combined pair of conditions.

### Task 9 — Search names containing “USB”

**Scenario:** A user remembers part of a product name but not the full name.

Find products whose names contain `USB`.

**Answer:**

```sql
SELECT product_id, name, price
FROM products
WHERE name LIKE '%USB%'
ORDER BY name;
```

**Explanation:** `%` matches any sequence of characters. This pattern matches text with `USB` anywhere in the name. SQLite's default `LIKE` behaviour is case-insensitive for basic ASCII letters.

### Task 10 — Display the two least expensive products

**Scenario:** A buyer wants a quick shortlist of the two lowest-priced products.

**Answer:**

```sql
SELECT product_id, name, price
FROM products
ORDER BY price ASC
LIMIT 2;
```

**Explanation:** `LIMIT 2` restricts the result to two rows after sorting.

## 5. Level 3 — Summarize data

### Task 11 — Count products

**Scenario:** The manager wants to know how many product records exist.

**Answer:**

```sql
SELECT COUNT(*) AS product_count
FROM products;
```

For the original starter data, the count is `3`.

**Explanation:** `COUNT(*)` counts rows. The alias `product_count` gives the result column a readable name.

### Task 12 — Calculate total stock

**Scenario:** The warehouse team wants the total number of units represented in the catalog.

**Answer:**

```sql
SELECT SUM(stock) AS total_stock
FROM products;
```

For the original starter data, the total is `152`.

### Task 13 — Find the average price

**Scenario:** The catalog manager wants the average price of all products.

**Answer:**

```sql
SELECT AVG(price) AS average_price
FROM products;
```

For the original starter data, the average is approximately `3582.67`.

**Explanation:** `AVG()` calculates the arithmetic mean of the non-`NULL` values in the selected column.

### Task 14 — Count products by category

**Scenario:** The manager wants to know how many products are listed in each category.

**Answer:**

```sql
SELECT category, COUNT(*) AS product_count
FROM products
GROUP BY category
ORDER BY category;
```

**Explanation:** `GROUP BY` puts rows with the same category into groups, and `COUNT(*)` counts the rows in each group.

## 6. Level 4 — Insert, update, and delete safely

These tasks change the database. Use the practice IDs described below, and do not delete or modify a starter product by accident.

### Task 15 — Insert a disposable product

**Scenario:** Add a practice product named `Practice HDMI Cable` in the `Accessories` category, priced at `599.00`, with stock of `15`.

Use product ID `180` only if it is not already in use. If it is taken, choose another unused ID and use that ID consistently in the later tasks.

**Answer:**

```sql
INSERT INTO products (product_id, name, category, price, stock)
VALUES (180, 'Practice HDMI Cable', 'Accessories', 599.00, 15);
```

Verify the insert:

```sql
SELECT product_id, name, category, price, stock
FROM products
WHERE product_id = 180;
```

**Expected result:** one row for the practice product.

If the insert reports a primary-key constraint error, ID `180` is already in use. Do not delete that unknown record. Choose a different unused ID instead.

### Task 16 — Update the practice product's stock

**Scenario:** The warehouse receives five additional units of the practice HDMI cable.

First verify the target:

```sql
SELECT product_id, name, stock
FROM products
WHERE product_id = 180;
```

Then update the stock:

```sql
UPDATE products
SET stock = 20
WHERE product_id = 180;
```

Verify it again:

```sql
SELECT product_id, name, stock
FROM products
WHERE product_id = 180;
```

The stock should now be `20`.

### Task 17 — Change the practice product's price

**Scenario:** The supplier revises the practice cable's price to ₹549.

```sql
UPDATE products
SET price = 549.00
WHERE product_id = 180;
```

Verify the price using `SELECT`. The price should now be `549.00`.

### Task 18 — Delete the practice product

**Scenario:** The practice activity is complete and the temporary product should be removed.

First inspect the record:

```sql
SELECT product_id, name
FROM products
WHERE product_id = 180;
```

Confirm that the result is the practice HDMI cable. Then delete it:

```sql
DELETE FROM products
WHERE product_id = 180;
```

Verify the deletion:

```sql
SELECT product_id, name
FROM products
WHERE product_id = 180;
```

The final query should return no rows.

If you used a different ID, substitute it in every query. Never run `DELETE FROM products;` during this exercise because it removes all rows from the table.

## 7. Python challenge — run a parameterized search

Now combine SQL with Python. Save the following as `Examples/sql_practice.py`.

```python
from pathlib import Path
import sqlite3

DATABASE_PATH = Path(__file__).resolve().parent / "ecommart.db"


def find_products_under_price(max_price):
    """Return products whose price is below the supplied limit."""
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


if __name__ == "__main__":
    try:
        raw_price = input("Show products priced below: ").strip()
        max_price = float(raw_price)

        if max_price < 0:
            print("Price limit cannot be negative.")
        else:
            products = find_products_under_price(max_price)

            if not products:
                print("No products matched that price limit.")
            else:
                for product_id, name, price, stock in products:
                    print(
                        f"{product_id} | {name} | "
                        f"₹{price:.2f} | Stock: {stock}"
                    )

    except ValueError:
        print("Please enter a valid non-negative number.")

    except sqlite3.Error as error:
        print(f"Database query failed: {error}")
```

Run it from the Week 5 folder:

```bash
python "Examples/sql_practice.py"
```

Try `3000` as the price limit. With the original sample data, the Thermal Label Roll should appear.

This script uses a parameterized query and closes its connection reliably. It also handles invalid numeric input and common SQLite errors.

## 8. Common SQL mistakes

| Mistake | Why it fails or causes risk | Correct approach |
|---|---|---|
| Forgetting `WHERE` in an update | All rows may be updated | Target the intended product ID |
| Forgetting `WHERE` in a delete | All rows may be removed | Inspect the row and specify the condition |
| Writing a text value without quotes in SQL | SQL may treat it as an identifier and report an error | Use single quotes for SQL text literals |
| Using `=` with a wildcard pattern | Wildcards work with `LIKE`, not ordinary equality | Use `LIKE '%text%'` |
| Using `AND` when either condition should match | The query may return fewer rows than intended | Use `OR` when either condition is sufficient |
| Using `fetchall()` just to count rows | Retrieves records that are not needed | Use `COUNT(*)` |
| Joining Python input into SQL | Can break the query and create injection risks | Use placeholders such as `?` |
| Assuming a query must return a row | A valid query can return no matches | Check the result before using it |

## 9. Final review challenge

Try this without looking at the answer first.

**Scenario:** The eComMART buyer wants to see the names and prices of products that cost less than ₹7,000 and have at least 10 units in stock. Show the least expensive products first, and display no more than five rows.

Write one SQL statement to solve the task.

**Suggested answer:**

```sql
SELECT name, price
FROM products
WHERE price < 7000
  AND stock >= 10
ORDER BY price ASC
LIMIT 5;
```

The query filters by both conditions, sorts the matches by price, and limits the output to five rows.

## 10. Lesson recap

You practised:

- Selecting columns and filtering rows with `WHERE`.
- Sorting results with `ORDER BY` and limiting them with `LIMIT`.
- Combining conditions with `AND` and `OR`.
- Searching text with `LIKE`.
- Summarizing records with `COUNT`, `SUM`, `AVG`, and `GROUP BY`.
- Inserting, updating, and deleting a disposable practice record.
- Calling a parameterized SQL query from Python.

## What comes next?

In `02_Guided_Python_Database_Practice.md`, you will practise connecting Python functions, SQL queries, input validation, and database result handling in small exercises.
