# File Paths and `os.path`

## eCOMMart AI Squad | Week 4

> “A file is useful only when your program can reliably find it.”

## What We Will Cover

1. Understand relative and absolute file paths.
2. Inspect the current working directory.
3. Build paths using Python's `os.path` tools.
4. Check whether a file or directory exists.
5. Use paths with file-handling operations.

---

## 1. Why File Paths Matter

A **file path** tells Python where a file or directory is located. In an eCOMMart project, you might store product data, application settings, and reports in different folders.

Example project structure:

```text
ecommart/
├── app.py
├── data/
│   └── products.json
└── reports/
    └── daily_sales.csv
```

A program that reads `products.json` needs to locate the file correctly. If the path is wrong, Python may raise `FileNotFoundError`.

## 2. Relative and Absolute Paths

A **relative path** describes a location relative to the current working directory or another defined base directory.

```python
data_path = "data/products.json"
```

An **absolute path** describes the location from the root of the file system.

Example on macOS or Linux:

```text
/Users/learner/ecommart/data/products.json
```

Example on Windows:

```text
C:\Users\Learner\ecommart\data\products.json
```

Absolute paths are machine-specific, so they are usually unsuitable for code that must run on many learners' computers. Relative paths are more portable when the project structure is consistent.

## 3. Find the Current Working Directory

The **current working directory** (CWD) is the directory from which the Python process is running. It is not necessarily the directory containing the script.

Use `os.getcwd()` to display it:

```python
import os

print(os.getcwd())
```

Example output:

```text
/Users/learner/ecommart
```

Your output will depend on where you run Python. If a relative path does not work, check the current working directory first.

You can change the working directory with `os.chdir()`, but changing it can make a program's file access harder to predict. Prefer using clear paths rather than changing directories unnecessarily.

## 4. Build Paths with `os.path.join`

Avoid manually joining path parts with a hard-coded slash or backslash. `os.path.join()` uses the appropriate separator for the current operating system.

```python
import os

folder = "data"
filename = "products.json"
file_path = os.path.join(folder, filename)

print(file_path)
```

Example output on macOS or Linux:

```text
data/products.json
```

Example output on Windows:

```text
data\products.json
```

The exact separator depends on the operating system.

### Build a Path from a Base Folder

```python
import os

project_folder = "ecommart"
data_folder = os.path.join(project_folder, "data")
products_file = os.path.join(data_folder, "products.json")

print(products_file)
```

Example output on macOS or Linux:

```text
ecommart/data/products.json
```

Each call combines path components without requiring you to write operating-system-specific separators.

## 5. Check Whether a Path Exists

Use `os.path.exists()` to check whether a file or directory exists. Use `os.path.isfile()` to check specifically for a file and `os.path.isdir()` to check specifically for a directory.

```python
import os

path = "data/products.json"

print(os.path.exists(path))
print(os.path.isfile(path))
print(os.path.isdir("data"))
```

Example output when `data/products.json` exists and `data` is a directory:

```text
True
True
True
```

If the paths do not exist, the results may be `False`. These checks are useful, but a file can still change between checking it and opening it. Your program should continue to handle file-related exceptions where appropriate.

## 6. Use a Path to Open a File

Once you have built the path, pass it to `open()` as you normally would.

```python
import os
import json

data_folder = "data"
filename = "products.json"
file_path = os.path.join(data_folder, filename)

with open(file_path, "r", encoding="utf-8") as file:
    products = json.load(file)

print(f"Loaded {len(products)} products.")
```

Example output when `products.json` contains three products:

```text
Loaded 3 products.
```

This example assumes the file exists, contains valid JSON, and stores a list of products. The path construction works independently of the JSON parsing.

## 7. Create a Folder if Needed

Use `os.makedirs()` to create a directory. Set `exist_ok=True` if the directory may already exist.

```python
import os

reports_folder = os.path.join("ecommart", "reports")
os.makedirs(reports_folder, exist_ok=True)

print("Reports folder is ready.")
```

Output:

```text
Reports folder is ready.
```

This creates the directory and any missing parent directories. If it already exists, `exist_ok=True` prevents Python from raising an error just because the directory is present.

## 8. A Note on Project-Relative Paths

A relative path is resolved from the process's current working directory. If you run the same program from different locations, the same relative path can point to different places.

For a simple training project, running the script from the project root is often sufficient. For a larger project, you can derive paths from the script's own location with `__file__`:

```python
import os

script_folder = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(script_folder, "data")
products_file = os.path.join(data_folder, "products.json")

print(products_file)
```

This assumes the code is saved in a Python script. `__file__` is not generally defined in every interactive environment, such as a standard Python REPL. If you are using a notebook or an interactive terminal, check the working directory with `os.getcwd()` instead.

## 9. Practice Tasks

Complete the tasks in order. Each task builds on the ideas introduced in this lesson.

### Task 1 — Join Path Components

Use `os.path.join()` to combine `"data"` and `"catalogue.csv"`. Print the resulting path.

Example output on macOS or Linux:

```text
data/catalogue.csv
```

On Windows, the separator may be a backslash.

### Task 2 — Check a Path

Use `os.path.exists()` to check whether `"products.json"` exists in your current working directory. Print the Boolean result.

Expected output depends on whether the file exists:

```text
True
```

or

```text
False
```

### Task 3 — Prepare a Reports Folder

Use `os.path.join()` to build the path for a folder named `reports` inside `ecommart`. Use `os.makedirs(..., exist_ok=True)` to create it. Then check whether it exists and print the result.

Expected output:

```text
Reports folder exists: True
```

## Summary

| Tool | Purpose |
|---|---|
| `os.getcwd()` | Get the current working directory |
| `os.chdir()` | Change the current working directory |
| `os.path.join()` | Combine path components |
| `os.path.exists()` | Check whether a path exists |
| `os.path.isfile()` | Check whether a path is a file |
| `os.path.isdir()` | Check whether a path is a directory |
| `os.makedirs()` | Create a directory and missing parent directories |
| `os.path.abspath()` | Convert a path to an absolute path |
| `os.path.dirname()` | Get the directory portion of a path |

Use `os.path` to build paths portably instead of hard-coding separators. Keep the project structure predictable and handle missing files even when you check paths first.

*Next: `02_Loading_Config_from_JSON.md`*
