# Independent Challenge: Build the eComMART Product Catalog

**Week 5 · Practice and Review · Independent Challenge**

## Challenge overview

eComMART needs a small Python application that stores product information in a database. Your task is to build a working command-line product catalog using **Python and SQLite**.

You have already practised SQL statements, connecting Python to SQLite, parameterized queries, transactions, and CRUD operations. Now combine those skills into one small application.

**Your goal:** a user should be able to add a product, view products, search for a product, update its details, and remove a product. Changes must remain available after the program exits and starts again.

> Work through the requirements before looking at the separate `solutions.md` file. The challenge is designed to test whether you can assemble the pieces yourself.

---

## 1. Project setup

Use the Week 5 project structure:

```text
Week 5/
├── Examples/
│   ├── setup_database.py
│   └── product_catalog.py
└── 05_Practice_and_Review/
    └── 03_Independent_Product_Catalog_Challenge.md
```

The database file must be stored in the `Examples` folder and named `ecommart.db`.

Use a path based on the location of the Python file so the program does not depend on which folder the terminal happens to be in:

```python
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent / "ecommart.db"
```

If you run `product_catalog.py` from the `Examples` folder, this path points to `Examples/ecommart.db`.

### Database schema

Use the existing `products` table. Do not create additional tables for this challenge.

| Column | SQLite type | Requirement |
|---|---|---|
| `product_id` | `INTEGER` | Primary key |
| `name` | `TEXT` | Required |
| `category` | `TEXT` | Required |
| `price` | `REAL` | Required; must be greater than zero |
| `stock` | `INTEGER` | Required; must be zero or greater |

The starter database contains these products:

| Product ID | Name | Category | Price | Stock |
|---:|---|---|---:|---:|
| 101 | Wireless Barcode Scanner | Scanners | 3499.00 | 24 |
| 102 | Thermal Label Roll | Shipping Supplies | 450.00 | 120 |
| 103 | USB-C Docking Station | Accessories | 6799.00 | 8 |

Run `setup_database.py` first if you have not created the database yet. Check its instructions before running it again: setup scripts may reset starter data, depending on how they were written. Do not rerun a reset script after you have added your own practice products unless you are happy to restore the starter data.

---

## 2. What you must build

Create `Examples/product_catalog.py`. Your program should present a simple menu, perform the selected operation, then return to the menu until the user chooses to exit.

Use a loop for the menu and functions to keep each task separate.

### Required menu

Your menu must offer these choices:

```text
========== eComMART Product Catalog ==========
1. View all products
2. Search for a product by ID
3. Add a product
4. Update a product
5. Delete a product
6. Exit
Choose an option:
```

You may improve the wording or presentation, but keep all six capabilities.

### Required functions

Use these function names so that your implementation is easy to review:

```python
def get_connection():
    """Open and return a connection to the eComMART database."""
    pass

def view_all_products():
    """Display every product in a readable format."""
    pass

def get_product_by_id(product_id):
    """Return one product by ID, or None if it does not exist."""
    pass

def add_product(name, category, price, stock):
    """Insert a valid product and report the outcome."""
    pass

def update_product(product_id, name, category, price, stock):
    """Update an existing product and report whether it was found."""
    pass

def delete_product(product_id):
    """Delete a product only when the requested ID exists."""
    pass

def main():
    """Run the menu until the user chooses to exit."""
    pass
```

You can add helper functions—for example, to validate input or display a single product. Each function should have one clear responsibility.

**Important:** the `pass` statements are placeholders, not working implementations. Replace them with your own code.

---

## 3. Functional requirements

### Task A — View all products

- Retrieve all rows from `products`.
- Display the ID, name, category, price, and stock for each product.
- Format prices consistently, for example `₹3,499.00`.
- If there are no products, display a helpful message instead of showing an empty result without explanation.

### Task B — Search by product ID

- Ask the user for a product ID.
- Retrieve only the matching row using a parameterized query.
- Display the product if it exists.
- If it does not exist, display a message such as `No product found with ID 999`.
- Do not treat a missing product as a program error.

### Task C — Add a product

Ask for the product name, category, price, and stock quantity.

Validate the input before inserting it:

- Name must not be blank.
- Category must not be blank.
- Price must be numeric and greater than zero.
- Stock must be a whole number greater than or equal to zero.
- Do not allow the user to provide a duplicate `product_id`; SQLite should generate the primary key automatically for a new row.

After a successful insert, report that the product was added. If validation fails, explain what the user needs to correct.

### Task D — Update a product

- Ask for the product ID to update.
- Check whether the product exists before asking for replacement details.
- Ask for the new name, category, price, and stock.
- Apply the same validation rules used when adding a product.
- Use a parameterized `UPDATE` statement.
- Report whether the update succeeded or the product ID was not found.

For this challenge, replace all four editable fields rather than implementing a partial-update feature.

### Task E — Delete a product

- Ask for the product ID.
- Check whether the product exists.
- If it exists, ask the user to confirm deletion before proceeding.
- Delete only after the user confirms.
- If the ID does not exist or the user cancels, leave the database unchanged.
- Display a clear result message.

### Task F — Exit cleanly

- Choosing option 6 should end the menu loop.
- Display a short closing message.
- Close every database connection after its operation, including when an exception occurs.

