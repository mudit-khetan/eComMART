# Writing and Appending Files
## eCOMMart AI Squad | Week 4

*“Reading helps an application use saved information; writing lets it save the results of its work.”*

## What We Will Cover

1. Open a file in write mode and save text.
2. Understand how write mode differs from append mode.
3. Use `write()` and newline characters to create readable text files.
4. Build a small eCOMMart report from product information.
5. Recognise when writing to a file can replace existing content.

---

## 1. Why Write to a File?

In the previous lesson, you read product names from a text file. Applications also need to save information: eCOMMart might produce a daily stock report, a list of products for review, or a summary of an order.

Python can write text to a file using `open()` and the file object's `write()` method. For this lesson, the examples use plain-text files and the standard library only.

## 2. Write Mode: `"w"`

The `"w"` mode opens a file for writing. If the file does not exist, Python creates it. If it already exists, its existing contents are **truncated** when it is opened in this mode.

```python
file = open("daily_report.txt", "w", encoding="utf-8")
file.write("eCOMMart Daily Report\n")
file.write("Products checked: 4\n")
file.close()

print("Report saved.")
# Output:
# Report saved.
```

After the program runs, `daily_report.txt` contains:

```text
eCOMMart Daily Report
Products checked: 4
```

The `\n` in each string adds a newline, so the next piece of text starts on a new line.

**Important:** Do not use `"w"` when you need to preserve existing content. Opening an existing file in write mode clears its previous contents before new text is written.

## 3. The `write()` Method

The `write()` method writes the string you provide. It does not automatically add a newline at the end.

```python
file = open("message.txt", "w", encoding="utf-8")
file.write("Wireless Mouse")
file.write("USB-C Cable")
file.close()

file = open("message.txt", "r", encoding="utf-8")
content = file.read()
file.close()

print(repr(content))
# Output:
# 'Wireless MouseUSB-C Cable'
```

The two strings were written directly next to each other. Add `\n` when separate lines are required:

```python
file = open("products.txt", "w", encoding="utf-8")
file.write("Wireless Mouse\n")
file.write("USB-C Cable\n")
file.close()

file = open("products.txt", "r", encoding="utf-8")
print(file.read(), end="")
file.close()
# Output:
# Wireless Mouse
# USB-C Cable
```

Here, `end=""` prevents `print()` from adding another newline after the file content. This is useful when you want to display exactly what the file contains.

## 4. Append Mode: `"a"`

Append mode adds new text to the end of a file without clearing its existing contents. If the file does not exist, Python creates it.

```python
file = open("activity_log.txt", "a", encoding="utf-8")
file.write("Checked product stock\n")
file.write("Generated daily summary\n")
file.close()

print("Activity added.")
# Output:
# Activity added.
```

Run this code again and the same two entries will be added again. Append mode preserves existing text, so repeated runs may create duplicate entries unless the program checks what it is recording.

A useful comparison:

| Mode | If the file exists | If the file does not exist |
|---|---|---|
| `"r"` | Reads existing content | Raises `FileNotFoundError` |
| `"w"` | Replaces existing content | Creates the file |
| `"a"` | Adds content at the end | Creates the file |

Use the mode that matches the intended behaviour. The next lesson will explore file modes and `with open(...)` more fully.

## 5. Write a Product List to a File

Imagine the application has already prepared a list of product names in memory. The program can save each name on its own line.

```python
products = ["Wireless Mouse", "USB-C Cable", "Desk Lamp", "Travel Mug"]

file = open("product_export.txt", "w", encoding="utf-8")

for product_name in products:
    file.write(product_name + "\n")

file.close()

print("Product export saved.")
# Output:
# Product export saved.
```

The resulting `product_export.txt` file contains:

```text
Wireless Mouse
USB-C Cable
Desk Lamp
Travel Mug
```

The loop writes each name and then a newline. This is a straightforward way to export simple text records.

## 6. Create a Formatted Stock Report

A text report can include headings and calculated values. The following example writes product names and stock counts from a list of tuples.

```python
inventory = [
    ("Wireless Mouse", 12),
    ("USB-C Cable", 30),
    ("Desk Lamp", 7),
]

file = open("stock_report.txt", "w", encoding="utf-8")
file.write("eCOMMart Stock Report\n")
file.write("=====================\n")

for product_name, stock in inventory:
    file.write(f"{product_name}: {stock} units\n")

file.close()

print("Stock report created.")
# Output:
# Stock report created.
```

