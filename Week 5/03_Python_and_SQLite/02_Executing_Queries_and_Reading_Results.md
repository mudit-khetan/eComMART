# Executing Queries and Reading Results

## Learning objectives

By the end of this lesson, you will be able to:

- Execute `SELECT` queries from Python using SQLite.
- Retrieve and interpret rows returned by a query.
- Use query results in conditions, loops, and calculations.
- Filter and sort database records using SQL.
- Understand the difference between a row, a tuple, and a list of rows.
- Handle queries that return no matching records.
- Organize related database queries into small, reusable functions.

## 1. From a query to Python logic

In `01_Connecting_Python_to_SQLite.md`, you opened the eComMART database, executed a `SELECT` statement, and read the returned rows. Now you will use that pattern to build useful catalog behaviour.

Imagine an eComMART employee wants to:

- View the full product catalog.
- Find products in the `Accessories` category.
- Find products that cost less than ₹3,000.
- Check whether a product ID exists.
- Calculate the total number of units currently listed in the catalog.

SQL is responsible for selecting the records. Python can then display, inspect, count, or process the results.

Rather than writing a separate throwaway script for each of these, this lesson builds one small function per task. By the end, you will combine them into a single program, the way a real application organizes related database operations.

## 2. Confirm the database path

Save this lesson's examples in `Examples/` so they can reuse the database created by `setup_database.py`.

```text
Week 5/
└── Examples/
    ├── setup_database.py
    ├── ecommart.db
    └── query_products.py
```

If `ecommart.db` does not exist, first run the setup script from the Week 5 folder:

```bash
python "Examples/setup_database.py"
```

Create a file named `Examples/query_products.py`. At the top, use this path pattern:

```python
from pathlib import Path
import sqlite3

DATABASE_PATH = Path(__file__).resolve().parent / "ecommart.db"
```

This points to the database file beside the script, rather than relying on whichever folder the terminal happens to be using.

Every function in this lesson is added to this same `query_products.py` file, one at a time. By the end of the lesson, the file will contain all of them together.

## 3. Show the full catalog

Add this function to `query_products.py`:

```python
def show_all_products():
    """Print every product in the catalog, ordered by product ID."""
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.execute(
            """
            SELECT product_id, name, category, price, stock
            FROM products
            ORDER BY product_id
            """
        )

        products = cursor.fetchall()

        if not products:
            print("The catalog has no products yet.")
            return

        print("eComMART Product Catalog")
        print("=" * 40)

        for product in products:
            product_id, name, category, price, stock = product
            print(f"{product_id} | {name} | {category} | ₹{price:.2f} | Stock: {stock}")

    finally:
        connection.close()
```

Call it for now by adding this at the bottom of the file, so you can test as you go:

```python
if __name__ == "__main__":
    show_all_products()
```

Run it:

```bash
python "Examples/query_products.py"
```

If the database still contains only the three original sample records, the output will look like this:

```text
eComMART Product Catalog
========================================
101 | Wireless Barcode Scanner | Scanners | ₹3499.00 | Stock: 24
102 | Thermal Label Roll | Shipping Supplies | ₹450.00 | Stock: 120
103 | USB-C Docking Station | Accessories | ₹6799.00 | Stock: 8
```

The exact output depends on your current database contents.

### Understand the result structure

The line `products = cursor.fetchall()` returns a **list of rows**. Each row is typically a **tuple**. The tuple values follow the order of the columns in your `SELECT` statement.

For example, one returned row may be represented as:

```python
(101, "Wireless Barcode Scanner", "Scanners", 3499.0, 24)
```

Because the query selected five columns, that tuple contains five values:

| Position | Column | Example value |
|---:|---|---|
| `product[0]` | `product_id` | `101` |
| `product[1]` | `name` | `"Wireless Barcode Scanner"` |
| `product[2]` | `category` | `"Scanners"` |
| `product[3]` | `price` | `3499.0` |
| `product[4]` | `stock` | `24` |

The example unpacks the tuple into named variables. This is often easier to read than repeatedly using numeric positions.

### A note on accessing columns by name

Throughout this course, you will unpack rows positionally, either into named variables (as above) or by index, such as `product[1]` for the name. This matches the plain tuples that `sqlite3` returns by default, and it is a reliable pattern as long as your variable names stay in the same order as your `SELECT` statement's columns.

SQLite also offers a way to access a row's values by column name instead of position, using `sqlite3.Row`:

