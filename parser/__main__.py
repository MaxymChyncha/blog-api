import asyncio

import aiocron

from parser.database import init_db, write_to_db
from parser.logger import logger
from parser.parse import WebParser


@aiocron.crontab("*/10 * * * *")
async def main() -> None:
    """
    Main function to initialize the database, parse articles, and write them
    to the database.

    This function is scheduled to run every 10 minutes using `aiocron`. It initializes
    the database, creates an instance of the `WebParser`, and parses articles from the
    web. If articles are successfully parsed, they are written to the database and a
    success message is logged. If no articles are found or an error occurs, a warning
    message is logged.

    Returns:
        None
    """
    await init_db()
    parser = WebParser()
    if articles := await parser.parse_all_articles():
        await write_to_db(articles)
        logger.info("Articles were added to database successfully")
    else:
        logger.warning("Articles were not added to database")


if __name__ == "__main__":
    asyncio.get_event_loop().run_forever()