The file contains:

```text
eCOMMart Stock Report
=====================
Wireless Mouse: 12 units
USB-C Cable: 30 units
Desk Lamp: 7 units
```

The file content is built one line at a time. The f-string formats each product's name and stock count into a readable record.

## 7. Add a New Entry Without Replacing the Report

Suppose the stock report exists and you want to add a note at the end. Append mode is appropriate when the existing report must be preserved.

```python
file = open("stock_report.txt", "a", encoding="utf-8")
file.write("Review completed by the inventory team.\n")
file.close()

print("Review note appended.")
# Output:
# Review note appended.
```

The new note appears after the existing report. If you instead opened the file with `"w"`, the previous report would be cleared first.

Be careful about line endings: if the existing file does not end with a newline, appended text may appear on the same line as the last existing entry. In this example, every report line was written with `\n`, so the note starts on a new line.

## 8. A Practical Safety Check Before Writing

Because `"w"` can replace an existing file, use clear output filenames and inspect the code before running it. During training, use sample files created specifically for the exercise.

For example:

```python
output_filename = "practice_output.txt"
file = open(output_filename, "w", encoding="utf-8")
file.write("This is a practice report.\n")
file.close()

print(f"Saved to {output_filename}")
# Output:
# Saved to practice_output.txt
```

This keeps the exercise output separate from the input file. Do not write a report back to the same file that holds source data unless the task explicitly requires that behaviour and you have planned for it.

## 9. Common Mistakes

- **Forgetting `\n`:** `write()` does not add a line break automatically.
- **Using `"w"` by accident:** Existing content is truncated when the file is opened.
- **Using `"a"` when a fresh file is required:** Previous content remains and new text is added to it.
- **Appending without a line break:** New text can join the last existing line.
- **Writing the wrong path:** The output may be created in a different working directory than expected.
- **Forgetting to close the file:** In this lesson, close manually opened files after writing. The next lesson introduces `with open(...)` for safer resource management.

---

## Practice Tasks

Complete the tasks in order. Use the same folder for your Python scripts and the sample output files unless your instructor specifies another path.

### Task 1 — Save a Short Report

**Goal:** Write several lines to a text file.

1. Create a script named `write_report.py`.
2. Open `practice_report.txt` in write mode with UTF-8 encoding.
3. Write the heading `eCOMMart Practice Report`.
4. Write `Products reviewed: 4` on the next line.
5. Close the file.
6. Print `Report saved.` and inspect the file to confirm both lines are present.

Expected output:

```text
Report saved.
```

Expected file content:

```text
eCOMMart Practice Report
Products reviewed: 4
```

### Task 2 — Export Product Names

**Goal:** Write a list to a file with one item per line.

1. Create a list containing `Wireless Mouse`, `USB-C Cable`, `Desk Lamp`, and `Travel Mug`.
2. Open `product_export.txt` in write mode.
3. Use a loop to write each product name followed by `\n`.
4. Close the file.
5. Open the output file in read mode and print its contents.
6. Confirm that each product name appears on its own line.

Expected output:

```text
Wireless Mouse
USB-C Cable
Desk Lamp
Travel Mug
```

### Task 3 — Append an Activity Log

**Goal:** Preserve existing content while adding a new entry.

1. Open `activity_log.txt` in write mode and write `Report generated` followed by a newline.
2. Close the file.
3. Reopen the same file in append mode and add `Stock review completed` followed by a newline.
4. Close the file.
5. Read and print the file contents.
6. Run only the append portion one more time and observe that the new entry is added again.
7. Add a comment explaining why append mode is appropriate and why repeated runs may create duplicate entries.

Expected output after the first complete run:

```text
Report generated
Stock review completed
```

## Summary

| Concept | What to remember |
|---|---|
| `"w"` mode | Creates a file or truncates an existing file before writing. |
| `"a"` mode | Creates a file if needed and adds new text at the end. |
| `write()` | Writes the supplied string; it does not add a newline automatically. |
| `\n` | Starts the next piece of text on a new line. |
| Text report | A loop can write multiple records in a readable format. |
| Safe practice | Use a separate output filename and check the mode before running. |

*Next: 03_with_open_and_File_Modes.md*
