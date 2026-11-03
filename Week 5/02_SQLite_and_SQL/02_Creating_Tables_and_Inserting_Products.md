# Creating Tables and Inserting Products

## Lesson purpose

In the previous lesson, you created the starting SQLite database and prepared the sample eComMART catalog. This lesson takes a closer look at the SQL statements that define a table and add records to it.

You will learn how a SQL statement is structured, how table definitions describe columns and rules, and how `INSERT` adds product records. You will also practise checking what happened instead of assuming a command succeeded.

> **Before you begin:** Run `Examples/setup_database.py` from the Week 5 project. This lesson uses the database file created by that script. The setup script stores `ecommart.db` beside itself in `Examples/`.

## Learning objectives

By the end of this lesson, you will be able to:

- Explain what SQL is and how a SQL statement is structured.
- Read a basic `CREATE TABLE` statement.
- Explain the purpose of column types and constraints such as `PRIMARY KEY` and `NOT NULL`.
- Explain how SQLite stores date and time values, and why that matters for comparing and sorting them.
- Insert a new product using `INSERT INTO`.
- Distinguish inserting a new record from updating an existing record.
- Use a query to verify whether data was inserted.
- Recognize common insertion errors.

## 1. What is SQL?

**SQL** stands for **Structured Query Language**. It is used to define and work with data in relational databases.

Python is the programming language we use to build the application. SQL is the language we use to describe database operations.

For example, Python can decide that a new product needs to be added. The SQL statement describes which table should receive the product and which values should be stored.

SQL keywords are often written in uppercase to make statements easier to read. SQLite does not require uppercase keywords; `SELECT` and `select` are treated the same way.

## 2. Understand the table definition

The setup script creates the `products` table with this statement:

```sql
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
);
```

Let's read it piece by piece.

- `CREATE TABLE` tells SQLite to define a new table.
- `IF NOT EXISTS` means SQLite should not raise a table-already-exists error if a table named `products` is already present.
- `products` is the table name.
- The parentheses contain the column definitions.
- `INTEGER`, `TEXT`, and `REAL` express the intended kinds of values.
- `PRIMARY KEY` makes `product_id` the chosen unique identifier.
- `NOT NULL` means a value must be supplied for that column.

The semicolon marks the end of the SQL statement. In Python's `sqlite3` interface, a trailing semicolon is commonly used for readability, though it is not always required when passing a single statement to a method.

### Why use `IF NOT EXISTS`?

Our setup script may be run more than once. Without `IF NOT EXISTS`, trying to create an already existing table would normally cause an error.

This clause only prevents the table-already-exists error. It does **not** modify an existing table to match a changed definition. If the schema needs to change later, we must handle that change deliberately.

### What constraints do we have?

A **constraint** is a rule the database enforces on stored data.

In this table:

- `PRIMARY KEY` prevents duplicate or missing primary-key identifiers.
- `NOT NULL` prevents a column from being left without a value.

These rules do not cover every possible business requirement. For example, `price REAL NOT NULL` still does not say that price must be greater than or equal to zero. We can add a `CHECK` constraint for that in a later refinement, but we will keep the first table definition simple while learning the basics.

### A note on dates and times

The `products` table does not currently store a date or time anywhere, but you will see date and time values often enough in real applications that it is worth understanding how SQLite handles them now, while column types are fresh.

**SQLite has no dedicated `DATE` or `DATETIME` storage type.** Unlike `INTEGER`, `TEXT`, and `REAL`, there is no separate type SQLite uses internally to store dates. Instead, the usual approach is to store a date or timestamp as `TEXT`, written in the ISO 8601 format: `YYYY-MM-DD` for a date, or `YYYY-MM-DD HH:MM:SS` for a date and time.

For example, if eComMART wanted to record when each product was added to the catalog, the column could be declared like this:

```sql
added_on TEXT NOT NULL
```

It is declared as `TEXT`, not `DATE`, because `DATE` is not an actual SQLite storage type. (SQLite will technically accept `DATE` or `DATETIME` as a column type name without raising an error, but it stores the value as plain text regardless — the keyword does not change how SQLite treats the data.)

**Why ISO 8601 (`YYYY-MM-DD`) and not a format like `DD/MM/YYYY`?**

Because it is stored as plain text, SQLite compares and sorts dates the same way it compares any other text: character by character, left to right. The ISO 8601 format was chosen specifically because this works out correctly for dates — the year comes first, then the month, then the day, so sorting the text alphabetically also sorts it chronologically.

```sql
-- Works correctly, because ISO 8601 text sorts the same way dates do:
SELECT name, added_on
FROM products
ORDER BY added_on;
```

A format like `DD/MM/YYYY` would sort incorrectly, because `"25/01/2026"` would be treated as alphabetically earlier than `"03/02/2026"`, even though January 25 comes before February 3. Always use `YYYY-MM-DD` (optionally followed by `HH:MM:SS`) for any date or time column.

**Letting SQLite fill in the current time**

