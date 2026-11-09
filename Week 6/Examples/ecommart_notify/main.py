"""Run the Week 6 eComMART low-stock notifier (core, offline demo).

This standalone demo uses sample products, not the Week 5 SQLite catalog.
It does not import the optional Anthropic integration or make API calls.
"""

from config import get_low_stock_threshold
from stock_alert import format_stock_message


def main():
    """Read the configured threshold and display each product's stock status."""
    threshold = get_low_stock_threshold()

    # Fresh, in-memory demo data; this is NOT the Week 5 SQLite catalog.
    products = [
        ("Wireless Barcode Scanner", 4),
        ("Thermal Label Roll", 120),
        ("USB-C Docking Station", 8),
        ("Shipping Label Printer", 10),
    ]

    print("=== eComMART Low-Stock Notifier ===")
    for product_name, quantity in products:
        message = format_stock_message(product_name, quantity, threshold)
        print(message)


if __name__ == "__main__":
    main()
