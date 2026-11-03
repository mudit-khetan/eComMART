# 01 — Understand the Database
## eComMART Product Catalog

Before writing SQL or connecting Python to a database, let's understand how the data is organised. This guide introduces the database concepts you will use throughout Week 5.

You do not need previous database experience. Read the explanations and use the examples to connect each new term to something familiar.

---

## 1. Why does eComMART need a database?

Imagine that eComMART is a B2B online store. Businesses use the store to find and order products. The store needs to keep track of each product's name, category, price, and available stock.

If the store kept all this information only in Python variables, the information would normally disappear when the program ended. A database lets the application save the information and use it again later.

For this week's examples, we will use **SQLite**. SQLite stores data in a database file on your computer, so you do not need to run a separate database server.

The database file is named:

```text
ecommart.db
```

The file stores the product information used by the examples.

## 2. What is a database?

A **database** is an organised collection of information that a computer program can store, search, and update.

Think of it like a well-organised digital record book. Instead of searching through unrelated notes, an application can ask the database for the exact information it needs.

For eComMART, the database stores information about the products available in the catalogue.

## 3. What is a table?

A **table** stores one kind of related information in rows and columns.

The eComMART example uses a table named:

```text
products
```

This table stores product information. Each row represents one product, and each column stores one detail about that product.

For example, the table contains a product ID, product name, category, price, and stock quantity.

## 4. Explore the products table

Here are the three starter records used throughout the Week 5 examples.

| product_id | name | category | price | stock |
|---:|---|---|---:|---:|
| 101 | Wireless Barcode Scanner | Scanners | 3499.00 | 24 |
| 102 | Thermal Label Roll | Shipping Supplies | 450.00 | 120 |
| 103 | USB-C Docking Station | Accessories | 6799.00 | 8 |

Let's understand how to read this table.

### Rows are records

A **row**, also called a **record**, contains all the stored details for one product.

For example, the first row describes the Wireless Barcode Scanner:

- Product ID: `101`
- Name: `Wireless Barcode Scanner`
- Category: `Scanners`
- Price: `3499.00`
- Stock: `24`

All five values belong to the same product.

### Columns are fields

A **column**, sometimes called a **field**, represents one type of information stored for every product.

For example:

- `name` stores product names.
- `price` stores product prices.
- `stock` stores the number of units available.

Every row follows the same column structure. This makes it easier for the application to find and compare information.

## 5. Understand each column

| Column | Meaning | Example value |
|---|---|---|
| `product_id` | The unique identifier assigned to a product. | `101` |
| `name` | The product's name. | `Wireless Barcode Scanner` |
| `category` | The group the product belongs to. | `Scanners` |
| `price` | The product's price. | `3499.00` |
| `stock` | The number of units currently available. | `24` |

The column names are written in lowercase with underscores where needed. For example, `product_id` uses an underscore instead of a space. This is a common naming style in programming and database examples.

## 6. What is a data type?

A **data type** describes the kind of value a column is expected to store. It helps the database interpret the information.

The eComMART table uses these SQLite data types:

| Column | SQLite type | Why this type is used |
|---|---|---|
| `product_id` | `INTEGER` | Product IDs are whole numbers. |
| `name` | `TEXT` | A product name is text. |
| `category` | `TEXT` | A category name is text. |
| `price` | `REAL` | Prices in this introductory example may contain decimal values. |
| `stock` | `INTEGER` | Stock quantities are whole numbers. |

You do not need to memorise every SQLite data type yet. For now, remember:

- `INTEGER` is used for whole numbers.
- `TEXT` is used for text.
- `REAL` is used for numeric values that may include a decimal point.

**A practical note about prices:** `REAL` is used here to keep the introductory example simple. Production financial systems often store money as integer minor units, such as paise or cents, or use a decimal-capable representation to avoid floating-point rounding issues.

## 7. What is a primary key?

A **primary key** is a column, or combination of columns, that uniquely identifies each row in a table.

In the eComMART table, `product_id` is the primary key.

Consider these IDs:

