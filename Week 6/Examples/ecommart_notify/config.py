"""Load the local low-stock threshold for the Week 6 eComMART demo.

The .env file holds local settings; an existing shell environment variable
has priority. No Anthropic credentials or network calls are needed.
"""

import os

from dotenv import load_dotenv


def get_low_stock_threshold():
    """Read LOW_STOCK_THRESHOLD and return a validated integer."""
    load_dotenv()
    raw_value = os.getenv("LOW_STOCK_THRESHOLD", "10")

    try:
        threshold = int(raw_value)
    except ValueError as error:
        raise ValueError(
            "LOW_STOCK_THRESHOLD must be a whole number."
        ) from error

    if threshold < 0:
        raise ValueError("LOW_STOCK_THRESHOLD cannot be negative.")

    return threshold
