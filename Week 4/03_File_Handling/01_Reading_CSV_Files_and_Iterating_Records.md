# Reading CSV Files and Iterating Over Records

## eCOMMart AI Squad | Week 4

> “Before eCOMMart can use saved product information, Python must be able to read each record reliably.”

## What We Will Cover

By the end of this lesson, you will be able to:

1. Explain why business applications store records in CSV files.
2. Open a CSV file using Python's `open()` function.
3. Read CSV rows using Python's built-in `csv` module.
4. Use `csv.reader()` and `csv.DictReader()` to access records.
5. Iterate over product records, skip empty rows, and count records.
6. Recognize common file-reading errors.

---

## 1. Why Use a CSV File?

So far, examples may have stored one product name on each line of a plain-text file. Real business records usually contain several related fields. For example, eCOMMart may need to store a product ID, product name, price, and available stock.

A **CSV (Comma-Separated Values)** file stores tabular data as rows and columns. It can be opened in a text editor or spreadsheet application.

For this lesson, use a file named `products.csv` with the following exact contents:

```csv
product_id,product_name,price,stock
P101,Wireless Mouse,799,25
P102,USB-C Cable,299,100
P103,Desk Lamp,1499,12
P104,Travel Mug,499,40
```

The first row contains the column headings. Each following row represents one product.

### Create the sample file

1. Create a file named `products.csv`.
2. Copy the CSV content above into the file.
3. Save it in the same folder as the Python script you will create.
4. Make sure the file is named `products.csv`, not `products.csv.txt`.

**Important:** The first row is a header, not a product record. The file contains four product records.

## 2. Open a CSV File

Python's built-in `open()` function opens a file. The mode `"r"` means read mode. The `newline=""` argument is recommended when opening CSV files so that Python's `csv` module can handle line endings correctly.

```python
import csv

file = open("products.csv", "r", encoding="utf-8", newline="")

reader = csv.reader(file)

for row in reader:
    print(row)

file.close()
```

Example output:

```text
['product_id', 'product_name', 'price', 'stock']
['P101', 'Wireless Mouse', '799', '25']
['P102', 'USB-C Cable', '299', '100']
['P103', 'Desk Lamp', '1499', '12']
['P104', 'Travel Mug', '499', '40']
```

Notice that each row is returned as a **list of strings**. The CSV reader does not automatically convert values such as `799` or `25` into numbers.

This example also prints the header row. In the next section, you will see how to handle headers more conveniently.

**Remember:** Close a file you open manually. Later in this module, you will practise using `with open(...)`, which closes the file automatically when the block ends.

## 3. Read Rows with `csv.reader()`

The `csv.reader()` function reads a CSV file one row at a time. Each row is a list, and each item in that list corresponds to a column.

```python
import csv

file = open("products.csv", "r", encoding="utf-8", newline="")
reader = csv.reader(file)

for row in reader:
    print("Product ID:", row[0])
    print("Product name:", row[1])
    print("Price:", row[2])
    print("Stock:", row[3])
    print("---")

file.close()
```

For the first product, `row[0]` is `"P101"` and `row[1]` is `"Wireless Mouse"`.

The first row of the file is the header, so this simple loop will also treat the headings as a row of data. You could skip that row with `next(reader)`, but `csv.DictReader()` is often easier when your code needs to refer to fields by name.

### Skip the header with `next()`

```python
import csv

file = open("products.csv", "r", encoding="utf-8", newline="")
reader = csv.reader(file)

header = next(reader)
print("Columns:", header)

for row in reader:
    print(row)

file.close()
```

Expected output begins with:

```text
Columns: ['product_id', 'product_name', 'price', 'stock']
['P101', 'Wireless Mouse', '799', '25']
['P102', 'USB-C Cable', '299', '100']
['P103', 'Desk Lamp', '1499', '12']
['P104', 'Travel Mug', '499', '40']
```