```python
connection = sqlite3.connect(DATABASE_PATH)
connection.row_factory = sqlite3.Row

cursor = connection.execute(
    "SELECT product_id, name, price FROM products WHERE product_id = ?",
    (101,),
)
row = cursor.fetchone()

print(row["name"], row["price"])   # access by column name
print(row[0], row[1])              # positional access still works too
```

Setting `connection.row_factory = sqlite3.Row` once, right after opening the connection, is enough to make every row returned by that connection behave this way. You do not need to use this pattern for this course — the tuple-unpacking style used throughout is simpler while you are learning, and it is what the guided practice and the independent challenge expect. It is mentioned here so that if you see `row["column_name"]` in other code or documentation, you will recognize what it does and why someone might prefer it: it protects code from breaking if a `SELECT` statement's column order changes later.

## 4. Filter records with `WHERE`

SQL can filter the rows before Python receives them. This is generally preferable to fetching every row and then filtering a large result in Python.

Add these three functions to `query_products.py`, below `show_all_products()`.

### Find products by category

```python
def find_products_by_category(category):
    """Print products that belong to the given category."""
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.execute(
            """
            SELECT product_id, name, price
            FROM products
            WHERE category = ?
            ORDER BY product_id
            """,
            (category,),
        )

        print(f"\nProducts in category '{category}':")
        found = False
        for product in cursor.fetchall():
            found = True
            print(product)

        if not found:
            print("No products found in this category.")

    finally:
        connection.close()
```

If the original sample data is unchanged, calling `find_products_by_category("Accessories")` returns product 103, the USB-C Docking Station.

The `?` placeholder marks a value supplied separately. The tuple `(category,)` contains one parameter; the comma makes it a one-item tuple.

### Find products below a given price

```python
def find_products_below_price(max_price):
    """Print products priced below the given amount."""
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.execute(
            """
            SELECT product_id, name, price
            FROM products
            WHERE price < ?
            ORDER BY price
            """,
            (max_price,),
        )

        print(f"\nProducts priced below ₹{max_price:.2f}:")
        found = False
        for product in cursor.fetchall():
            found = True
            print(product)

        if not found:
            print("No products found below this price.")

    finally:
        connection.close()
```

With the original sample data, calling `find_products_below_price(3000)` returns the Thermal Label Roll, because its price is ₹450.00. The other two sample products cost more than ₹3,000.

### Find products with low stock

```python
def find_low_stock_products(threshold):
    """Print products with stock below the given threshold."""
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.execute(
            """
            SELECT product_id, name, stock
            FROM products
            WHERE stock < ?
            ORDER BY stock
            """,
            (threshold,),
        )

        print(f"\nProducts with stock below {threshold}:")
        found = False
        for product in cursor.fetchall():
            found = True
            print(product)

        if not found:
            print("No products match this stock threshold.")

    finally:
        connection.close()
```

With the original data, calling `find_low_stock_products(10)` returns product 103, because its stock is `8`.

**Remember:** the SQL statement determines which rows are returned. Python only receives and processes those matching rows.

## 5. Read a single row with `fetchone()`

When you search by a unique `product_id`, you usually expect zero or one matching row. `fetchone()` is suitable for this case.

Add this function to `query_products.py`:

```python
def find_product_by_id(product_id):
    """Print one product's full details, or a not-found message."""
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

        product = cursor.fetchone()

        print(f"\nLooking up product ID {product_id}:")
        if product is None:
            print(f"No product found with ID {product_id}.")
        else:
            pid, name, category, price, stock = product
            print(f"Product: {name}")
            print(f"Category: {category}")
            print(f"Price: ₹{price:.2f}")
            print(f"Stock: {stock}")

    finally:
        connection.close()
```

Calling `find_product_by_id(102)` prints its name, category, price, and stock, since product 102 exists in the original sample data. Calling `find_product_by_id(999)` prints a not-found message instead, because `fetchone()` returns `None` when no row matches.

### Why check for `None`?

A database query can execute successfully and still find no matching record. No matching record is not necessarily an error. Your Python code should decide what to do in that situation.

## 6. Count results and calculate values

Python can process the values returned by SQL. For example, you can count rows or calculate the total stock represented in the catalog.

### Count products in a category

The simplest approach is to retrieve matching rows and count them in Python:

```python
cursor = connection.execute(
    "SELECT product_id FROM products WHERE category = ?",
    ("Accessories",),
)
products = cursor.fetchall()

print(f"Number of products: {len(products)}")
```

