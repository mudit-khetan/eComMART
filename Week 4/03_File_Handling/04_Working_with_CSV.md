# Working with CSV: Reading Entire Files, Processing Records, and Using Excel

## eCOMMart AI Squad | Week 4

> “A CSV file can be viewed as text, opened in a spreadsheet, or processed one record at a time by Python. Choosing the right approach depends on what your application needs to do.”

## What We Will Cover

By the end of this lesson, you will be able to:

1. Explain what a CSV file is and how it represents tabular data.
2. Open the same CSV file in Microsoft Excel and inspect its rows and columns.
3. Read an entire CSV file as one string using `read()`.
4. Process CSV records one at a time using `csv.reader()` and `csv.DictReader()`.
5. Explain the difference between reading raw file content and parsing CSV records.
6. Write and append records to CSV files.
7. Handle common file and CSV errors.

---

## 1. What Is a CSV File?

CSV stands for **Comma-Separated Values**. It is a plain-text format commonly used to store tabular data. Each line usually represents a row, and commas separate values within a row.

eCOMMart can use a CSV file to store product catalogue information, such as a product ID, product name, price, and quantity.

Create a file named `products.csv` containing this exact content:

```csv
product_id,name,price,quantity
P101,Wireless Mouse,799,25
P102,Keyboard,1299,18
P103,Laptop Stand,999,12
P104,USB-C Hub,1499,10
```

The first row contains the column headings. The remaining four rows represent product records.

### Create and save the file

1. Open a text editor or code editor.
2. Copy the CSV content above.
3. Save the file as `products.csv` in the same folder as your Python script.
4. Make sure the file is named `products.csv`, not `products.csv.txt`.

A CSV file is plain text. You can inspect its comma-separated values in a text editor, or open it in a spreadsheet application such as Microsoft Excel.

**Important:** CSV files do not preserve Python data types. When Python reads CSV values through the `csv` module, values such as `799` and `25` are initially returned as strings.

## 2. Open the CSV File in Microsoft Excel

Before writing Python code, look at the data as a spreadsheet user would.

1. Locate the `products.csv` file you created.
2. Open Microsoft Excel.
3. Use Excel's **Open** option to open `products.csv`. Depending on your Excel version and operating system, you may also be able to open the file directly from your file manager.
4. If Excel shows an import screen, choose comma as the delimiter and confirm the import.
5. Check that the four headings appear in separate columns and that each product appears on its own row.

The spreadsheet should look similar to this:

| product_id | name | price | quantity |
|---|---|---:|---:|
| P101 | Wireless Mouse | 799 | 25 |
| P102 | Keyboard | 1299 | 18 |
| P103 | Laptop Stand | 999 | 12 |
| P104 | USB-C Hub | 1499 | 10 |

This table is an illustrative preview of how the data should appear in Excel.

### What to notice

- The first row contains the column headings.
- Each product is represented by one row.
- Each column represents one field, such as `name` or `price`.
- Excel displays the values in cells, while the underlying CSV file stores the data as text separated by commas.

**Do not confuse CSV with an Excel workbook.** A CSV file normally stores one table of plain-text data and does not preserve Excel-specific features such as formulas, formatting, multiple worksheets, or charts. If you save a file as `.xlsx`, you are creating an Excel workbook rather than a CSV file.

---

## 3. Method A — Read the Entire File in One Operation

Python's built-in `open()` function opens a file. The `read()` method reads the remaining file content and returns it as **one string**.

This is called reading the file in one operation, or reading the entire file at once.

```python
with open("products.csv", "r", encoding="utf-8") as file:
    content = file.read()

print(content)
```

Example output:

```text
product_id,name,price,quantity
P101,Wireless Mouse,799,25
P102,Keyboard,1299,18
P103,Laptop Stand,999,12
P104,USB-C Hub,1499,10
```

The variable `content` contains the entire file as a single string, including the header row and newline characters.

You can verify its type:

```python
with open("products.csv", "r", encoding="utf-8") as file:
    content = file.read()

print(type(content).__name__)
print(repr(content))
```

Example output:

```text
str
'product_id,name,price,quantity\nP101,Wireless Mouse,799,25\nP102,Keyboard,1299,18\nP103,Laptop Stand,999,12\nP104,USB-C Hub,1499,10\n'
```

The `\n` sequences shown by `repr()` represent newline characters.

### What does `read()` actually do?

`read()` does not understand CSV columns. It reads the file's raw text. It does not automatically create a list for each row or a dictionary for each product.

