import asyncio
from typing import Optional, List, Tuple

import httpx
from bs4 import BeautifulSoup, Tag

from parser.items import Article
from parser.logger import logger


class WebParser:
    BASE_URL = "https://news.ycombinator.com/newest"

    def __init__(self):
        """
        Initializes an instance with an asynchronous HTTP client.

        This method sets up an instance of `httpx.AsyncClient` for making
        asynchronous HTTP requests and assigns it to the `client` attribute.

        Attributes:
            client (httpx.AsyncClient): The asynchronous HTTP client instance.
        """
        self.client = httpx.AsyncClient()

    async def parse_all_articles(self) -> List[Optional[Article]]:
        """
        Parses all articles from the specified base URL.

        This method fetches the content of the base URL, parses the HTML to extract
        articles, and then processes each article asynchronously. It returns a
        list of `Article` objects or None if an error occurs during the request.

        Returns:
            List[Optional[Article]]: A list of `Article` objects if successful, or
            None if a request error occurs.
        """
        try:
            response = await self.client.get(self.BASE_URL)
            response.raise_for_status()
            page_soup = BeautifulSoup(response.content, "html.parser")
            articles_soup = page_soup.find_all("tr", class_="athing")
            articles = await asyncio.gather(
                *[
                    self._parse_single_article(article_soup)
                    for article_soup in articles_soup
                ]
            )
            return self._filter_articles(articles)
        except httpx.RequestError as e:
            logger.error(f"Error fetching the page: {e}")
            return None
        finally:
            await self.client.aclose()

    @staticmethod
    def _filter_articles(articles: Tuple[Optional[Article]]) -> List[Article]:
        """
        Filters out None values from a tuple of articles.

        This static method takes a tuple of articles, which may contain None values,
        and returns a list of articles excluding the None values.

        Args:
            articles (Tuple[Optional[Article]]): A tuple of Article
            objects and None values.

        Returns:
            List[Article]: A list of Article objects with None values filtered out.
        """
        return [article for article in articles if article is not None]

    @staticmethod
    def _get_title(article: Tag) -> str | None:
        """
        Extracts and cleans the title text from an HTML tag.

        This static method takes an HTML tag representing an article and
        extracts the text content, removing any leading or trailing whitespace.
        If the text content is not found or an AttributeError occurs, it logs a
        warning and returns None.

        Args:
            article (Tag): A BeautifulSoup Tag object representing an article.

        Returns:
            str | None: The cleaned title text of the article or None if not found.
        """
        try:
            return article.get_text().strip()
        except AttributeError:
            logger.warning(f"Title from {article} could not be extracted.")
            return None

    @staticmethod
    def _get_url(article: Tag) -> str | None:
        """
        Extracts the URL from an HTML tag.

        This static method takes an HTML tag representing an article and
        extracts the value of the "href" attribute, which is assumed to be the URL.
        If the "href" attribute is not found or an AttributeError occurs, it logs a
        warning and returns None.

        Args:
            article (Tag): A BeautifulSoup Tag object representing an article.

        Returns:
            str | None: The URL of the article or None if not found.
        """
        try:
            return article.get("href")
        except AttributeError:
            logger.warning(f"URL from {article} could not be extracted.")
            return None

    async def _parse_single_article(self, article_soup: Tag) -> Optional[Article]:
        """
        Parses a single article from the provided HTML tag.

        This method extracts the title and URL of an article from the given
        BeautifulSoup Tag object. If the article is successfully parsed, it returns
        an Article object. If no article is found or an error occurs, it logs a
        warning or error and returns None.

        Args:
            article_soup (Tag): A BeautifulSoup Tag object representing
            a single article entry.

        Returns:
            Optional[Article]: An Article object if parsing
            is successful, otherwise None.
        """
        try:
            if article := article_soup.find("span", class_="titleline").a:
                return Article(
                    title=self._get_title(article),
                    url=self._get_url(article)
                )
            else:
                logger.warning("No article found in soup.")
        except Exception as e:
            logger.error(f"Error parsing article: {e}")