For a simple count, SQL can do this directly with `COUNT(*)`, which is usually the more efficient choice when you only need a count, not the individual product records. Add this function to `query_products.py`:

```python
def count_products_in_category(category):
    """Print how many products exist in the given category."""
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.execute(
            "SELECT COUNT(*) FROM products WHERE category = ?",
            (category,),
        )
        count = cursor.fetchone()[0]
        print(f"\nNumber of products in '{category}': {count}")

    finally:
        connection.close()
```

`cursor.fetchone()` returns one row containing a single value: the count. `[0]` reads that value out of the row.

With the original sample data, calling `count_products_in_category("Accessories")` prints `1`.

### Calculate total listed stock

Add this function too:

```python
def calculate_total_stock():
    """Print the total number of units listed across all products."""
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.execute("SELECT stock FROM products")
        stock_rows = cursor.fetchall()

        total_stock = sum(row[0] for row in stock_rows)
        print(f"\nTotal units listed: {total_stock}")

    finally:
        connection.close()
```

For the original sample data, calling `calculate_total_stock()` prints `152` units (`24 + 120 + 8`). If stock values have changed, the total will change too.

You could also calculate this value in SQL using `SUM(stock)`. This function calculates it in Python instead, to demonstrate how to process returned rows yourself. When you only need a total and do not need to process each row individually, consider asking SQL to calculate it with `SUM()`.

## 7. Retrieve results one row at a time

`fetchall()` is convenient for a small catalog, but it stores all remaining rows in memory. If a query returns a very large number of records, retrieving and processing rows incrementally can be more appropriate.

A cursor can be iterated directly, without calling `fetchall()` or `fetchone()` at all:

```python
cursor = connection.execute(
    """
    SELECT product_id, name, stock
    FROM products
    ORDER BY product_id
    """
)

for product in cursor:
    product_id, name, stock = product
    print(f"{product_id}: {name} — {stock} in stock")
```

This processes each row as it is read from the cursor, rather than creating a list containing all remaining rows with `fetchall()`. You already used this style inside `find_products_by_category()`, `find_products_below_price()`, and `find_low_stock_products()` above, where each `for product in cursor.fetchall():` loop could equally have iterated the cursor directly as `for product in cursor:`.

Use the approach that fits the task:

- Use `fetchone()` when you need one row.
- Use `fetchall()` when the result set is small and you need all its rows together.
- Iterate over the cursor when you want to process rows one at a time.
- Use SQL functions such as `COUNT(*)` when you only need a summary value.

## 8. Putting it all together

You have now built seven functions, each handling one specific catalog question. A real application rarely runs just one of these in isolation — it calls several of them, often in response to what a user asks for.

Here is the complete `query_products.py` file with every function defined together, followed by a `main()` function that calls each one in turn:

