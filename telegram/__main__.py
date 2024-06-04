import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from dotenv import load_dotenv

from .handlers import (
    get_start,
    get_latest,
    get_help,
    start_subscribe,
    pass_password,
    finish_subscribe
)
from .state import SubscriberState
from .commands import set_commands

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = os.getenv("TELEGRAM_ADMIN_ID")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def start_bot(bot: Bot) -> None:
    """
    Notify the admin that the bot has been started.

    This function sends a message to the admin informing them
    that the bot has been started.

    Args:
        bot (Bot): The instance of the Telegram bot.
    """
    await bot.send_message(ADMIN_ID, text="The bot was started")

dp.startup.register(start_bot)
dp.message.register(get_start, Command(commands="start"))
dp.message.register(get_help, Command(commands="help"))
dp.message.register(start_subscribe, Command(commands="subscribe"))
dp.message.register(pass_password, SubscriberState.email)
dp.message.register(finish_subscribe, SubscriberState.password)
dp.message.register(get_latest, Command(commands="latest"))


async def start() -> None:
    """
    Start the bot.

    This function sets bot commands, starts the polling loop
    to receive updates from Telegram,
    and ensures that the bot session is properly closed when the bot is stopped.
    """
    await set_commands(bot)
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start())
