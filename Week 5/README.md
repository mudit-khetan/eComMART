# Week 5: Python Database Integration

**Course:** AI Engineering Academy — eComMART AI Squad  
**Focus:** SQLite, SQL, Python database integration, and reliable data handling

## 1. Welcome to Week 5

In Week 4, you worked with Python classes and file handling. You learned how an application can represent information using Python objects and save or load data using files.

This week, you will extend that foundation. You will learn how an application can store structured information in a database, retrieve the records it needs, and update them without rebuilding the entire catalog in application code.

We will continue using the **eComMART B2B product catalog**. It gives us a practical setting for learning database concepts: products have names, categories, prices, and stock quantities, and the application needs to find and maintain those records reliably.

By the end of the week, you will build toward a Python application that can add, view, update, and delete product records stored in SQLite. The data will still be available after the application closes and runs again.

## 2. What you will learn

By the end of Week 5, you should be able to:

- Explain why an application may use a database instead of relying only on JSON or CSV files.
- Understand tables, rows, columns, data types, primary keys, and the purpose of other common key types.
- Create and initialize a SQLite database using Python's built-in `sqlite3` module.
- Write basic SQL statements to create a table, insert records, retrieve records, filter results, update values, and delete records.
- Connect Python to SQLite and understand connections, cursors, query parameters, and fetched results.
- Use parameterized queries rather than building SQL by concatenating user input.
- Commit successful changes and understand when rollback is needed.
- Organize database operations into reusable Python functions.
- Handle common errors and verify that data persists between application runs.
- Apply introductory database practices that make code safer and easier to maintain.

## 3. The eComMART scenario

Imagine eComMART is a B2B store that supplies products to business customers. The catalog needs to keep track of the products available for purchase.

We will use these fields throughout the core lessons:

| Field | Purpose | Example |
|---|---|---|
| `product_id` | Identifies a product record | `101` |
| `name` | Product's display name | `Wireless Barcode Scanner` |
| `category` | Product category | `Scanners` |
| `price` | Product price | `3499.00` |
| `stock` | Available quantity | `24` |

The first version of our database will use one table named `products`. This is deliberate: the goal is to learn the foundations clearly before introducing more complicated designs with multiple related tables.

`01_Database_Fundamentals/02_Tables_Records_and_Primary_Keys.md` includes a short, clearly labeled illustration using a hypothetical `orders` table to explain foreign keys and composite keys. That illustration is there to help the concepts make sense; it is not an additional table that students must build for the core project.

## 4. How the learning path works

The lessons follow a gradual path. Each stage introduces concepts that will be used in the next stage.

| Stage | What you will do | Why it matters |
|---|---|---|
| 1. Database fundamentals | Compare files and databases; understand tables and keys | Build a mental model before writing SQL |
| 2. SQLite and SQL | Set up the database and practise SQL operations | Learn how data is structured and changed |
| 3. Python and SQLite | Connect Python, execute queries, and handle results | Use database operations from an application |
| 4. Product catalog | Implement product CRUD operations and persistence checks | Combine the concepts into a working application |
| 5. Practice and review | Complete guided tasks and an independent challenge | Demonstrate that you can apply the ideas yourself |

Do not skip the early concepts just to reach the project. Understanding why a query works will help you debug it later, instead of relying on copying code that you cannot explain.

## 5. Tools and prerequisites

### You should already know

Week 5 builds on the Python skills taught earlier in the academy:

- Variables, strings, numbers, conditionals, loops, and functions.
- Lists and dictionaries.
- Basic classes and objects.
- Reading and writing files.
- Running a Python script and interpreting its output.

You do **not** need prior experience with SQL, relational databases, or database administration. These topics will be introduced from the beginning.

### Tools used this week

- **Python:** runs the application logic.
- **SQLite:** stores and manages the product records in a database file.
- **`sqlite3`:** Python's built-in module for working with SQLite.
- **A code editor and terminal:** used to edit and run the examples.

