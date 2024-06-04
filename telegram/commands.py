from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot) -> None:
    """
    Set bot commands for the Telegram bot.

    This function sets the list of available commands for the bot,
    including their descriptions.
    These commands will be available to users interacting with the bot.

    Args:
        bot (Bot): The instance of the Telegram bot.

    Commands:
        /start - Run the bot.
        /help - List of available commands and their descriptions.
        /subscribe - Activate or deactivate subscription for notifications.
        /latest - Get the latest article from the blog.
    """
    commands = [
        BotCommand(
            command="start",
            description="Run the bot"
        ),
        BotCommand(
            command="help",
            description="List of available commands and their descriptions"
        ),
        BotCommand(
            command="subscribe",
            description="Activate or deactivate subscription for notifications"
        ),
        BotCommand(
            command="latest",
            description="Get the latest article from the blog"
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
