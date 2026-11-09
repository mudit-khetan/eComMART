"""Core, offline stock-alert rules for the Week 6 eComMART demo.

This module has no database, configuration, or AI dependencies.
The same inputs always give the same results, making it easy to test.
"""


def is_low_stock(quantity, threshold):
    """Return True only when available units are below the threshold."""
    return quantity < threshold


def format_stock_message(product_name, quantity, threshold):
    """Return a human-readable status message; do not print it here."""
    if is_low_stock(quantity, threshold):
        return (
            f"LOW STOCK: {product_name} has {quantity} units "
            f"(threshold: {threshold})."
        )
    return f"OK: {product_name} has {quantity} units."
