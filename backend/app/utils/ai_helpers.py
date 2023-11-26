from typing import Any


def individual_serial(review: dict[str, Any]) -> dict[str, str]:
    """
    Function that returns only the title and text fields from a
    model review document.

    Args:
        review: dict[str, Any]- model review

    Return:
        dict[str, str] - dictionary
    """
    return {"title": review["title"], "text": review["text"]}


def list_serial(reviews: list[dict[str, Any]]) -> list[dict[str, str]]:
    """
    Function that returns a list of all reviews with just the
    text and title fields.

    Args:
        reviews: list[dict[str, Any]]

    Return:
        list[dict[str, str]]
    """
    return [individual_serial(review) for review in reviews]