For example, this expression:

```python
content = file.read()
```

gives you one string. It does **not** give you an individual product record.

### When is reading the entire file useful?

Reading the whole file at once can be convenient when:

- The file is small.
- You need to inspect or display the complete text.
- You need to pass the complete text to another operation that expects a string.

For very large files, reading everything into memory at once can be inefficient. If you need to process each product separately, a record-by-record approach is usually more appropriate.

---

## 4. Method B — Read CSV Records One at a Time

When an application needs to process each product separately, use Python's built-in `csv` module. It understands CSV rows and fields, rather than treating the complete file as one string.

### 4.1 Use `csv.reader()`

```python
import csv

with open("products.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)

    for row in reader:
        print(row)
```

Example output:

```text
['product_id', 'name', 'price', 'quantity']
['P101', 'Wireless Mouse', '799', '25']
['P102', 'Keyboard', '1299', '18']
['P103', 'Laptop Stand', '999', '12']
['P104', 'USB-C Hub', '1499', '10']
```

Each `row` is a list of strings. The loop obtains one row at a time from the CSV reader and processes it before moving to the next row.

The first row contains the headings. If you want to process only product records, you can skip the header.

```python
import csv

with open("products.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader, None)  # Skip the header row if present.

    for row in reader:
        product_id, name, price, quantity = row
        print(f"{name}: ₹{price}, stock {quantity}")
```

Example output:

```text
Wireless Mouse: ₹799, stock 25
Keyboard: ₹1299, stock 18
Laptop Stand: ₹999, stock 12
USB-C Hub: ₹1499, stock 10
```

`next(reader, None)` retrieves the next row before the loop begins. Here, that row is the header. The default value `None` means the call will not raise `StopIteration` if the file has no rows.

### 4.2 Use `csv.DictReader()`

If the CSV file has a header row, `csv.DictReader()` lets you access each record by column name instead of numeric position.

```python
import csv

with open("products.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for product in reader:
        print(product["product_id"], "-", product["name"])
        print("Price:", product["price"])
        print("Quantity:", product["quantity"])
        print("---")
```

Example output:

```text
P101 - Wireless Mouse
Price: 799
Quantity: 25
---
P102 - Keyboard
Price: 1299
Quantity: 18
---
P103 - Laptop Stand
Price: 999
Quantity: 12
---
P104 - USB-C Hub
Price: 1499
Quantity: 10
---
```

Each `product` is a dictionary-like row. The CSV headings become keys, so you can write `product["name"]` instead of remembering that the product name is at position `1`.

Unlike `csv.reader()`, `csv.DictReader()` uses the first row as column headings automatically. It does not yield the header as a product record.

### 4.3 Convert values before doing calculations

Values returned by `csv.reader()` and `csv.DictReader()` are strings. Convert numeric fields before performing arithmetic.

```python
import csv

with open("products.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for product in reader:
        price = int(product["price"])
        quantity = int(product["quantity"])
        stock_value = price * quantity

        print(f'{product["name"]}: ₹{stock_value}')
```

Example output:

```text
Wireless Mouse: ₹19975
Keyboard: ₹23382
Laptop Stand: ₹11988
USB-C Hub: ₹14990
```

This calculates the value of the available stock for each product by multiplying its price by its quantity.

---

## 5. Compare the Two Reading Approaches

Both approaches read the same `products.csv` file, but they give your program different kinds of results.

| Question | `file.read()` | `csv.reader()` / `csv.DictReader()` |
|---|---|---|
| What does it return or yield? | One string containing the remaining file text | One parsed CSV row at a time |
| Does it understand CSV columns? | No | Yes |
| How are product fields accessed? | The text must be parsed separately if field-level access is needed | By list position with `reader`, or by column name with `DictReader` |
| Does it load the complete file content at once? | Yes | It iterates through rows rather than reading the entire file into one string |
| Best suited for | Inspecting or using all the raw text | Processing individual records and fields |

### Visual comparison

