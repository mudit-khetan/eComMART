"""
Week 5 — eComMART Product Catalog Application

This beginner-friendly console program demonstrates CRUD operations:
    Create — add a product
    Read   — view and search for products
    Update — change a product's details
    Delete — remove a product

Design note:
    This file follows the same separation-of-concerns pattern taught in
    04_Building_the_eComMART_Catalog/: database-access functions return
    data or a status value and never call input()/print() themselves.
    The menu functions handle all user interaction and display. This
    keeps each function easy to read, reuse, and test on its own.

Before running:
    1. Run setup_database.py.
    2. Keep this file and ecommart.db in the same Examples folder.
    3. Run:
         Windows:      python 05_Product_Catalog_App.py
         macOS/Linux:  python3 05_Product_Catalog_App.py

Tip:
    Practise using a disposable product. The program asks for
    confirmation before deleting a product.
"""

import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent / "ecommart.db"


# ---------------------------------------------------------------------------
# Database-access functions.
#
# Each function opens its own connection, performs one database operation,
# and returns data or a status value. None of these functions call input()
# or print() — that keeps them reusable and easy to test on their own.
# ---------------------------------------------------------------------------


def validate_product(name, category, price, stock):
    """Raise ValueError when a product's input is invalid."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Product name must not be empty.")

    if not isinstance(category, str) or not category.strip():
        raise ValueError("Product category must not be empty.")

    if isinstance(price, bool) or not isinstance(price, (int, float)):
        raise ValueError("Price must be a number.")

    if price <= 0:
        raise ValueError("Price must be greater than 0.")

    if isinstance(stock, bool) or not isinstance(stock, int):
        raise ValueError("Stock must be a whole number.")

    if stock < 0:
        raise ValueError("Stock cannot be negative.")


def get_all_products():
    """Return all products ordered by product ID."""
    connection = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = connection.execute(
            """
            SELECT product_id, name, category, price, stock
            FROM products
            ORDER BY product_id
            """
        )
        return cursor.fetchall()
    finally:
        connection.close()


def get_product_by_id(product_id):
    """Return one product tuple, or None if the ID does not exist."""
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
        return cursor.fetchone()
    finally:
        connection.close()


def add_product(name, category, price, stock):
    """Insert a product and return its new product ID.

    product_id is not supplied here: the products table defines
    product_id as an INTEGER PRIMARY KEY, so SQLite assigns the next
    available ID automatically when the INSERT statement omits it.
    """
    validate_product(name, category, price, stock)

    connection = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = connection.execute(
            """
            INSERT INTO products (name, category, price, stock)
            VALUES (?, ?, ?, ?)
            """,
            (name.strip(), category.strip(), float(price), stock),
        )
        new_product_id = cursor.lastrowid
        connection.commit()
        return new_product_id

    except sqlite3.Error:
        connection.rollback()
        raise
    finally:
        connection.close()


def update_product(product_id, name, category, price, stock):
    """Update a product; return True if a matching row was affected."""
    validate_product(name, category, price, stock)

    connection = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = connection.execute(
            """
            UPDATE products
            SET name = ?, category = ?, price = ?, stock = ?
            WHERE product_id = ?
            """,
            (name.strip(), category.strip(), float(price), stock, product_id),
        )

        if cursor.rowcount != 1:
            connection.rollback()
            return False

        connection.commit()
        return True

    except sqlite3.Error:
        connection.rollback()
        raise
    finally:
        connection.close()


def delete_product(product_id):
    """Delete one product; return True if a row was deleted."""
    connection = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = connection.execute(
            "DELETE FROM products WHERE product_id = ?",
            (product_id,),
        )

        if cursor.rowcount != 1:
            connection.rollback()
            return False

        connection.commit()
        return True

    except sqlite3.Error:
        connection.rollback()
        raise
    finally:
        connection.close()


# ---------------------------------------------------------------------------
# User-interaction functions.
#
# These functions handle input() and print(). They call the database
# functions above and decide how to display the result; they do not
# contain any SQL themselves.
# ---------------------------------------------------------------------------


def read_integer(prompt):
    """Read an integer from the user; return None for invalid input."""
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("Please enter a whole number, such as 104.")
        return None


def read_number(prompt):
    """Read a numeric value from the user; return None if invalid."""
    try:
        return float(input(prompt).strip())
    except ValueError:
        print("Please enter a valid number, such as 299 or 299.50.")
        return None


def format_product_row(product):
    """Return one formatted display line for a product tuple."""
    product_id, name, category, price, stock = product
    return (
        f"{product_id:<8}{name[:28]:<30}{category[:20]:<22}"
        f"{price:>10.2f}{stock:>8}"
    )


def view_all_products():
    """Display all products ordered by product ID."""
    try:
        products = get_all_products()
    except sqlite3.Error as error:
        print(f"Could not read products: {error}")
        return

    print("\n--- Product Catalog ---")
    if not products:
        print("No products found.")
        return

    print(f"{'ID':<8}{'Name':<30}{'Category':<22}{'Price':>10}{'Stock':>8}")
    print("-" * 78)
    for product in products:
        print(format_product_row(product))


def search_product():
    """Find and display one product using its ID."""
    product_id = read_integer("Enter the product ID to search for: ")
    if product_id is None:
        return

    try:
        product = get_product_by_id(product_id)
    except sqlite3.Error as error:
        print(f"Could not search for the product: {error}")
        return

    if product is None:
        print(f"No product found with ID {product_id}.")
        return

    print("\nProduct found:")
    print(f"ID:       {product[0]}")
    print(f"Name:     {product[1]}")
    print(f"Category: {product[2]}")
    print(f"Price:    {product[3]:.2f}")
    print(f"Stock:    {product[4]}")


def add_product_menu():
    """Collect input for a new product, then add it.

    The product ID is not requested from the user: SQLite assigns the
    new product_id automatically, the same way add_product() in
    04_Building_the_eComMART_Catalog/02_Implementing_Product_CRUD_Operations.md
    does. This avoids ID collisions and matches that lesson's design.
    """
    print("\n--- Add a Product ---")
    name = input("Product name: ").strip()
    category = input("Category: ").strip()
    price = read_number("Price (must be greater than 0): ")
    stock = read_integer("Stock (0 or greater): ")

    if price is None or stock is None:
        print("Add cancelled: price and stock must both be valid numbers.")
        return

    try:
        new_id = add_product(name, category, price, stock)
        print(f"Product '{name}' added with ID {new_id}.")
    except ValueError as error:
        print(f"Could not add the product: {error}")
    except sqlite3.Error as error:
        print(f"Could not add the product: {error}")


def update_product_menu():
    """Collect input to replace an existing product's details."""
    print("\n--- Update a Product ---")
    product_id = read_integer("Product ID to update: ")
    if product_id is None:
        return

    existing = get_product_by_id(product_id)
    if existing is None:
        print(f"No product found with ID {product_id}.")
        return

    print(f"Current values: {format_product_row(existing)}")
    print("Enter the new values below.")

    name = input("New name: ").strip()
    category = input("New category: ").strip()
    price = read_number("New price (must be greater than 0): ")
    stock = read_integer("New stock (0 or greater): ")

    if price is None or stock is None:
        print("Update cancelled: price and stock must both be valid numbers.")
        return

    try:
        updated = update_product(product_id, name, category, price, stock)
        if updated:
            print(f"Product {product_id} updated.")
        else:
            print(f"No product found with ID {product_id}.")
    except ValueError as error:
        print(f"Could not update the product: {error}")
    except sqlite3.Error as error:
        print(f"Could not update the product: {error}")


