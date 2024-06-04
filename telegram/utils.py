import os
from datetime import datetime

from aiogram.client.session import aiohttp
from dotenv import load_dotenv

load_dotenv()


async def get_token(
        session: aiohttp.ClientSession,
        email: str,
        password: str
) -> str | None:
    """
    Retrieve authentication token from the API using provided credentials.

    This function sends a POST request to the login endpoint of the API with
    provided email and password to obtain an authentication token.

    Args:
        session (aiohttp.ClientSession): The aiohttp client session.
        email (str): The user's email address.
        password (str): The user's password.

    Returns:
        str or None: The authentication token if successful, otherwise None.
    """
    async with session.post(
            os.getenv("LOGIN_URL"),
            data={
                "email": email,
                "password": password
            }
    ) as response:
        if response.status == 200:
            token_data = await response.json()
            return token_data.get("token")
        else:
            return None


def format_date(date: str) -> str:
    """
    Format ISO-formatted date string to a human-readable format.

    This function takes an ISO-formatted date string and converts it to a
    human-readable format with the year, month, day, hour, minute, and second.

    Args:
        date (str): The ISO-formatted date string.

    Returns:
        str: The formatted date string in the format "YYYY-MM-DD HH:MM:SS".
    """
    timestamp = datetime.fromisoformat(date)
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")