<box border radius="lg" padding={3} gap={3}>
  <box gap={1}>
    **Entire-file read**

    <box background="surface-secondary" radius="md" padding={3} gap={1}>
      <text color="secondary" size="sm">products.csv</text>
      <text preserveWhitespace>{`Header + Product 1 + Product 2 + Product 3 + Product 4`}</text>
    </box>
    <row justify="center">
      <icon name="arrow-down" size="lg"/>
    </row>
    <box border radius="md" padding={3} gap={1}>
      <text weight="medium">One string: `content`</text>
      <text color="secondary" size="sm">The complete file text is stored in one variable.</text>
    </box>
  </box>
  <divider color="subtle"/>
  <box gap={1}>
    **Record-by-record processing**

    <box background="surface-secondary" radius="md" padding={3} gap={1}>
      <text color="secondary" size="sm">products.csv</text>
      <text preserveWhitespace>{`Header → Product 1 → Product 2 → Product 3 → Product 4`}</text>
    </box>
    <row justify="center">
      <icon name="arrow-down" size="lg"/>
    </row>
    <box border radius="md" padding={3} gap={2}>
      {#each ["Product 1: process fields","Product 2: process fields","Product 3: process fields","Product 4: process fields"] as item}
        <row align="center" gap={2}>
          <icon name="check-circle" size="sm" color="success"/>
          <text>{item}</text>
        </row>
      {/each}
      <text color="secondary" size="sm">The program handles each parsed record in turn.</text>
    </box>
  </box>
</box>

**Remember:** `file.read()` is a file-reading method; `csv.reader()` and `csv.DictReader()` are CSV-parsing tools. The key difference is not simply the number of lines printed, but whether your code receives raw text or structured records.

---

## 6. Write CSV Rows with `csv.writer()`

So far, the lesson has focused on reading data. Python can also create CSV files.

Use `csv.writer()` when your rows are represented as lists. `writerow()` writes one row, while `writerows()` writes multiple rows.

```python
import csv

rows = [
    ["product_id", "name", "price", "quantity"],
    ["P201", "USB-C Hub", 1499, 10],
    ["P202", "Phone Stand", 399, 30],
]

with open("new_products.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(rows)

print("CSV file created.")
```

Output:

```text
CSV file created.
```

The resulting `new_products.csv` file contains:

```csv
product_id,name,price,quantity
P201,USB-C Hub,1499,10
P202,Phone Stand,399,30
```

Open `new_products.csv` in Excel to verify that its header and two product records appear in separate columns and rows.

**Important:** Mode `"w"` creates a file or replaces existing content. Use it only when creating a new file or when replacing the file is intentional.

## 7. Write Dictionaries with `csv.DictWriter()`

Use `csv.DictWriter()` when each record is represented as a dictionary. Specify the column names and their order through `fieldnames`.

```python
import csv

products = [
    {"product_id": "P301", "name": "Webcam", "price": 2499},
    {"product_id": "P302", "name": "Headphones", "price": 1799},
]

fieldnames = ["product_id", "name", "price"]

with open("accessories.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(products)

print("Accessory records saved.")
```

Output:

```text
Accessory records saved.
```

The resulting file contains:

```csv
product_id,name,price
P301,Webcam,2499
P302,Headphones,1799
```

`writeheader()` writes the column names as the first row. Each dictionary should use keys that match the intended column names.

## 8. Append a Row to an Existing CSV

Use mode `"a"` to append data without replacing existing rows. If the file already contains a header, do not write the header again.

```python
import csv

new_product = ["P105", "Bluetooth Speaker", 2199, 8]

with open("products.csv", "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(new_product)

print("New product appended.")
```

Output:

```text
New product appended.
```

This example assumes that `products.csv` already exists and uses the same four columns. If you run the script repeatedly, it appends the same product each time. A real application may need to check for duplicate product IDs.

After running the code, reopen or refresh the CSV in Excel to see the appended row.

---

## 9. Handle Common CSV Errors

### File not found

If the requested file does not exist at the supplied path, Python raises `FileNotFoundError`.

```python
try:
    with open("missing_products.csv", "r", newline="", encoding="utf-8") as file:
        import csv
        reader = csv.reader(file)
        rows = list(reader)
except FileNotFoundError:
    print("Product CSV file was not found.")
```

Output:

```text
Product CSV file was not found.
```

### Invalid numeric data

Converting a value such as `"not-a-price"` to an integer raises `ValueError`.

```python
price_text = "not-a-price"

try:
    price = int(price_text)
except ValueError:
    print("Price must be a whole number.")
```

Output:

```text
Price must be a whole number.
```

### Missing or unexpected column names

If your code tries to access `product["name"]` but the CSV heading is spelled differently or is missing, the code may raise `KeyError`.

Check the first row of the CSV file and make sure the column names match those used in your program.

### Unexpected CSV structure

If the file uses a delimiter other than a comma, the reader may not split the fields as expected. Check the file contents and use the appropriate delimiter when necessary. The sample files in this lesson use commas.

---

## 10. Worked Example — Calculate Total Catalogue Stock Value

eCOMMart wants to calculate the value of its available product stock. Use the same `products.csv` file from Section 1.

For each product:

\[
\text{Stock value} = \text{Price} \times \text{Quantity}
\]

The program processes each record individually, calculates its stock value, and adds it to a running total.

```python
import csv

total_value = 0

with open("products.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for product in reader:
        price = int(product["price"])
        quantity = int(product["quantity"])

        stock_value = price * quantity
        total_value += stock_value

        print(f'{product["name"]}: ₹{stock_value}')

print(f"Total stock value: ₹{total_value}")
```

Expected output:

```text
Wireless Mouse: ₹19975
Keyboard: ₹23382
Laptop Stand: ₹11988
USB-C Hub: ₹14990
Total stock value: ₹80336
```

This example combines file handling, CSV parsing, dictionaries, loops, type conversion, and arithmetic.

---

## Practice Tasks

Complete the tasks in order. Use the same `products.csv` file created in Section 1 unless a task specifies a different filename.

### Task 1 — Inspect the CSV in Excel

**Goal:** Understand how the same CSV data appears in a spreadsheet.

1. Open `products.csv` in Microsoft Excel.
2. Confirm that `product_id`, `name`, `price`, and `quantity` appear as separate columns.
3. Confirm that each product occupies its own row.
4. Identify the header row and count the product records.
5. Do not save the file as `.xlsx` for this task; keep the original `products.csv`.

**Check your result:** You should see four product records below the header row.

### Task 2 — Read the Entire File as One String

**Goal:** Use `read()` and inspect its return type.

1. Open `products.csv` using `open()` in read mode.
2. Use `file.read()` to store the entire content in a variable named `content`.
3. Print `type(content).__name__`.
4. Print the contents.
5. Close the file using a `with open(...)` block.

Expected first line of output:

```text
str
```

The CSV text should follow.

### Task 3 — Process Records One at a Time

**Goal:** Use `csv.DictReader()` to print each product name and price.

1. Import the `csv` module.
2. Open `products.csv` with UTF-8 encoding and `newline=""`.
3. Create a `csv.DictReader`.
4. Iterate over each product.
5. Print the product name and price.
6. Do not print the header as if it were a product.

Expected output:

```text
Wireless Mouse: ₹799
Keyboard: ₹1299
Laptop Stand: ₹999
USB-C Hub: ₹1499
```

### Task 4 — Compare the Results

**Goal:** Explain the difference between the two approaches.

1. Run your Task 2 code.
2. Run your Task 3 code.
3. Add a comment under each example describing what it returns or processes.
4. In your own words, explain why `read()` returns a string while `DictReader` provides access to individual fields.

### Task 5 — Write a CSV Report

**Goal:** Create a new CSV file using `csv.DictWriter()`.

Use this data:

```python
products = [
    {"product_id": "P601", "name": "Webcam", "price": 2499},
    {"product_id": "P602", "name": "Headphones", "price": 1799},
]
```

1. Set the column names to `product_id`, `name`, and `price`.
2. Write the records to `task_report.csv`.
3. Include the header using `writeheader()`.
4. Open `task_report.csv` in Excel and verify the result.

Expected output from your Python program:

```text
Report saved.
```

---

## Summary

| Concept | What to remember |
|---|---|
| CSV | A plain-text format for tabular data. |
| Excel view | Excel displays CSV values as cells arranged in rows and columns. |
| `file.read()` | Reads the remaining file content into one string. |
| `csv.reader()` | Parses CSV data and yields rows as lists of strings. |
| `csv.DictReader()` | Parses CSV data and yields records accessible by column name. |
| `next(reader, None)` | Retrieves the next row; often used to skip a header with `csv.reader()`. |
| Type conversion | CSV values are strings; convert numeric values before calculations. |
| `csv.writer()` | Writes rows represented as lists. |
| `csv.DictWriter()` | Writes rows represented as dictionaries. |
| `writerow()` / `writerows()` | Write one row or multiple rows. |
| Mode `"a"` | Appends rows to an existing file. |
| `newline=""` | Recommended when opening CSV files for use with the `csv` module. |

**Key takeaway:** Use `read()` when you need the entire file as raw text. Use `csv.reader()` or `csv.DictReader()` when you need to process CSV records and fields individually. Opening the same CSV in Excel helps you connect the file's text representation to its familiar spreadsheet layout.

*Next: `05_Working_with_JSON.md`*
