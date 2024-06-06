import os

from dotenv import load_dotenv
from sqlalchemy import String, Integer, Column, select
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import DeclarativeBase

from parser.items import Article

load_dotenv()

DATABASE_URL = os.getenv("POSTGRES_URL")

engine = create_async_engine(url=DATABASE_URL)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    """
    Base class for SQLAlchemy ORM models with async attributes.

    Combines `AsyncAttrs` for asynchronous attribute handling
    and `DeclarativeBase` for declarative ORM definitions.
    """

    __abstract__ = True


class ParsedArticle(Base):
    """
    A SQLAlchemy ORM class representing a parsed article.

    Attributes:
        id (int): The primary key and unique identifier for the parsed article.
        title (str): The title of the article, nullable.
        url (str): The URL of the article, nullable.

    Table:
        parsed_articles
    """
    __tablename__ = "parsed_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=True)
    url = Column(String(255), nullable=True)


async def init_db() -> None:
    """
    Initializes the database by creating all tables defined in the metadata.

    This function uses an asynchronous connection to the database engine and
    runs the `create_all` method to create all tables defined in the SQLAlchemy
    Base metadata.

    Returns:
        None
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def write_to_db(articles: list[Article]) -> None:
    """
    Writes a list of articles to the database, avoiding duplicates.

    This function iterates over a list of articles and checks if each article
    already exists in the database based on its URL. If an article does not
    exist, it is added to the session and then committed to the database.

    Args:
        articles (list[Article]): A list of Article objects
        to be written to the database.

    Returns:
        None
    """
    async with async_session() as session:
        for article in articles:
            existing_article = await session.execute(
                select(ParsedArticle).where(ParsedArticle.url == article.url)
            )

            if existing_article.scalar_one_or_none():
                continue

            parsed_article = ParsedArticle(title=article.title, url=article.url)
            session.add(parsed_article)

        await session.commit()