def delete_product_menu():
    """Delete a product only after showing it and asking for confirmation."""
    print("\n--- Delete a Product ---")
    product_id = read_integer("Product ID to delete: ")
    if product_id is None:
        return

    product = get_product_by_id(product_id)
    if product is None:
        print(f"No product found with ID {product_id}.")
        return

    print("\nYou selected:")
    print(f"ID:       {product[0]}")
    print(f"Name:     {product[1]}")
    print(f"Category: {product[2]}")
    confirmation = input("Delete this product? Type YES to confirm: ").strip()

    if confirmation != "YES":
        print("Deletion cancelled. No product was removed.")
        return

    try:
        deleted = delete_product(product_id)
        if deleted:
            print(f"Product {product_id} deleted.")
        else:
            print(f"No product found with ID {product_id}.")
    except sqlite3.Error as error:
        print(f"Could not delete the product: {error}")


def show_menu():
    """Display the main menu."""
    print("\n" + "=" * 40)
    print("       eComMART PRODUCT CATALOG")
    print("=" * 40)
    print("1. View all products")
    print("2. Search for a product by ID")
    print("3. Add a new product")
    print("4. Update a product")
    print("5. Delete a product")
    print("6. Exit")


def main():
    """Run the application menu until the user chooses Exit."""
    if not DATABASE_PATH.exists():
        print("Database file not found.")
        print("Run setup_database.py first.")
        return

    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            view_all_products()
        elif choice == "2":
            search_product()
        elif choice == "3":
            add_product_menu()
        elif choice == "4":
            update_product_menu()
        elif choice == "5":
            delete_product_menu()
        elif choice == "6":
            print("Thank you for using the eComMART Product Catalog.")
            break
        else:
            print("Please choose a number from 1 to 6.")


if __name__ == "__main__":
    main()
