-- ============================================================
-- Week 5: SQL Query Examples
-- eComMART Product Catalog
-- ============================================================
--
-- PURPOSE
-- This file contains SQL examples for practising with the
-- eComMART products table in SQLite.
--
-- HOW TO USE THIS FILE
-- 1. Open ecommart.db in DB Browser for SQLite.
-- 2. Select the "Execute SQL" tab.
-- 3. Open this file in a text editor.
-- 4. Copy ONE complete SQL statement at a time into DB Browser.
-- 5. Click "Execute SQL" and inspect the results.
--
-- IMPORTANT
-- - This is an SQL file, not a Python script. Do not run it with
--   "python 02_SQL_Query_Examples.sql".
-- - Read the comments before running a statement.
-- - SELECT statements read data. INSERT, UPDATE, and DELETE
--   statements change data.
-- - Do not select and execute the entire file all at once.
-- - The starter products are IDs 101, 102, and 103.
-- - The practice product uses ID 104. Check that it does not
--   already exist before inserting it.
--
-- STARTER PRODUCTS
-- 101 | Wireless Barcode Scanner | Scanners          | 3499.00 | 24
-- 102 | Thermal Label Roll       | Shipping Supplies |  450.00 | 120
-- 103 | USB-C Docking Station    | Accessories       | 6799.00 | 8
--
-- ============================================================
-- SECTION 1 — READ DATA WITH SELECT
-- ============================================================

-- Example 1: Display every column for every product.
-- Expected: the three starter products, plus any other records
-- already in your database.
SELECT *
FROM products;


-- Example 2: Display only the product name and price.
-- Expected: two columns named name and price.
SELECT name, price
FROM products;


-- Example 3: Find products in the Scanners category.
-- Expected starter match: Wireless Barcode Scanner.
SELECT *
FROM products
WHERE category = 'Scanners';


-- Example 4: Find products with fewer than 20 units in stock.
-- Expected starter matches: USB-C Docking Station (stock 8).
SELECT product_id, name, stock
FROM products
WHERE stock < 20;


-- Example 5: Sort products from highest price to lowest price.
-- DESC means descending order.
SELECT name, price
FROM products
ORDER BY price DESC;


-- Example 6: Display only two products.
-- Without ORDER BY, SQLite does not promise a particular order.
-- Add ORDER BY when you need a predictable order.
SELECT product_id, name
FROM products
ORDER BY product_id
LIMIT 2;


-- Example 7: Search for product names containing the word "Label".
-- The percent signs (%) mean that other text may appear before
-- or after the word.
SELECT product_id, name, category
FROM products
WHERE name LIKE '%Label%';


-- ============================================================
-- SECTION 2 — ADD A DISPOSABLE PRACTICE PRODUCT
-- ============================================================
-- The next statements use product ID 104 so that you can practise
-- without changing the three starter products.
--
-- Before inserting, run this check. If product ID 104 already
-- exists, do not insert another product with the same ID.
-- If it exists from an earlier practice session, you can use it
-- for the UPDATE and DELETE exercises below.

SELECT *
FROM products
WHERE product_id = 104;


-- Example 8: Add a temporary practice product.
-- Run this INSERT only if the check above returned no rows.
-- Expected: one new product with ID 104.
INSERT INTO products (product_id, name, category, price, stock)
VALUES (104, 'Practice USB Cable', 'Accessories', 299.00, 15);


-- Check the practice product after inserting it.
SELECT *
FROM products
WHERE product_id = 104;


-- ============================================================
-- SECTION 3 — UPDATE A RECORD
-- ============================================================
-- Example 9: Change the practice product's stock from 15 to 20.
-- Run this only after product ID 104 exists.
-- The WHERE clause is essential: it targets only product 104.
UPDATE products
SET stock = 20
WHERE product_id = 104;


-- Verify the update.
-- Expected for the practice product: stock is now 20.
SELECT product_id, name, stock
FROM products
WHERE product_id = 104;


-- Example 10: Change the practice product's price to 349.00.
-- Run this only after product ID 104 exists.
UPDATE products
SET price = 349.00
WHERE product_id = 104;


-- Verify the price change.
SELECT product_id, name, price
FROM products
WHERE product_id = 104;


-- ============================================================
-- SECTION 4 — DELETE THE PRACTICE RECORD
-- ============================================================
-- Example 11: Delete only the disposable practice product.
-- Before running, confirm that product ID 104 is the practice
-- record you added. Do not remove a record you need to keep.
DELETE FROM products
WHERE product_id = 104;


-- Verify that product ID 104 is no longer present.
-- Expected: zero rows if the delete succeeded.
SELECT *
FROM products
WHERE product_id = 104;


-- ============================================================
-- SECTION 5 — REVIEW
-- ============================================================
-- SELECT  : reads records.
-- INSERT  : adds a record.
-- UPDATE  : changes existing records.
-- DELETE  : removes records.
--
-- SAFETY REMINDER
-- Never run an UPDATE or DELETE statement without checking
-- its WHERE clause. Without WHERE, the statement may affect
-- every row in the table.
--
-- Example of a dangerous statement — DO NOT RUN:
--
-- UPDATE products
-- SET stock = 0;
--
-- It would set the stock to zero for every product.
--
-- Another dangerous statement — DO NOT RUN:
--
-- DELETE FROM products;
--
-- It would remove every record from the products table.
-- ============================================================