SQLite is included with Python through the `sqlite3` module, so a separate database server is not required. Before running a lesson, use the Python environment recommended by your instructor and confirm that it can import `sqlite3`.

You can check the module with this small command:

```python
import sqlite3

print(sqlite3.sqlite_version)
```

Run it in your Python environment. It should print the SQLite library version available to that Python installation. If the import fails, check that you are using a standard Python installation that includes the `sqlite3` module and ask your instructor for help with the environment before continuing.

## 6. How to work through the materials

For each lesson:

1. Read the explanation in order.
2. Study the worked example before changing the code.
3. Follow the run instructions exactly, including the working directory when one is specified.
4. Compare your result with the expected output or verification steps.
5. Complete the guided task without looking at the solution first.
6. If something fails, read the error message and consult the troubleshooting notes before changing several things at once.
7. Complete the knowledge check or recap before moving on.

When a lesson asks you to modify a file, save your changes before running the program. If a script creates or updates a database file, make sure you know where that file is being created. SQLite can create a new database file when a path does not point to an existing one, so an incorrect working directory can make it appear that your earlier data has disappeared when the program has actually opened a different file.

## 7. Important conventions used throughout the week

To keep the examples consistent:

- The main table is named `products`.
- The product identifier is `product_id`.
- Product fields are `name`, `category`, `price`, and `stock`.
- The example catalog uses illustrative products and values; these are learning data, not real inventory.
- SQL keywords may be written in uppercase for readability, although SQLite does not require that capitalization.
- Text values in SQL are quoted; numeric values are represented as numbers.
- When Python supplies values to SQL statements, we will use parameterized queries rather than inserting values directly into SQL strings.
- We will use simple functions to keep database operations understandable and reusable.

The lessons will distinguish between **SQL** and **Python**. SQL expresses the database operation; Python connects to the database, supplies parameters, processes results, and applies the application's logic.

## 8. The final outcome

By the end of the learning path, you should be able to explain and demonstrate a small product catalog application that:

- Creates or opens the intended SQLite database.
- Stores product records in a `products` table.
- Adds a new product.
- Retrieves all products or products matching a condition.
- Updates a product's price or stock.
- Deletes a product record when appropriate for the exercise.
- Handles common invalid inputs or database errors with understandable feedback.
- Saves changes and verifies that they remain after the application is restarted.

This is an introductory database project. It is not intended to be a complete production inventory system. We will focus on foundational SQL, safe query practices, clear Python structure, and reliable persistence.

## 9. Folder guide

The Week 5 materials are organized as follows:

```text
Week 5/
├── README.md
├── 01_Database_Fundamentals/
├── 02_SQLite_and_SQL/
├── 03_Python_and_SQLite/
├── 04_Building_the_eComMART_Catalog/
├── 05_Practice_and_Review/
├── Examples/
└── Image/
```

- `01_Database_Fundamentals/` introduces the problem, table structure, and keys.
- `02_SQLite_and_SQL/` prepares the database and teaches SQL operations.
- `03_Python_and_SQLite/` shows how Python runs database operations.
- `04_Building_the_eComMART_Catalog/` combines the skills in the application.
- `05_Practice_and_Review/` contains guided exercises, the independent challenge, and solutions.
- `Examples/` contains runnable code referenced by lessons.
- `Image/` contains selected instructional visuals where they make a concept easier to understand.

The folder guide describes the intended organization. As files are added, use the exact filenames in the repository and follow the links or next-lesson references provided in each lesson.

## 10. Before you begin

Check that you can:

- Run a Python script.
- Import `sqlite3`.
- Locate the folder where you are saving the course materials.
- Read a file's output and identify whether a script completed successfully.

You do not need to create the product database manually at this point. The setup lesson will guide you through that process in a controlled, repeatable way.

**Start here:** `01_Database_Fundamentals/01_Files_vs_Databases.md`

The first lesson connects your Week 4 file-handling knowledge to the reason eComMART will use a database.
