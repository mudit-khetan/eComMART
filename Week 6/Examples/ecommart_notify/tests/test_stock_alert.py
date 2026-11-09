"""Core Week 6 eComMART tests for the low-stock business rule.

Run from the ecommart_notify project folder: python -m pytest -v
These tests require no database, credentials, or AI API calls.
"""

from stock_alert import is_low_stock, format_stock_message


def test_quantity_below_threshold_is_low():
    # Arrange: choose a product quantity and a threshold.
    quantity = 4
    threshold = 10

    # Act: run the function we want to check.
    result = is_low_stock(quantity, threshold)

    # Assert: compare the result with the expected rule.
    assert result is True


def test_quantity_equal_to_threshold_is_not_low():
    # Arrange: a quantity at the boundary is NOT below it.
    quantity = 10
    threshold = 10

    # Act
    result = is_low_stock(quantity, threshold)

    # Assert: this catches accidental use of <= instead of <.
    assert result is False


# OPTIONAL/STRETCH: To test the exact alert wording, add a fourth test
# that calls format_stock_message("Scanner", 4, 10) and checks the text.
