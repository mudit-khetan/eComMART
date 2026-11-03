# 03 — SQL Explained
## Learn SQL with the eComMART Product Catalog

This guide explains the SQL statements in `02_SQL_Query_Examples.sql`. Read the explanation first, then open the SQL file and run one statement at a time in DB Browser for SQLite.

You do not need to memorise every command. The goal is to understand what each statement asks the database to do.

---

## 1. Before you begin

Make sure you have:

- Run `setup_database.py`.
- Created or located `ecommart.db`.
- Opened `ecommart.db` in DB Browser for SQLite.

To run a query:

1. Open `02_SQL_Query_Examples.sql` in your code editor.
2. Copy one complete SQL statement.
3. In DB Browser, select **Execute SQL**.
4. Paste the statement into the SQL editor.
5. Click **Execute SQL** and inspect the result.

Do not run the entire practice file at once. Some statements change data.

## 2. Read data with `SELECT`

A `SELECT` statement asks the database to return information.

### Example A — Read every column

```sql
SELECT *
FROM products;
```

- `SELECT` means “return information”.
- `*` means “all columns”.
- `FROM products` identifies the table to read.

**Expected result:** Every product currently stored in the table. The starter database begins with three products, but your results may include additional practice records.

### Example B — Read selected columns

```sql
SELECT name, price
FROM products;
```

This returns only the `name` and `price` columns. It does not change the data in the database.

**When is this useful?** When a screen or report needs only a few details, selecting specific columns makes the result easier to read.

## 3. Filter results with `WHERE`

A `WHERE` clause keeps only records that match a condition.

### Example C — Find a category

```sql
SELECT *
FROM products
WHERE category = 'Scanners';
```

The query returns products whose category is exactly `Scanners`.

- `WHERE` introduces the condition.
- `category` is the column being checked.
- `=` means “equals”.
- `'Scanners'` is a text value, so it is surrounded by single quotes.

**Expected starter match:** Wireless Barcode Scanner.

### Example D — Find products with low stock

```sql
SELECT product_id, name, stock
FROM products
WHERE stock < 20;
```

The `<` symbol means “less than”. This returns products with fewer than 20 units in stock.

**Expected starter match:** USB-C Docking Station, with stock of 8.

Other useful comparison operators include:

| Operator | Meaning |
|---|---|
| `=` | Equal to |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal to |
| `<=` | Less than or equal to |
| `<>` | Not equal to |

## 4. Sort results with `ORDER BY`

```sql
SELECT name, price
FROM products
ORDER BY price DESC;
```

`ORDER BY price` sorts the results using the price column.

- `ASC` means ascending order (low to high). It is the default.
- `DESC` means descending order (high to low).

For example, to show the cheapest products first:

```sql
SELECT name, price
FROM products
ORDER BY price ASC;
```

Sorting the results does not change how records are stored in the table.

## 5. Limit the number of results

```sql
SELECT product_id, name
FROM products
ORDER BY product_id
LIMIT 2;
```

`LIMIT 2` asks SQLite to return no more than two rows. `ORDER BY product_id` makes the selection predictable by sorting the products by ID first.

## 6. Search text with `LIKE`

```sql
SELECT product_id, name, category
FROM products
WHERE name LIKE '%Label%';
```

`LIKE` is used for pattern matching.

- `%` means that any sequence of characters may appear in that position.
- `'%Label%'` finds names containing `Label` anywhere in the text.

The starter product `Thermal Label Roll` should match.

## 7. Add a record with `INSERT`

The SQL practice file uses product ID `104` for a disposable practice product.

```sql
INSERT INTO products (product_id, name, category, price, stock)
VALUES (104, 'Practice USB Cable', 'Accessories', 299.00, 15);
```

The column list tells SQLite which columns will receive values. The `VALUES` list supplies the values in the same order.

The values must line up:

- `product_id` → `104`
- `name` → `'Practice USB Cable'`
- `category` → `'Accessories'`
- `price` → `299.00`
- `stock` → `15`

Text values use single quotes. Numeric values do not need quotes in this example.

**Before running the insert:** Check whether ID `104` already exists:

```sql
SELECT *
FROM products
WHERE product_id = 104;
```

If the practice product already exists, do not run the same insert again. You can continue with the update examples using that record, or use a different unused ID and adjust the later statements to match.

## 8. Change a record with `UPDATE`

```sql
UPDATE products
SET stock = 20
WHERE product_id = 104;
```

- `UPDATE products` identifies the table to change.
- `SET stock = 20` sets the stock value to 20.
- `WHERE product_id = 104` identifies which product to change.

**Why is `WHERE` important?** Without it, the statement could update every product in the table.

After updating, verify the result:

```sql
SELECT product_id, name, stock
FROM products
WHERE product_id = 104;
```

The practice product should now have stock `20`.

## 9. Remove a record with `DELETE`

```sql
DELETE FROM products
WHERE product_id = 104;
```

This removes the record with product ID `104`.

Before running it, confirm that ID `104` belongs to the disposable practice product. Never delete a record unless you understand which record the condition selects.

Verify the result:

```sql
SELECT *
FROM products
WHERE product_id = 104;
```

If the deletion succeeded, this query returns zero rows.

## 10. Important safety rules

1. Run one statement at a time.
2. Read the whole statement before executing it.
3. Check the `WHERE` clause in every `UPDATE` or `DELETE`.
4. Practise with a disposable record instead of changing the starter products.
5. Review changes in DB Browser before choosing **Write Changes**.
6. If you are unsure what a statement will do, do not run it yet.

These statements are dangerous and are shown only as warnings. **Do not run them:**

```sql
-- DANGEROUS: changes the stock for every product.
UPDATE products
SET stock = 0;

-- DANGEROUS: removes every record from the table.
DELETE FROM products;
```

## 11. Common mistakes

### Text value has no quotes

Incorrect:

```sql
SELECT *
FROM products
WHERE category = Scanners;
```

Correct:

```sql
SELECT *
FROM products
WHERE category = 'Scanners';
```

Text values should be enclosed in single quotes.

### Column name is misspelled

If the column is named `product_id`, typing `productid` or `product_ids` will cause an error. Check the exact column names in the table.

### The practice product already exists

An insert using ID `104` may fail if that ID is already present because the primary key must be unique. Check the table before inserting again.

### The change affected too many records

An `UPDATE` or `DELETE` statement may affect every row if the `WHERE` clause is missing. Always review the condition before executing the statement.

## 12. Check your understanding

Try to answer these questions before checking the answers.

1. Which command reads data?
2. What does `WHERE stock < 20` mean?
3. What does `ORDER BY price DESC` do?
4. Which command adds a record?
5. Why does an update usually need a `WHERE` clause?
6. What should you check before inserting product ID `104`?
7. How can you verify that a delete worked?

### Answers

1. `SELECT`.
2. It returns products with fewer than 20 units in stock.
3. It sorts products from highest price to lowest price.
4. `INSERT`.
5. It identifies which records should be changed; without it, every record may be affected.
6. Check whether product ID `104` already exists.
7. Run a `SELECT` query for ID `104` and confirm that it returns zero rows.

## 13. Summary

| SQL command | Main purpose |
|---|---|
| `SELECT` | Read data |
| `WHERE` | Filter records by a condition |
| `ORDER BY` | Sort results |
| `LIMIT` | Restrict the number of returned rows |
| `INSERT` | Add a record |
| `UPDATE` | Change records |
| `DELETE` | Remove records |

When you are comfortable with these statements, continue to `04_Python_Database_Example.py` to see how Python executes a query and reads the results.