- `101` identifies the Wireless Barcode Scanner.
- `102` identifies the Thermal Label Roll.
- `103` identifies the USB-C Docking Station.

Each product has a different ID. This lets the application refer to one particular product without relying on its name.

### Why not use the product name as the identifier?

Product names are not always reliable identifiers. Two products could have similar names, or a name could change. A unique ID gives the application a stable way to identify a record.

### Remember

A primary key must uniquely identify each record. The same primary-key value cannot identify two different products in this table.

## 8. What is a schema?

A **schema** describes how a database table is organised. It defines the table name, its columns, their data types, and rules such as which column is the primary key.

The eComMART example has this core table structure:

```sql
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
);
```

You do not need to run this code just to read this guide. It is shown so you can see how the table structure is described in SQL.

Let's break it down:

- `CREATE TABLE products` tells SQLite to create a table named `products`.
- `product_id INTEGER PRIMARY KEY` creates the product ID column and marks it as the primary key.
- `name TEXT NOT NULL` creates a text column that must have a value.
- `category TEXT NOT NULL` creates a category column that must have a value.
- `price REAL NOT NULL` creates a numeric price column that must have a value.
- `stock INTEGER NOT NULL` creates a whole-number stock column that must have a value.

`NOT NULL` means that a value cannot be left as SQL `NULL`, which represents a missing or unknown value. It is different from an empty string or the number zero.

The setup script supplied with your course may include additional validation rules, such as preventing negative prices or stock values. Those rules help protect the data.

## 9. How does the database fit into the Python application?

The database stores the information. Python code can connect to it and ask for information or make permitted changes.

A simplified workflow looks like this:

```text
Python program
      |
      | sends an SQL query
      v
SQLite database (ecommart.db)
      |
      | returns matching records
      v
Python program displays or uses the results
```

For example, a Python program might ask SQLite to return all products. SQLite reads the `products` table and sends the matching rows back to Python. Python can then display the products to the user.

The database and the Python program have different jobs:

- **SQLite** stores and manages the records.
- **SQL** describes what information to read or change.
- **Python** controls the application workflow and decides how to use the results.

## 10. Try it yourself: view the table

Now open the database and see the table for yourself.

### Step 1 — Create the database if needed

If you have not prepared the database yet, follow the instructions in `START_HERE.md` and run `setup_database.py`.

### Step 2 — Open the database

1. Open DB Browser for SQLite.
2. Choose **Open Database**.
3. Select `ecommart.db` from the `Examples` folder.

### Step 3 — View the records

1. Select **Browse Data**.
2. Choose `products` from the table selector.
3. Look at the column names and the three starter records.

### Step 4 — Check your understanding

Try to answer these questions while looking at the table:

1. How many products are shown?
2. Which column stores the product name?
3. Which product has a stock quantity of `8`?
4. Which column is the primary key?
5. What is the category of product ID `102`?

**Check your answers:**

1. Three products.
2. `name`.
3. USB-C Docking Station.
4. `product_id`.
5. Shipping Supplies.

## 11. Quick knowledge check

Try answering these questions before looking at the answers.

### Questions

1. What is a database?
2. In the `products` table, what does one row represent?
3. What is the difference between a row and a column?
4. Why does the table use a `product_id` primary key?
5. Which data type is used for the product name?
6. Which file stores the actual database data?
7. What is the role of Python in this example?

### Answers

1. An organised collection of information that a program can store, search, and update.
2. One product record.
3. A row contains the details for one record; a column stores one type of information across records.
4. It uniquely identifies each product.
5. `TEXT`.
6. `ecommart.db`.
7. Python connects to the database, sends queries, and uses the results in the application.

## 12. Key takeaways

- A database stores organised information.
- The eComMART database file is named `ecommart.db`.
- The `products` table stores the product catalogue.
- Each row represents one product, and each column represents one type of information.
- The `product_id` column is the primary key.
- Data types describe the kind of values stored in each column.
- The schema describes the table's structure.
- Python can use SQL to work with data stored in SQLite.

Once these ideas make sense, move on to the SQL examples. You will learn how to retrieve and change the product data.
