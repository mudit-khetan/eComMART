# Setting Up the eComMART SQLite Database

## Lesson purpose

In the previous lessons, you learned why eComMART can benefit from a database and how tables, records, data types, and keys are organized.

Now we will prepare the database that the rest of Week 5 will use. By the end of this lesson, you will have a SQLite database file containing a `products` table and a small, repeatable set of sample products.

This lesson focuses on setup and verification. We will examine SQL statements in more detail in the next lesson.

## Learning objectives

By the end of this lesson, you will be able to:

- Explain what a SQLite database file is.
- Import Python's built-in `sqlite3` module.
- Create or open a database using `sqlite3.connect()`.
- Create the `products` table if it does not already exist.
- Insert sample records without duplicating them when the setup script is rerun.
- Commit changes and close a database connection.
- Verify that the database and sample records were created successfully.
- Diagnose common setup mistakes, including accidentally creating a database in a different folder.

## 1. What we are going to create

Our database will be called `ecommart.db`. It will contain one table named `products` with the following columns:

| Column | Purpose | Example |
|---|---|---|
| `product_id` | Unique product identifier and primary key | `101` |
| `name` | Product display name | `Wireless Barcode Scanner` |
| `category` | Product category | `Scanners` |
| `price` | Product price | `3499.00` |
| `stock` | Available quantity | `24` |

We will use the same names throughout the Week 5 course. Consistent names make it easier to connect the SQL examples to the Python code later.

The setup script will create the table if it does not exist and insert a small sample catalog. It will be safe to run again: the sample IDs will not be inserted a second time.

### Important: know where your database is saved

SQLite stores its database in a file. If Python is given a relative path such as `ecommart.db`, the file is created relative to the program's current working directory—not necessarily the folder containing the Python script.

For this course, we will use a path based on the setup script's own location. This makes the example more predictable when it is run from different working directories.

## 2. Check that Python can use SQLite

Python includes the `sqlite3` module in standard installations. You do not need to install a separate SQLite server.

Run this short script:

```python
import sqlite3

print("SQLite library version:", sqlite3.sqlite_version)
```

Expected output will look similar to this (the version number may differ):

```text
SQLite library version: 3.x.x
```

If the import fails, check which Python environment you are using and ask your instructor to help verify that the installation includes `sqlite3`.

## 3. Optional tool: install DB Browser for SQLite

You can create and use the database entirely through Python. Python includes the `sqlite3` module, so **you do not need to download a separate SQL server or install a Python database package** for this course.

A graphical database tool is optional, but it can make the database easier to inspect and lets you run SQL statements in a dedicated editor. In this lesson, we will use **DB Browser for SQLite**.

Official download page: <https://sqlitebrowser.org/dl/>

### Step 1 — Choose the right download

1. Open the official download page: <https://sqlitebrowser.org/dl/>.
2. Find the downloads for your operating system.
3. Choose the appropriate current stable release for your computer:
   - **Windows:** choose the Windows installer that matches your system. Most modern Windows computers use 64-bit Windows.
   - **macOS:** choose the macOS download suitable for your Mac and follow the installation instructions provided on the download page.
   - **Linux:** follow the instructions or package options listed for your distribution.
4. Download only from the official DB Browser for SQLite website or a distribution source it explicitly recommends.

The exact download filenames may change as new releases are published. Select the current stable release rather than relying on an old filename from a screenshot or tutorial.

### Step 2 — Install and launch the application

**On Windows**

1. Open the downloaded installer.
2. Follow the installation prompts.
3. When installation finishes, launch **DB Browser for SQLite** from the Start menu.

**On macOS**

1. Open the downloaded file.
2. Follow the instructions shown for the downloaded package. If it contains an application bundle, move the application to the Applications folder when instructed.
3. Open **DB Browser for SQLite** from Applications. If macOS displays a security prompt, follow your organisation's software-installation policy and the instructions provided by the official download source.

**On Linux**

Use the installation method documented for your Linux distribution on the official download page. If you are using a managed training computer, ask your instructor or administrator if you do not have permission to install applications.

You do not need to create a database in DB Browser yet. We will generate the database with the Python setup script first.

### Step 3 — Confirm Python and SQLite are available

Open a terminal and run:

```bash
python --version
```

If your computer uses `python3`, run:

```bash
python3 --version
```

Next, check the SQLite library available to Python. Create a temporary file named `check_sqlite.py` with this code:

```python
import sqlite3

print("Python can use SQLite.")
print("SQLite library version:", sqlite3.sqlite_version)
```

Run it from the terminal:

```bash
python check_sqlite.py
```