---

## 4. Technical requirements

Your solution must satisfy all of the following:

- Use Python's built-in `sqlite3` module.
- Use the `products` table defined above.
- Use `?` placeholders for values in SQL statements.
- Do not build SQL by concatenating user input into the query.
- Use `SELECT`, `INSERT`, `UPDATE`, and `DELETE` for the appropriate operations.
- Use a function for each main operation.
- Use `try`/`except` where user input or database operations can fail.
- Close connections reliably. Remember that `with sqlite3.connect(...) as connection` manages transaction commit/rollback, but does not automatically close the connection.
- Keep database access and menu interaction reasonably organised. Avoid placing the entire program inside one enormous function.
- Do not print a success message before confirming that the database operation actually succeeded.

---

## 5. Suggested implementation sequence

Build the program in small steps. Test each step before adding the next one.

1. **Connect:** implement `get_connection()` and confirm that the database opens.
2. **Read:** implement `get_product_by_id()` and `view_all_products()`.
3. **Create:** implement validation and `add_product()`.
4. **Update:** implement `update_product()` and check the affected row count.
5. **Delete:** implement confirmation and `delete_product()`.
6. **Menu:** connect the functions to the six menu options.
7. **Robustness:** test invalid inputs, missing IDs, and repeated runs.

Do not attempt to write the whole program at once. A working read operation is a useful milestone before you implement changes to the database.

---

## 6. Test checklist

Use the checklist as you work. Tick each item only after you have actually tested it.

- [ ] The application starts when launched from the `Examples` folder.
- [ ] All three starter products appear when you choose **View all products**.
- [ ] Searching for ID `101` displays Wireless Barcode Scanner.
- [ ] Searching for an unused ID, such as `999`, displays a helpful not-found message.
- [ ] Adding a valid product succeeds.
- [ ] Adding a product with a blank name is rejected.
- [ ] Adding a product with a blank category is rejected.
- [ ] A price of `0` or a negative price is rejected.
- [ ] A non-numeric price is rejected.
- [ ] Negative stock and fractional stock are rejected.
- [ ] Updating an existing product changes the stored values.
- [ ] Updating an unknown ID does not create a new row.
- [ ] Cancelling a deletion leaves the product in the database.
- [ ] Confirming a deletion removes the selected product.
- [ ] The program handles an invalid menu option without crashing.
- [ ] Choosing Exit returns control to the terminal.
- [ ] After exiting and starting the program again, saved changes are still present.

For add/update/delete tests, use a disposable practice product rather than modifying or deleting a starter product you want to keep.

---

## 7. Sample interaction

Your exact formatting may differ, but the interaction should be similarly clear:

```text
========== eComMART Product Catalog ==========
1. View all products
2. Search for a product by ID
3. Add a product
4. Update a product
5. Delete a product
6. Exit
Choose an option: 2

Enter product ID: 101

Product found
ID:       101
Name:     Wireless Barcode Scanner
Category: Scanners
Price:    ₹3,499.00
Stock:    24
```

A missing product should produce a normal message, not a traceback:

```text
Enter product ID: 999
No product found with ID 999.
```

An invalid price should be rejected with an explanation:

```text
Enter price: -25
Price must be greater than zero. Please try again.
```

You may either re-prompt the user or return to the menu after invalid input, provided the application remains stable and explains the problem.

---

## 8. Quality expectations

A strong solution should be easy for another beginner to read and test.

- Use descriptive variable and function names.
- Keep validation rules consistent between adding and updating products.
- Avoid duplicated code when a small helper function would make the program clearer.
- Use parameterized queries for every user-supplied SQL value.
- Make messages specific: say which product ID was not found or which field needs correction.
- Keep the user in control of destructive actions by requiring deletion confirmation.
- Ensure that a failed operation does not leave the database in a partially updated state.

### Self-review rubric

| Area | What success looks like |
|---|---|
| Database | Uses the correct SQLite database and schema |
| CRUD | All four create, read, update, and delete operations work |
| Validation | Blank and invalid values are rejected clearly |
| SQL safety | User values are passed through `?` parameters |
| Reliability | Connections close and expected errors are handled |
| Usability | Menu and feedback messages are understandable |
| Persistence | Changes remain after restarting the application |

---

## 9. Optional extensions

Complete these only after every required test passes.

1. **Search by category:** allow users to list all products in a chosen category.
2. **Low-stock report:** show products with fewer than 10 units in stock.
3. **Sort by price:** display products from lowest to highest price.
4. **Stock adjustment:** let a user add or subtract stock while preventing negative quantities.
5. **Summary report:** display the total number of products and the total units in stock.

Use parameterized SQL for any user-provided search values in these extensions.

---

## 10. Completion criteria

You are finished when:

- all six menu choices work;
- the required test checklist passes;
- the database keeps changes after a restart;
- invalid input and missing IDs are handled without unexpected crashes; and
- your code is organised into small, understandable functions.

Before moving on, explain to yourself how a product moves through the application:

**User input → validation → parameterized SQL → SQLite database → result handling → user feedback**

If you can explain each step and trace it through your own code, you have practised the core skills of Week 5.

**Next:** use `solutions.md` to compare your approach with a reference solution after you have made a genuine attempt.