`next(reader)` retrieves the next row from the reader. Here, it retrieves the header before the loop starts, so the loop processes only product records.

## 4. Read Records by Column Name with `csv.DictReader()`

When a CSV file has headings, `csv.DictReader()` can make the code easier to understand. Instead of accessing a field by its numeric position, you can access it by its column name.

```python
import csv

file = open("products.csv", "r", encoding="utf-8", newline="")
reader = csv.DictReader(file)

for product in reader:
    print(product["product_id"], "-", product["product_name"])
    print("Price:", product["price"])
    print("Stock:", product["stock"])
    print("---")

file.close()
```

Example output:

```text
P101 - Wireless Mouse
Price: 799
Stock: 25
---
P102 - USB-C Cable
Price: 299
Stock: 100
---
P103 - Desk Lamp
Price: 1499
Stock: 12
---
P104 - Travel Mug
Price: 499
Stock: 40
---
```

Each `product` is a dictionary-like row. The CSV column headings become the keys, such as `"product_id"` and `"product_name"`.

For example:

```python
print(product["product_name"])
```

This accesses the product name by its column heading. It is generally clearer than remembering that the product name is at index `1`.

**Important:** Values read from a CSV file are strings. If you need to perform arithmetic, convert the value to the required type first.

```python
price = int(product["price"])
stock = int(product["stock"])

print(price * stock)
```

This calculation gives the value of the available stock for that product, assuming the price and stock fields contain valid whole numbers.

## 5. Count Product Records

Let's count how many product records eCOMMart has saved. Because `DictReader` uses the first row as column headings, the loop processes only the product records.

```python
import csv

file = open("products.csv", "r", encoding="utf-8", newline="")
reader = csv.DictReader(file)

product_count = 0

for product in reader:
    if product["product_id"].strip():
        product_count += 1

file.close()

print(f"Product records: {product_count}")
```

Expected output:

```text
Product records: 4
```

The condition `if product["product_id"].strip():` checks that the product ID is not empty or made up only of whitespace.

This example assumes that each valid product record has a non-empty `product_id`.

## 6. Keep Product Records in a List

Sometimes an application needs to keep records in memory so that it can use them after reading the file. You can append each row returned by `DictReader` to a list.

```python
import csv

file = open("products.csv", "r", encoding="utf-8", newline="")
reader = csv.DictReader(file)

products = []

for product in reader:
    if product["product_id"].strip():
        products.append(product)

file.close()

print(products)
print("Product records:", len(products))
```

The list contains dictionaries, one for each product. A record will look similar to this:

```python
{
    "product_id": "P101",
    "product_name": "Wireless Mouse",
    "price": "799",
    "stock": "25"
}
```

Expected final line:

```text
Product records: 4
```

Do not confuse these two ideas:

- **Iterating over a CSV reader** processes records one at a time.
- **Appending records to a list** keeps those records in memory so the program can use them later.

For a small file, keeping all records in a list is convenient. For a very large file, processing records one at a time may use less memory.

## 7. Handle Empty Rows and Missing Values

A CSV file can contain a blank row or a row with a missing field. For example:

```csv
product_id,product_name,price,stock
P101,Wireless Mouse,799,25

P102,USB-C Cable,299,100
P103,Desk Lamp,,12
```

In this example:

- The blank line does not represent a complete product record.
- The Desk Lamp row has an empty price field.
- A missing value should not automatically be treated as zero. The application should decide how to handle it.

The following example skips blank rows and reports records with missing required fields:

```python
import csv

file = open("products_with_missing_values.csv", "r", encoding="utf-8", newline="")
reader = csv.DictReader(file)

for product in reader:
    # Skip a completely blank row.
    if not any(value and value.strip() for value in product.values()):
        continue

    # Check fields required for this example.
    required_fields = ["product_id", "product_name", "price", "stock"]
    missing_fields = [
        field
        for field in required_fields
        if not product.get(field) or not product[field].strip()
    ]

    if missing_fields:
        print("Incomplete product record:", product)
        print("Missing fields:", missing_fields)
        continue

    print("Valid product:", product["product_name"])

file.close()
```