Or use `python3 check_sqlite.py` if that is the command configured on your system.

Expected output will look similar to this; the version number can differ:

```text
Python can use SQLite.
SQLite library version: 3.x.x
```

If this works, Python can access SQLite. You do not need to install `sqlite3` with `pip`.

### Step 4 — Create the eComMART database

Use the `Examples/setup_database.py` file supplied with the course. From the main `Week 5/` folder, run:

```bash
python Examples/setup_database.py
```

If required on your computer:

```bash
python3 Examples/setup_database.py
```

The script creates the database file beside itself:

```text
Week 5/
└── Examples/
    ├── setup_database.py
    └── ecommart.db
```

The setup script creates the `products` table and adds any missing starter products. It is designed to preserve existing rows when run again. Still, read any setup script before running it, and do not use a reset script on a database containing work you want to keep.

### Step 5 — Open the database in DB Browser

1. Launch **DB Browser for SQLite**.
2. Choose **Open Database**. Depending on the version, this may be available from the toolbar or the **File** menu.
3. Browse to the `Examples` folder inside your Week 5 course folder.
4. Select `ecommart.db` and open it.
5. Select the **Browse Data** tab.
6. Choose the `products` table from the table selector.

You should see the starter product records. If you cannot find the file, check that you ran `setup_database.py` successfully and that you opened the database in the `Examples` folder—not a similarly named file elsewhere.

### Step 6 — Run your first SQL query

1. In DB Browser, open the **Execute SQL** tab.
2. Enter the query below:

```sql
SELECT product_id, name, category, price, stock
FROM products
ORDER BY product_id;
```

3. Select **Execute** (the button or control name may vary slightly by version).
4. Inspect the results grid.

You should see the three starter products:

| Product ID | Name | Category | Price | Stock |
|---:|---|---|---:|---:|
| 101 | Wireless Barcode Scanner | Scanners | 3499.00 | 24 |
| 102 | Thermal Label Roll | Shipping Supplies | 450.00 | 120 |
| 103 | USB-C Docking Station | Accessories | 6799.00 | 8 |

This query only reads data; it does not change the database.

**Try one more query:**

```sql
SELECT name, price
FROM products
WHERE price < 5000
ORDER BY price;
```

This returns products priced below 5000, sorted from lowest to highest price.

For now, use `SELECT` statements while becoming familiar with the interface. Later lessons will explain how to insert, update, and delete records. Before executing a write query, inspect it carefully and check its `WHERE` clause.

### Optional: save a query

If you want to keep a query for later, save it in a text file named `sql_practice.sql` or use the save option available in your database tool. A `.sql` file contains SQL statements; it is not the database itself. The database remains `ecommart.db`.

### If installation is not possible

You can still complete the core Week 5 lessons without DB Browser. Use the supplied Python scripts and the built-in `sqlite3` module. If your course instructor requires the graphical interface, ask for help installing it on your training machine.

---

## 4. Understand the setup sequence

Before writing the full script, understand the steps it will perform.

1. Import `sqlite3` so Python can communicate with SQLite.
2. Choose a predictable path for the database file.
3. Connect to the database. If the file does not exist at that path, SQLite creates it.
4. Create the `products` table if it does not already exist.
5. Insert the sample products only when their IDs are not already present.
6. Commit the changes so they are saved.
7. Query the table to verify the sample data.
8. Close the connection.

This order is important. The table must exist before we insert product records. Changes should be committed before we finish, and the connection should be closed when the work is complete.

## 5. Create the setup script

Inside the Week 5 `Examples/` folder, create a file named `setup_database.py`.

If the `Examples/` folder does not exist yet, create it under the main `Week 5/` folder.

Copy the following code into `setup_database.py`:

