"""Core Week 6 eComMART test for invalid threshold configuration.

The pytest monkeypatch fixture changes an environment variable only during
this test. It restores the environment afterward and never edits .env.
Using monkeypatch independently is optional for the Week 6 takeaway.
"""

import pytest

from config import get_low_stock_threshold


def test_invalid_threshold_text_raises_error(monkeypatch):
    # Arrange: temporarily set an invalid configuration value.
    monkeypatch.setenv("LOW_STOCK_THRESHOLD", "ten")

    # Act + Assert: rejecting a nonnumeric threshold is correct behavior.
    with pytest.raises(ValueError, match="whole number"):
        get_low_stock_threshold()
