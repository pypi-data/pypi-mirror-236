"""Module for getting random quote from database of programming quotes."""

import random

from random_quote_generator.quotes import quotes


def get_quote() -> dict:
    """Get random quote from quotes.

    Returns:
        dict: Random quote from quotes.
    """
    return quotes[random.randint(0, len(quotes) - 1)]


if __name__ == "__main__":
    print(get_quote())