```python
"""
Create the eComMART SQLite database and insert starter products.

Run this script from any working directory:
    python setup_database.py

The database file is created beside this script:
    Examples/ecommart.db

Safety note:
    This script preserves existing product data. It creates the table if needed
    and inserts the starter products only when their product IDs do not already
    exist. It does not delete or reset existing rows.
"""

import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent / "ecommart.db"

STARTER_PRODUCTS = [
    (101, "Wireless Barcode Scanner", "Scanners", 3499.00, 24),
    (102, "Thermal Label Roll", "Shipping Supplies", 450.00, 120),
    (103, "USB-C Docking Station", "Accessories", 6799.00, 8),
]


def setup_database():
    """Create the products table and add any missing starter products."""
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    product_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    price REAL NOT NULL CHECK (price > 0),
                    stock INTEGER NOT NULL CHECK (stock >= 0)
                )
                """
            )

            connection.executemany(
                """
                INSERT OR IGNORE INTO products
                    (product_id, name, category, price, stock)
                VALUES (?, ?, ?, ?, ?)
                """,
                STARTER_PRODUCTS,
            )

        print(f"Database ready: {DATABASE_PATH}")
        print("Starter products are present. Existing product data was preserved.")

        rows = connection.execute(
            """
            SELECT product_id, name, category, price, stock
            FROM products
            ORDER BY product_id
            """
        ).fetchall()

        print(f"\nProducts currently in the database: {len(rows)}")
        for product_id, name, category, price, stock in rows:
            print(
                f"ID: {product_id} | {name} | {category} | "
                f"₹{price:,.2f} | Stock: {stock}"
            )

    except sqlite3.Error as error:
        print(f"Database setup failed: {error}")
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    setup_database()
```

This is the actual file supplied in `Examples/setup_database.py`. If you are typing the script in yourself rather than using the supplied copy, match it exactly so your output lines up with the rest of this lesson.

### Read the code before running it

The script uses a few concepts that are worth understanding now. We will study SQL statements and query execution more thoroughly in later lessons.

**`Path(__file__).resolve().parent`**

- `__file__` identifies the current Python script.
- `Path(__file__).resolve()` turns its location into a resolved path.
- `.parent` refers to the folder containing the script.

This makes `DATABASE_PATH` point to `ecommart.db` beside `setup_database.py`. For this example, both the setup script and the database file will be in `Examples/`.

**`sqlite3.connect(DATABASE_PATH)`**

This opens a connection to the database file. If the file does not exist, SQLite creates it. A connection is the object Python uses to interact with the database.

**`with connection:`**

This is SQLite's connection context manager. It commits the table-creation and insert statements together if the block finishes without an error, and rolls them back if an exception occurs inside the block. It does not close the connection — that is still done explicitly in `finally`. You will look at this distinction more closely in the Python integration lessons.

**`CREATE TABLE IF NOT EXISTS`**

This asks SQLite to create the table only if a table with that name does not already exist. It lets us rerun the setup script without trying to create the same table again.

**`product_id INTEGER PRIMARY KEY`**

This defines `product_id` as the table's primary key. SQLite will not allow two rows to have the same primary-key value.

**`NOT NULL`**

This says the field must have a value. It does not, by itself, ensure a value is sensible — only that one was supplied.

**`CHECK (price > 0)` and `CHECK (stock >= 0)`**

A `CHECK` constraint asks SQLite to reject a row that fails the given condition. Here, SQLite will refuse to insert or update a product with a price of zero or less, or with negative stock. This gives the database itself a basic data-quality rule, in addition to any validation the Python application performs.

**Question-mark placeholders (`?`)**

The insert statement uses placeholders for values. The actual product values are supplied separately through `executemany()`. This is a parameterized operation; it avoids building SQL by concatenating values into the SQL text.

**`INSERT OR IGNORE`**

For this teaching setup, SQLite skips a sample insert when it would violate a constraint such as the primary key. Because the sample products use fixed IDs, rerunning the script will not create duplicate rows for those IDs.

This simple seeding strategy is suitable for the initial exercise. It does not update an existing product if you later change the sample values in the script. We will discuss more deliberate update behavior when learning SQL and application logic.

**`finally` and `close()`**

The `finally` block runs whether the operation succeeds or raises an error. Closing the connection releases the database connection after the script has finished.

## 6. Run the setup script

Open a terminal in the main `Week 5/` folder and run:

```bash
python Examples/setup_database.py
```

If your system uses `python3` to launch Python, run:

```bash
python3 Examples/setup_database.py
```

Use the command that matches the Python environment configured for your course.

### Expected output

The full path will depend on your computer. The output should look similar to this:

```text
Database ready: /.../Week 5/Examples/ecommart.db
Starter products are present. Existing product data was preserved.

Products currently in the database: 3
ID: 101 | Wireless Barcode Scanner | Scanners | ₹3,499.00 | Stock: 24
ID: 102 | Thermal Label Roll | Shipping Supplies | ₹450.00 | Stock: 120
ID: 103 | USB-C Docking Station | Accessories | ₹6,799.00 | Stock: 8
```

The path will differ on your computer. The formatted price (`₹3,499.00`) comes from the `f"₹{price:,.2f}"` formatting in the script; the value stored in the database is the plain number `3499.0`.

### What should have happened?

