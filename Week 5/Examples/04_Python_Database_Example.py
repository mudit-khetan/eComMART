"""
Week 5 — Python Database Example
eComMART Product Catalog

Purpose:
    Connect to the eComMART SQLite database, read the product
    records, and display them in the terminal.

Before running:
    1. Run setup_database.py.
    2. Keep this file and ecommart.db in the same Examples folder.
    3. Run:
         Windows:      python 04_Python_Database_Example.py
         macOS/Linux:  python3 04_Python_Database_Example.py
"""

import sqlite3
from pathlib import Path


# Find ecommart.db in the same folder as this Python file.
DATABASE_PATH = Path(__file__).resolve().parent / "ecommart.db"


def display_products():
    """Read products from SQLite and display them."""
    if not DATABASE_PATH.exists():
        print("Database file not found.")
        print("Run setup_database.py first, then try again.")
        return

    connection = None

    try:
        # Open a connection to the database file.
        connection = sqlite3.connect(DATABASE_PATH)

        # A cursor is used to execute SQL statements.
        cursor = connection.cursor()

        # Ask SQLite to return the product details.
        cursor.execute(
            """
            SELECT product_id, name, category, price, stock
            FROM products
            ORDER BY product_id;
            """
        )

        # fetchall() collects all rows returned by the query.
        products = cursor.fetchall()

        print("\n" + "=" * 72)
        print("eComMART PRODUCT CATALOG")
        print("=" * 72)

        if not products:
            print("No products were found in the database.")
            return

        # Each row is returned as a tuple of values.
        for product in products:
            product_id, name, category, price, stock = product
            print(f"\nProduct ID : {product_id}")
            print(f"Name       : {name}")
            print(f"Category   : {category}")
            print(f"Price      : {price:.2f}")
            print(f"Stock      : {stock}")

        print("\n" + "=" * 72)
        print(f"Products displayed: {len(products)}")

    except sqlite3.Error as error:
        print("A database error occurred.")
        print(f"Details: {error}")

    finally:
        # Close the connection even if an error occurs.
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    display_products()
