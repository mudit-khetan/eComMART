# Start Here — Week 5 Examples
## Python Database Integration with SQLite

Welcome! This folder contains the example files for Week 5. They will help you learn how Python works with a database by building a simple product catalogue for **eComMART**, a fictional B2B online store.

You do not need previous database experience. Follow the steps in order, run one example at a time, and compare your results with the expected results in the guide.

---

## What will you learn?

By using these examples, you will learn how to:

- Understand a database table, its rows, columns, and primary key.
- Create and inspect a small SQLite database.
- Use SQL to read, add, update, and delete product records.
- Connect a Python program to a database.
- Check that saved data remains available after a program closes.

## 1. Know your files

| File | What it is for | What to do with it |
|---|---|---|
| `START_HERE.md` | This guide. | Read it first and follow the steps below. |
| `setup_database.py` | Creates the database table and adds starter products. | Run it once to prepare your database. |
| `ecommart.db` | The database file containing the product data. | Open it with DB Browser for SQLite. It is not a Python script. |
| `01_Understand_the_Database.md` | Explains the table and its columns in beginner-friendly language. | Read it before practising SQL. |
| `02_SQL_Query_Examples.sql` | Contains labelled SQL examples. | Run one statement at a time in DB Browser for SQLite. |
| `03_SQL_Explained.md` | Explains what the SQL statements do and what results to expect. | Read it alongside the SQL examples. |
| `04_Python_Database_Example.py` | A small Python example that connects to SQLite and reads product data. | Run it after creating the database. |
| `05_Product_Catalog_App.py` | A larger example that brings the database concepts together. | Run it after you understand the smaller example. |

If a file listed here has not yet been supplied, continue with the files you have and return to that step when it becomes available.

### What do the file extensions mean?

- `.md` — a written guide or explanation.
- `.py` — a Python program.
- `.sql` — SQL commands for a database.
- `.db` — the database file itself.

---

## 2. Before you begin

You will need:

1. **Python 3** installed on your computer.
2. A code editor, such as **Visual Studio Code**.
3. **DB Browser for SQLite** (recommended), which lets you view database tables and run SQL visually.

### Check Python

Open a terminal in Visual Studio Code by choosing **Terminal → New Terminal**.

Run:

```bash
python --version
```

If that command is not recognised, try:

```bash
python3 --version
```

A Python 3 version number should appear.

### Check SQLite support

Run one of these commands:

```bash
python -c "import sqlite3; print(sqlite3.sqlite_version)"
```

or:

```bash
python3 -c "import sqlite3; print(sqlite3.sqlite_version)"
```

If a version number appears, Python can use SQLite. You do not need to install `sqlite3` separately.

### Install DB Browser for SQLite

1. Visit the official website: https://sqlitebrowser.org/
2. Download the version for your operating system.
3. Install and open the application.

---

## 3. Follow this learning path

### Step 1 — Prepare the database

Open the `Examples` folder in Visual Studio Code. Keep the example files together in this folder.

In the terminal, run the command for your system.

**Windows:**

```bash
python setup_database.py
```

**macOS or Linux:**

```bash
python3 setup_database.py
```

The script should create the `products` table and show the starter products. It should also create `ecommart.db` in the `Examples` folder.

### Step 2 — Check the starter data

The database starts with these sample products:

| Product ID | Product name | Category | Price | Stock |
|---:|---|---|---:|---:|
| 101 | Wireless Barcode Scanner | Scanners | 3499.00 | 24 |
| 102 | Thermal Label Roll | Shipping Supplies | 450.00 | 120 |
| 103 | USB-C Docking Station | Accessories | 6799.00 | 8 |

Your terminal output may format prices differently, but the values should match.

### Step 3 — Open the database visually

1. Open DB Browser for SQLite.
2. Click **Open Database**.
3. Select `ecommart.db` from the `Examples` folder.
4. Choose **Browse Data**.
5. Select the `products` table.

You should see the same three products. If the database file is missing, return to Step 1 and run the setup script.

### Step 4 — Understand the table

Open `01_Understand_the_Database.md`. Learn what each column means and why `product_id` identifies each product uniquely.

