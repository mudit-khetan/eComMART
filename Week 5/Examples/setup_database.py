"""
Create the eComMART SQLite database and insert starter products.

Run this script from any working directory:
    python setup_database.py

The database file is created beside this script:
    Examples/ecommart.db

Safety note:
    This script preserves existing product data. It creates the table if needed
    and inserts the starter products only when their product IDs do not already
    exist. It does not delete or reset existing rows.
"""

import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent / "ecommart.db"

STARTER_PRODUCTS = [
    (101, "Wireless Barcode Scanner", "Scanners", 3499.00, 24),
    (102, "Thermal Label Roll", "Shipping Supplies", 450.00, 120),
    (103, "USB-C Docking Station", "Accessories", 6799.00, 8),
]


def setup_database():
    """Create the products table and add any missing starter products."""
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    product_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    price REAL NOT NULL CHECK (price > 0),
                    stock INTEGER NOT NULL CHECK (stock >= 0)
                )
                """
            )

            connection.executemany(
                """
                INSERT OR IGNORE INTO products
                    (product_id, name, category, price, stock)
                VALUES (?, ?, ?, ?, ?)
                """,
                STARTER_PRODUCTS,
            )

        print(f"Database ready: {DATABASE_PATH}")
        print("Starter products are present. Existing product data was preserved.")

        rows = connection.execute(
            """
            SELECT product_id, name, category, price, stock
            FROM products
            ORDER BY product_id
            """
        ).fetchall()

        print(f"\nProducts currently in the database: {len(rows)}")
        for product_id, name, category, price, stock in rows:
            print(
                f"ID: {product_id} | {name} | {category} | "
                f"₹{price:,.2f} | Stock: {stock}"
            )

    except sqlite3.Error as error:
        print(f"Database setup failed: {error}")
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    setup_database()