- Python opened or created `Examples/ecommart.db`.
- SQLite created the `products` table if needed.
- The three sample products were inserted if their IDs were not already present.
- The script committed its changes.
- The verification query retrieved the products and printed them.
- The connection was closed.

## 6. Verify that rerunning the script is safe

Run the same command again:

```bash
python Examples/setup_database.py
```

You should still see three product records, not six.

Why? The setup script uses stable product IDs and `INSERT OR IGNORE`. When it encounters an existing primary-key value, SQLite skips that insert instead of adding another row with the same ID.

This property is useful for setup scripts because learners and developers often need to run them more than once. It also makes the exercise repeatable.

**Do not delete the database file after every run.** Keeping the file lets you verify that later lessons are working with the same database.

## 7. Common problems and how to troubleshoot them

### Problem: `ModuleNotFoundError: No module named 'sqlite3'`

Python installations normally include `sqlite3`, but the environment may be incomplete or unusual.

**Try this:** Confirm which Python interpreter you are running. Use the Python environment recommended by your instructor and ask for help repairing or replacing it if necessary. Do not install an unrelated database server to solve this import problem.

### Problem: `python: command not found`

Your terminal may use `python3` instead of `python`.

**Try this:**

```bash
python3 Examples/setup_database.py
```

If that also fails, check that Python is installed and available in your terminal.

### Problem: the database seems to lose data

SQLite can create a new database file when the path points to a location where no database exists. If a program uses a relative path, running it from another working directory may cause it to open a different file.

**In this lesson:** `DATABASE_PATH` is built from the setup script's location, so it consistently points to `Examples/ecommart.db`. Read the printed path and verify that later examples use the same database file.

### Problem: the table already exists

That is expected when rerunning this script. `CREATE TABLE IF NOT EXISTS` prevents an error when the table already exists.

### Problem: a product is missing after you edited the sample data

`INSERT OR IGNORE` does not update an existing row with the same primary-key value. It skips a conflicting insert. If you change a sample product's name or price in the script, the existing database record will remain unchanged.

For this introductory setup, use the provided sample data as-is. Later lessons will teach you how to update existing records intentionally.

## 8. Guided practice

Complete these tasks after the setup script runs successfully.

### Task A — Confirm the table contents

1. Run `setup_database.py`.
2. Count the product records printed.
3. Confirm that product IDs `101`, `102`, and `103` are present.
4. Confirm that the USB-C Docking Station has stock `8`.

**Expected result:** Three products are printed, and the USB-C Docking Station's stock is `8`.

### Task B — Test repeatability

1. Run the script a second time.
2. Compare the product count with the first run.
3. Explain why the count does not increase.

**Expected result:** The count remains three because the script ignores duplicate sample IDs.

### Task C — Locate the database file

1. Read the `Database ready:` path printed by the script.
2. Open the `Examples/` folder in your project.
3. Confirm that `ecommart.db` exists there.

**Expected result:** The database file is alongside `setup_database.py`.

## 9. Check your understanding

1. What does `sqlite3.connect()` do?
2. Why does the script use `CREATE TABLE IF NOT EXISTS`?
3. Why does it use `INSERT OR IGNORE` for the sample records?
4. What does the `with connection:` block do in this script?
5. Why is the database path based on the script's location?
6. If you change the sample price in the script and run it again, will `INSERT OR IGNORE` update the existing product? Why or why not?
7. What would happen if you tried to insert a product with a price of `0`?

### Suggested answers

1. It opens a connection to the specified SQLite database file, creating the file if it does not exist.
2. It lets the script run again without failing because the table already exists.
3. It prevents duplicate sample records with the same primary-key IDs from being inserted.
4. It commits the table-creation and insert statements together if no error occurs inside the block, and rolls them back if one does.
5. It helps the script consistently use the database stored beside the script, regardless of the terminal's working directory.
6. No. The existing primary-key value causes the insert to be ignored. A separate update operation would be needed to change the existing record.
7. SQLite would reject it. The `CHECK (price > 0)` constraint on the `price` column does not allow a price of zero or less.

## 10. Recap and transition

You have created the starting point for the Week 5 database project.

You now know how to:

- Check that Python can import `sqlite3`.
- Create or open a SQLite database file.
- Create the `products` table if needed.
- Insert sample data without duplicating the fixed sample IDs.
- Commit changes and close the connection.
- Verify the records and locate the database file.

The database is now ready for the next stage: learning SQL statements deliberately, instead of treating the setup script as a black box.

**Next lesson:** `02_Creating_Tables_and_Inserting_Products.md`

Next, we will study how `CREATE TABLE` and `INSERT` work, including the structure of a SQL statement and how values are placed into columns.