This example assumes the CSV file has the expected column headings. It shows a basic validation pattern; it does not yet check whether price and stock contain valid numeric values.

## 8. Common CSV-Reading Errors

### `FileNotFoundError`

Python cannot find the file at the path provided.

Check:

- The file is named `products.csv`.
- The file is saved in the folder from which the script is being run, or you have supplied the correct path.
- The spelling and file extension are correct.

### `PermissionError`

The program does not have permission to read the file. Check its permissions and whether another application or process is preventing access.

### `KeyError`

The code tries to access a dictionary key that does not exist. For example, `product["product_name"]` will fail if the CSV header is spelled differently or is missing.

Check the header row and make sure your code uses the same column names.

### `ValueError` when converting values

A conversion such as `int(product["price"])` can fail if the field is empty or contains text that is not a valid integer. Validate the value before converting it.

### Incorrect CSV structure

If the file uses different delimiters or has unexpected headings, the reader may not return the fields you expect. Check the file's contents and its delimiter. The examples in this lesson use commas.

---

## Practice Tasks

Complete the tasks in order. Use the `products.csv` file created in Section 1.

### Task 1 — Read and Display CSV Rows

**Goal:** Open a CSV file and display its rows.

1. Create `products.csv` using the sample data from Section 1.
2. Create a Python file named `read_products.py` in the same folder.
3. Import Python's built-in `csv` module.
4. Open `products.csv` in read mode using UTF-8 encoding and `newline=""`.
5. Use `csv.reader()` to iterate through the rows.
6. Print each row.
7. Close the file after reading.

**Check your result:** The output should show the header row followed by four product rows.

### Task 2 — Display Product Details

**Goal:** Read a record using column names.

1. Open `products.csv` in read mode.
2. Create a `csv.DictReader` for the file.
3. Iterate over each product record.
4. Print its product ID, product name, price, and stock.
5. Close the file after the loop.

**Check your result:** The four product names should appear, and the header row should not be printed as a product.

### Task 3 — Count Product Records

**Goal:** Count valid product rows.

1. Read `products.csv` with `csv.DictReader()`.
2. Start a variable named `product_count` at `0`.
3. Iterate over the records.
4. Increase the count only when `product_id` is not empty.
5. Print the final count.

Expected output:

```text
Product records: 4
```

### Task 4 — Build a List of Products

**Goal:** Keep the records for later use.

1. Read the file using `csv.DictReader()`.
2. Create an empty list named `products`.
3. Append each record with a non-empty product ID to the list.
4. Print the number of stored records using `len(products)`.
5. Print the name of the first product using `products[0]["product_name"]`.

Expected output:

```text
Product records: 4
First product: Wireless Mouse
```

Add a comment explaining why the records are stored in a list.

---

## Summary

| Concept | What to remember |
|---|---|
| CSV file | Stores tabular records as rows and columns. |
| `open(path, "r", encoding="utf-8", newline="")` | Opens a CSV file for reading. |
| `csv.reader(file)` | Reads rows as lists of strings. |
| `next(reader)` | Retrieves the next row; useful for reading or skipping a header. |
| `csv.DictReader(file)` | Reads rows using column headings as keys. |
| `product["product_name"]` | Accesses a field by its column name. |
| `strip()` | Removes surrounding whitespace. |
| `append()` | Adds a record to a list. |
| `len(products)` | Returns the number of records stored in a list. |
| Type conversion | CSV values are strings; convert them before arithmetic. |
| File errors | Check paths, permissions, headings, and field values. |

**Key takeaway:** CSV files let eCOMMart store product information in a structured format. Python's `csv` module helps you read each row and access the values needed by your application.

*Next: `02_Writing_and_Appending_Files.md`*