SQLite provides a built-in value, `CURRENT_TIMESTAMP`, that inserts the current date and time automatically:

```sql
INSERT INTO products (product_id, name, category, price, stock, added_on)
VALUES (104, 'Ethernet Switch', 'Networking', 2499.00, 15, CURRENT_TIMESTAMP);
```

This stores a value such as `'2026-10-30 09:15:42'` — the current date and time, in UTC, as plain text in the ISO 8601 format described above.

This course's `products` table does not include a date column, so you will not use `CURRENT_TIMESTAMP` in the core project. It is shown here so that when you do need to record a date or time in a future project, you will know the recommended format and why it matters.

## 3. Read the current product data

The setup script creates three sample products. Before adding another product, let's see how SQL retrieves existing records.

```sql
SELECT product_id, name, category, price, stock
FROM products
ORDER BY product_id;
```

Read the statement from top to bottom:

- `SELECT` names the columns to return.
- `FROM products` identifies the table to read.
- `ORDER BY product_id` sorts the returned rows by product ID.

The query should return the three sample products:

| product_id | name | category | price | stock |
|---:|---|---|---:|---:|
| 101 | Wireless Barcode Scanner | Scanners | 3499.00 | 24 |
| 102 | Thermal Label Roll | Shipping Supplies | 450.00 | 120 |
| 103 | USB-C Docking Station | Accessories | 6799.00 | 8 |

This query is included here so you can verify changes in the following sections. We will explore retrieval and filtering in more depth in a later lesson.

## 4. Insert a new product with `INSERT`

Suppose eComMART begins selling a new product: an **Ethernet Switch**, in the **Networking** category, priced at ₹2,499, with 15 units in stock. We will assign it product ID `104`.

The SQL statement is:

```sql
INSERT INTO products (product_id, name, category, price, stock)
VALUES (104, 'Ethernet Switch', 'Networking', 2499.00, 15);
```

Understand each part:

- `INSERT INTO products` names the table that will receive the new record.
- The column list tells SQLite which fields we are supplying.
- `VALUES` introduces the values for those columns.
- The values must correspond to the columns in the same order.

The first value, `104`, belongs to `product_id`; the second value belongs to `name`; and so on.

Text values use single quotation marks in SQL. Numeric values such as `2499.00` and `15` are written without quotation marks.

### Why list the column names?

Listing the columns makes the statement explicit and easier to maintain. If the table later gains another column, a statement that names its target columns is clearer than one that relies on an implicit column order.

For this lesson, we will always name the columns in our `INSERT` statements.

## 5. Run the insert from Python

You can experiment with the SQL statement using Python's `sqlite3` module. Create a temporary practice file named `insert_product_practice.py` inside `Examples/`. This file is for learning the insert operation; it uses the same database path as the setup script.

```python
from pathlib import Path
import sqlite3

SCRIPT_DIR = Path(__file__).resolve().parent
DATABASE_PATH = SCRIPT_DIR / "ecommart.db"

new_product = (104, "Ethernet Switch", "Networking", 2499.00, 15)

with sqlite3.connect(DATABASE_PATH) as connection:
    connection.execute(
        """
        INSERT INTO products (product_id, name, category, price, stock)
        VALUES (?, ?, ?, ?, ?)
        """,
        new_product,
    )

print("Insert completed.")
```

### Walkthrough

**1. Locate the same database**

```python
SCRIPT_DIR = Path(__file__).resolve().parent
DATABASE_PATH = SCRIPT_DIR / "ecommart.db"
```

The practice script is inside `Examples/`, so this path points to the database created by `setup_database.py`. Keeping the path consistent avoids accidentally writing to a second database file.

**2. Store the values in a tuple**

```python
new_product = (104, "Ethernet Switch", "Networking", 2499.00, 15)
```

The tuple holds the values in the same order as the columns in the SQL statement.

**3. Use placeholders**

```sql
VALUES (?, ?, ?, ?, ?)
```

Each question mark is a placeholder for one supplied value. The tuple is passed separately to `execute()`. This is called a **parameterized query**. It is safer and clearer than building SQL by joining strings, especially when values come from users.

**4. Use a connection context manager**

```python
with sqlite3.connect(DATABASE_PATH) as connection:
```

For Python's SQLite connection, the context manager commits the transaction if the block succeeds and rolls it back if an exception escapes the block. It does not automatically close the connection when the block ends; in this short script, the connection object is cleaned up after it is no longer referenced. In later lessons, we will use explicit connection management where it makes the lifecycle clearer.

### Important: the insert is not safe to run repeatedly

The practice statement uses the fixed ID `104`. After the first successful run, that ID already exists. Running the same script again will raise an integrity error because the primary key must be unique.

That is intentional for this demonstration: `INSERT` adds a new record; it does not update an existing one. If you need repeatable setup data, use the supplied `setup_database.py`, which uses `INSERT OR IGNORE` for its fixed sample IDs. If you want to change an existing product, you will learn to use `UPDATE` in a later lesson.