### Step 5 — Practise SQL

Read `03_SQL_Explained.md`, then open `02_SQL_Query_Examples.sql`.

In DB Browser, choose **Execute SQL** and copy one complete statement at a time into the SQL editor. Execute it and inspect the result before moving to the next statement.

**Important:** `UPDATE` and `DELETE` can change or remove data. Read each statement carefully and check its `WHERE` clause. Do not run all statements at once unless your instructor specifically tells you to.

### Step 6 — Run the small Python example

After creating the database, run:

**Windows:**

```bash
python 04_Python_Database_Example.py
```

**macOS or Linux:**

```bash
python3 04_Python_Database_Example.py
```

The program should connect to the database and display product information. Read the code and notice how Python sends a query to SQLite and reads the returned rows.

### Step 7 — Run the product catalogue application

When you understand the smaller example, run:

**Windows:**

```bash
python 05_Product_Catalog_App.py
```

**macOS or Linux:**

```bash
python3 05_Product_Catalog_App.py
```

Follow the prompts displayed by the program. The exact actions available depend on the version of the application supplied with your course.

---

## 4. How to run SQL safely

These four SQL commands are especially important:

| Command | Purpose |
|---|---|
| `SELECT` | Reads records without changing them. |
| `INSERT` | Adds a new record. |
| `UPDATE` | Changes existing records. |
| `DELETE` | Removes records. |

For example, this query only reads product names and prices:

```sql
SELECT name, price
FROM products;
```

This statement changes the stock for product 101 only:

```sql
UPDATE products
SET stock = 25
WHERE product_id = 101;
```

Without the `WHERE` clause, the update would affect every product. The same risk applies to a `DELETE` statement without a suitable `WHERE` clause.

Unless a lesson specifically asks you to modify a starter product, practise with a temporary product created for that purpose.

---

## 5. Check that your changes were saved

A database can preserve data after a Python program closes. This is called **persistence**.

To check it:

1. Run a program that makes a permitted change.
2. Exit the program.
3. Run it again, or open `ecommart.db` in DB Browser.
4. Check whether the change is still present.

If you changed data in DB Browser, you may need to click **Write Changes** to save it. Always review your changes before saving.

---

## 6. Troubleshooting

### `python` is not recognised

Try `python3`. If neither command works, install Python 3 and open a new terminal.

### `ecommart.db` is missing

Run `setup_database.py` first. Make sure you are using the `Examples` folder containing the script.

### `no such table: products`

You may have opened a different database file, or setup did not complete successfully. Run the setup script and open the database from the same folder as the Python examples.

### SQL changes do not appear

Confirm that DB Browser and Python are using the same `ecommart.db` file. Refresh or reopen the database view. If you edited data in DB Browser, check whether **Write Changes** is required.

### A Python example cannot find a file

Check that the terminal is open in the `Examples` folder and that the required file is present. Use the exact filename shown in the command.

### You see an error you do not understand

Copy the complete error message and note which command you ran. Sharing both with your instructor is much more useful than sharing only a screenshot of the final line.

---

## 7. Completion checklist

Before you finish, check that you can:

- [ ] Explain what each example file is for.
- [ ] Run `setup_database.py`.
- [ ] Find and open `ecommart.db`.
- [ ] View the `products` table in DB Browser.
- [ ] Run a `SELECT` query and understand its result.
- [ ] Explain the difference between `SELECT`, `INSERT`, `UPDATE`, and `DELETE`.
- [ ] Run the small Python database example.
- [ ] Run the product catalogue application, if it has been supplied.
- [ ] Explain how a database preserves data after a program closes.

## 8. Key terms

- **Database:** An organised place to store and manage data.
- **Table:** Related data arranged in rows and columns.
- **Record / row:** One entry in a table, such as one product.
- **Column:** One type of information, such as product name.
- **Primary key:** A value that uniquely identifies a row.
- **Query:** A request sent to a database.
- **Persistence:** Data remains saved after a program stops running.

You do not need to memorise everything immediately. Use this guide as a reference while you work through the Week 5 lessons.
