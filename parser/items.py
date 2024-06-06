from dataclasses import dataclass


@dataclass
class Article:
    """
    A dataclass representing an article.

    Attributes:
        title (str): The title of the article.
        url (str): The URL of the article.
    """
    title: str
    url: str
