"""OPTIONAL/STRETCH ONLY: illustration of an Anthropic SDK boundary.

NOT imported by main.py or needed for any required Week 6 activity.
Students must use only a fake placeholder key this week. No signup,
paid account, real API key, or live Claude request is required.

This file does not send an API request. Its optional client factory would
only construct an SDK object in a future course, if a real key were provided.
Do not invoke that path as part of Week 6.
"""

import os

from dotenv import load_dotenv


PLACEHOLDER_KEY = "YOUR_PLACEHOLDER_KEY_HERE"


def describe_optional_integration():
    """Explain the future connection without using credentials or a network."""
    return (
        "OPTIONAL ONLY: a future LLM could receive a stock alert generated "
        "by stock_alert.py. The Week 6 demo does not call Claude."
    )


def create_anthropic_client():
    """Optional future-use factory; does NOT make a network request.

    This function is NOT part of any core lesson or test. With the Week 6
    placeholder, it intentionally stops before importing the optional SDK.
    """
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY", PLACEHOLDER_KEY)

    if not api_key or api_key == PLACEHOLDER_KEY:
        raise ValueError(
            "Week 6 uses a placeholder Anthropic API key only. "
            "Do not create an SDK client or make a live API call."
        )

    # OPTIONAL future-use path ONLY: anthropic is not in requirements.txt.
    # Merely creating a client does not send a request to Anthropic.
    try:
        from anthropic import Anthropic
    except ImportError as error:
        raise RuntimeError(
            "Optional Anthropic SDK is not installed; it is not needed "
            "for Week 6."
        ) from error

    return Anthropic(api_key=api_key)


if __name__ == "__main__":
    # Running this module is safe: no SDK import or API call is attempted.
    print(describe_optional_integration())