```python
from pathlib import Path
import sqlite3

DATABASE_PATH = Path(__file__).resolve().parent / "ecommart.db"


def show_all_products():
    """Print every product in the catalog, ordered by product ID."""
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.execute(
            """
            SELECT product_id, name, category, price, stock
            FROM products
            ORDER BY product_id
            """
        )

        products = cursor.fetchall()

        if not products:
            print("The catalog has no products yet.")
            return

        print("eComMART Product Catalog")
        print("=" * 40)

        for product in products:
            product_id, name, category, price, stock = product
            print(f"{product_id} | {name} | {category} | ₹{price:.2f} | Stock: {stock}")

    finally:
        connection.close()


def find_products_by_category(category):
    """Print products that belong to the given category."""
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.execute(
            """
            SELECT product_id, name, price
            FROM products
            WHERE category = ?
            ORDER BY product_id
            """,
            (category,),
        )

        print(f"\nProducts in category '{category}':")
        found = False
        for product in cursor.fetchall():
            found = True
            print(product)

        if not found:
            print("No products found in this category.")

    finally:
        connection.close()


def find_products_below_price(max_price):
    """Print products priced below the given amount."""
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.execute(
            """
            SELECT product_id, name, price
            FROM products
            WHERE price < ?
            ORDER BY price
            """,
            (max_price,),
        )

        print(f"\nProducts priced below ₹{max_price:.2f}:")
        found = False
        for product in cursor.fetchall():
            found = True
            print(product)

        if not found:
            print("No products found below this price.")

    finally:
        connection.close()


def find_low_stock_products(threshold):
    """Print products with stock below the given threshold."""
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.execute(
            """
            SELECT product_id, name, stock
            FROM products
            WHERE stock < ?
            ORDER BY stock
            """,
            (threshold,),
        )

        print(f"\nProducts with stock below {threshold}:")
        found = False
        for product in cursor.fetchall():
            found = True
            print(product)

        if not found:
            print("No products match this stock threshold.")

    finally:
        connection.close()


def find_product_by_id(product_id):
    """Print one product's full details, or a not-found message."""
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

        product = cursor.fetchone()

        print(f"\nLooking up product ID {product_id}:")
        if product is None:
            print(f"No product found with ID {product_id}.")
        else:
            pid, name, category, price, stock = product
            print(f"Product: {name}")
            print(f"Category: {category}")
            print(f"Price: ₹{price:.2f}")
            print(f"Stock: {stock}")

    finally:
        connection.close()


def count_products_in_category(category):
    """Print how many products exist in the given category."""
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.execute(
            "SELECT COUNT(*) FROM products WHERE category = ?",
            (category,),
        )
        count = cursor.fetchone()[0]
        print(f"\nNumber of products in '{category}': {count}")

    finally:
        connection.close()


def calculate_total_stock():
    """Print the total number of units listed across all products."""
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.execute("SELECT stock FROM products")
        stock_rows = cursor.fetchall()

        total_stock = sum(row[0] for row in stock_rows)
        print(f"\nTotal units listed: {total_stock}")

    finally:
        connection.close()


def main():
    """Run each catalog report in sequence."""
    show_all_products()
    find_products_by_category("Accessories")
    find_products_below_price(3000)
    find_low_stock_products(10)
    find_product_by_id(102)
    find_product_by_id(999)
    count_products_in_category("Accessories")
    calculate_total_stock()


if __name__ == "__main__":
    main()
```

Run it:

```bash
python "Examples/query_products.py"
```

With the original three sample products, the output is:

```text
eComMART Product Catalog
========================================
101 | Wireless Barcode Scanner | Scanners | ₹3499.00 | Stock: 24
102 | Thermal Label Roll | Shipping Supplies | ₹450.00 | Stock: 120
103 | USB-C Docking Station | Accessories | ₹6799.00 | Stock: 8

Products in category 'Accessories':
(103, 'USB-C Docking Station', 6799.0)

Products priced below ₹3000.00:
(102, 'Thermal Label Roll', 450.0)

Products with stock below 10:
(103, 'USB-C Docking Station', 8)

Looking up product ID 102:
Product: Thermal Label Roll
Category: Shipping Supplies
Price: ₹450.00
Stock: 120

Looking up product ID 999:
No product found with ID 999.

Number of products in 'Accessories': 1

Total units listed: 152
```

### Why organize the code this way?

- **Each function does one job.** `find_product_by_id()` only looks up a product; it does not also print the whole catalog or calculate totals. This makes each function easier to read, test, and reuse on its own.
- **Every function opens and closes its own connection.** This keeps each function self-contained: you can call `calculate_total_stock()` by itself, without needing to also set up a connection for it beforehand.
- **`main()` only coordinates.** It does not contain any SQL itself; it simply calls the functions in the order the program needs. This is the same separation-of-concerns idea you will see again in `04_Building_the_eComMART_Catalog/01_Designing_the_Database_Backend.md`, where database access, application logic, and user interaction are kept as separate responsibilities.
- **You can call just the function you need.** A real application would not usually run all seven functions one after another, every time, the way `main()` does here. More often, a menu or a web request would call exactly one of these functions, based on what the user asked for. Combining them into one `main()` here is a way to demonstrate and test all of them together in this lesson.

## 9. Common mistakes and fixes

| Mistake | Why it causes trouble | Better approach |
|---|---|---|
| Treating a row tuple as a dictionary | `product["name"]` will not work with the default tuple rows | Use the correct position, or unpack the tuple into named variables |
| Forgetting the comma in a one-value parameter tuple | `(102)` is an integer, not a tuple | Use `(102,)` |
| Unpacking a result without checking it | `fetchone()` may return `None` | Check `if product is None` first |
| Selecting every column when only one is needed | Returns more data than the task requires | Select only the required columns |
| Fetching every row just to count them | Unnecessary when SQL can return the count | Use `SELECT COUNT(*) FROM products` |
| Filtering every record in Python when SQL can filter it | The program may retrieve more data than needed | Use a `WHERE` clause in the query |
| Forgetting to close a connection | Resources can remain open longer than necessary | Close it in `finally` or use a deliberate connection-management helper |
| Writing one large function that does everything | Harder to read, test, and reuse any single part | Split each database question into its own small function, as in Section 8 |