If you need to repeat this particular practice, either use a different unused ID and suitable product values, or reset the practice database according to your instructor's instructions. Do not delete a database containing work you want to keep.

## 6. Verify that the new product exists

After running the insert script once, verify the result using this SQL query:

```sql
SELECT product_id, name, category, price, stock
FROM products
WHERE product_id = 104;
```

`WHERE product_id = 104` restricts the result to the product with ID `104`. We will study filtering in detail in the next retrieval lesson.

The expected row is:

| product_id | name | category | price | stock |
|---:|---|---|---:|---:|
| 104 | Ethernet Switch | Networking | 2499.00 | 15 |

If the query returns the row, the new product was inserted. If it returns no rows, check that the insert script ran against the intended database and that it completed without an error.

The practice script prints `Insert completed.` after its connection block finishes. Use the verification query as well; a message alone does not show you which values were stored.

## 7. Common insertion errors

### Error: `UNIQUE constraint failed: products.product_id`

**What it means:** The product ID you tried to insert already exists.

**Why it happens:** The primary key must be unique. You may have run the same practice script twice.

**What to do:** Use a new unused ID when adding a genuinely new product. If the intention is to change an existing product, use `UPDATE` rather than `INSERT`.

### Error: `NOT NULL constraint failed`

**What it means:** A required column was given a missing value.

**Why it happens:** The table declares fields such as `name` and `price` as `NOT NULL`.

**What to do:** Supply a valid value for every required column. Do not use an empty or missing value as a substitute for information that the table requires.

### Error: the values appear in the wrong columns

**What it means:** The values may have been supplied in a different order from the column list.

**What to do:** Compare the column list with the values one by one. Listing columns explicitly and using a consistently ordered tuple makes this easier to check.

### Error: the product cannot be found after insertion

**Possible cause:** The script may have opened a different database file.

**What to do:** Check `DATABASE_PATH` in the script and confirm it points to `Examples/ecommart.db`, the same file used by `setup_database.py`.

## 8. Guided practice

Complete the tasks in order.

### Task A — Read the table definition

In your own words, explain what each of these parts does:

1. `product_id INTEGER PRIMARY KEY`
2. `name TEXT NOT NULL`
3. `CREATE TABLE IF NOT EXISTS`

**Suggested answers**

1. It defines an integer identifier as the primary key.
2. It defines a text field that must have a value.
3. It creates the table only if it does not already exist.

### Task B — Plan a new product record

A new product is added to the catalog:

- Product ID: `105`
- Name: `Wireless Presenter`
- Category: `Accessories`
- Price: `1799.00`
- Stock: `12`

Write an `INSERT INTO` statement that names all five columns and supplies the values in the correct order.

**Suggested answer**

```sql
INSERT INTO products (product_id, name, category, price, stock)
VALUES (105, 'Wireless Presenter', 'Accessories', 1799.00, 12);
```

Do not run this statement if you have already used ID `105` for another practice record in your database.

### Task C — Verify your planned record

Write a `SELECT` query that would return only the product whose ID is `105`.

**Suggested answer**

```sql
SELECT product_id, name, category, price, stock
FROM products
WHERE product_id = 105;
```

## 9. Check your understanding

1. What does `INSERT INTO` do?
2. Why is it good practice to list the target columns in an insert statement?
3. Why are placeholders (`?`) used in the Python example?
4. Why does rerunning the insert for ID `104` cause an error?
5. What is the difference between `INSERT` and `UPDATE`?
6. Why should you verify an inserted record with a query?
7. Why should a date be stored in `YYYY-MM-DD` format rather than `DD/MM/YYYY`?

### Suggested answers

1. It adds a new row to a table.
2. It makes the intended mapping between columns and values explicit.
3. They separate SQL structure from the supplied values and support parameterized queries.
4. The primary key `104` already exists, and primary-key values must be unique.
5. `INSERT` creates a new row; `UPDATE` changes values in an existing row.
6. Verification confirms that the expected record and values are present in the intended database.
7. SQLite stores dates as plain text and sorts them the same way it sorts any text, character by character. `YYYY-MM-DD` sorts correctly because the year comes first; a format like `DD/MM/YYYY` would sort alphabetically rather than chronologically.

## 10. Recap and transition

You have learned how a table is defined and how a new product record is inserted.

Remember:

- `CREATE TABLE` defines the table's columns and rules.
- `PRIMARY KEY` identifies records uniquely.
- `NOT NULL` requires a value for a column.
- SQLite has no dedicated date/time type; dates are stored as `TEXT` in `YYYY-MM-DD` (or `YYYY-MM-DD HH:MM:SS`) format so they sort and compare correctly.
- `INSERT INTO` adds a new record.
- Listing columns explicitly makes inserts easier to read.
- Parameterized queries keep values separate from SQL text.
- A verification query helps confirm that the intended record was stored.

**Next lesson:** `03_Retrieving_and_Filtering_Products.md`

Next, we will learn how to retrieve selected columns, filter records with `WHERE`, combine conditions, and sort the results to answer everyday eComMART catalog questions.