## 10. Guided practice

Complete the tasks below using the eComMART database. Write each task as its own function, following the pattern from Section 8. Use parameter placeholders for values supplied by Python.

### Task A — List all products in ascending price order

Write a function `list_products_by_price()` that selects `product_id`, `name`, and `price`, sorted by price from lowest to highest, and prints one product per line.

### Task B — Find products with at least 20 units in stock

Write a function `find_well_stocked_products(minimum_stock)` that selects `product_id`, `name`, and `stock` where `stock >= minimum_stock`, sorted by stock from highest to lowest.

### Task C — Search for product ID 999

Write a function `look_up_product(product_id)` that uses `fetchone()` to look up the given ID and prints a helpful message if the record does not exist. Call it with `999`. Do not insert or delete anything for this task.

### Task D — Count products in the Accessories category

Write a function `count_by_category(category)` that uses `SELECT COUNT(*)` with a `WHERE category = ?` condition. Call it with `"Accessories"` and print the count.

### Suggested answers

**Task A**

```python
def list_products_by_price():
    connection = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = connection.execute(
            """
            SELECT product_id, name, price
            FROM products
            ORDER BY price ASC
            """
        )
        for product_id, name, price in cursor:
            print(f"{product_id} | {name} | ₹{price:.2f}")
    finally:
        connection.close()
```

**Task B**

```python
def find_well_stocked_products(minimum_stock):
    connection = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = connection.execute(
            """
            SELECT product_id, name, stock
            FROM products
            WHERE stock >= ?
            ORDER BY stock DESC
            """,
            (minimum_stock,),
        )
        for product_id, name, stock in cursor:
            print(f"{product_id} | {name} | Stock: {stock}")
    finally:
        connection.close()
```

**Task C**

```python
def look_up_product(product_id):
    connection = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = connection.execute(
            "SELECT product_id, name FROM products WHERE product_id = ?",
            (product_id,),
        )
        product = cursor.fetchone()

        if product is None:
            print(f"No product found with ID {product_id}.")
        else:
            print(product)
    finally:
        connection.close()
```

**Task D**

```python
def count_by_category(category):
    connection = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = connection.execute(
            "SELECT COUNT(*) FROM products WHERE category = ?",
            (category,),
        )
        count = cursor.fetchone()[0]
        print(f"{category} products: {count}")
    finally:
        connection.close()
```

If the original sample data is unchanged, `count_by_category("Accessories")` prints `1`. Your results may differ if you have added, changed, or removed products.

## 11. Knowledge check

1. What does `fetchall()` return?
2. When is `fetchone()` useful?
3. Why should you use `WHERE` in SQL rather than retrieve every row and filter everything in Python?
4. What is the purpose of `COUNT(*)`?
5. What should your code do when `fetchone()` returns `None`?
6. Does the low-stock query modify the database?
7. In Section 8, why does `main()` contain no SQL of its own?

### Answers

1. A list of the remaining rows, typically as tuples.
2. When the program needs one matching row, such as a product found by its unique ID.
3. Filtering in SQL can reduce the amount of data transferred to Python and make the query's intent clear.
4. It returns the number of rows matching the query.
5. Handle the missing result, for example by printing a message or returning from the function.
6. No. It is a `SELECT` query, so it reads data without changing records.
7. `main()`'s job is only to decide which functions run and in what order. Each function it calls already knows how to perform its own specific database task, so `main()` does not need to repeat any SQL itself.

## 12. Lesson recap

- Python sends SQL queries to SQLite and reads the returned rows.
- `fetchone()` is useful for a single result; `fetchall()` returns a list of remaining rows; cursor iteration processes rows one at a time.
- Query results are usually tuples by default, and the values follow the selected column order.
- Use `WHERE`, `ORDER BY`, and SQL summary functions to retrieve only what you need.
- Check for missing results before using or unpacking them.
- Keep read-only queries separate from operations that change data.
- Organizing each database task into its own small function, then calling those functions from one `main()`, keeps a program easy to read, test, and extend.

## What comes next?

In `03_Parameterized_Queries_and_Transactions.md`, you will learn why parameterized queries matter, how they help protect SQL statements from unsafe input, and how to manage groups of database changes with transactions.
