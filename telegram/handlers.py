import os

import aiohttp
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from dotenv import load_dotenv

from telegram.state import SubscriberState
from telegram.utils import get_token, format_date

load_dotenv()


async def get_start(message: Message, bot: Bot) -> None:
    """
    Send a welcome message when the user starts interacting with the bot.

    This function sends a welcome message to the user, introducing the Blog Bot
    and its purpose of providing the newest articles from around the world.

    Args:
        message (Message): The incoming message from the user.
        bot (Bot): The instance of the Telegram bot.
    """
    await bot.send_message(
        message.from_user.id,
        "Welcome to the our Blog Bot 🤖\nWith "
        "the newest articles 📰\nFrom all the World 🌍"
    )


async def get_help(message: Message, bot: Bot) -> None:
    """
    Send a help message listing available commands.

    This function sends a message to the user with a list of available commands
    and their descriptions.

    Args:
        message (Message): The incoming message from the user.
        bot (Bot): The instance of the Telegram bot.
    """
    await bot.send_message(
        message.from_user.id,
        "Available commands:\n"
        "🔹 /start - Start communication with the bot\n"
        "🔹 /help - Shows the list of commands\n"
        "🔹 /latest - Displays the latest article\n"
        "🔹 /subscribe - Allows you to subscribe to notifications from the Blog API"
    )


async def get_latest(message: Message, bot: Bot) -> None:
    """
    Get the latest article from the Blog API and send it to the user.

    This function retrieves the latest article from the Blog API and sends its
    title, content, and publication date to the user.

    Args:
        message (Message): The incoming message from the user.
        bot (Bot): The instance of the Telegram bot.
    """
    async with aiohttp.ClientSession() as session:
        if not (token := await get_token(
                session,
                os.getenv("ADMIN_API_EMAIL"),
                os.getenv("ADMIN_API_PASSWORD")
        )):
            await message.reply("🛑 Failed connection to Blog API. Please try again.")
            return

        headers = {"Authorization": f"Token {token}"}

        async with session.get(
            os.getenv("LAST_ARTICLE_URL"), headers=headers
        ) as response:
            if response.status == 200:
                if article := await response.json():
                    await message.reply(
                        f"🆕 Title: {article.get('title')}\n"
                        f"📰 Content: {article.get('content')}\n"
                        f"⌚️ Published on {format_date(article.get('publication_date'))}"
                    )
                else:
                    await message.answer("🛑 No articles found.")
            else:
                await message.answer("🛑 Failed to get latest article. Please try again.")


async def start_subscribe(message: Message, state: FSMContext) -> None:
    """
    Start the subscription process.

    This function initiates the subscription process
    by asking the user to provide their email address.

    Args:
        message (Message): The incoming message from the user.
        state (FSMContext): The state of the conversation.
    """
    await message.answer(
        "🟢 Let's subscribe.\n"
        "📝 Firstly pass your email."
    )
    await state.set_state(SubscriberState.email)


async def pass_password(message: Message, state: FSMContext) -> None:
    """
    Prompt the user to enter their password.

    This function asks the user to enter their password and updates
    the conversation state
    with the email previously provided by the user.

    Args:
        message (Message): The incoming message from the user containing the password.
        state (FSMContext): The state of the conversation.
    """
    await message.answer("📝 Pass your password.")
    await state.update_data(email=message.text)
    await state.set_state(SubscriberState.password)


async def finish_subscribe(message: Message, state: FSMContext) -> None:
    """
    Complete the subscription process.

    This function completes the subscription process by sending the user's credentials
    to the Blog API for authentication. If successful, the user is subscribed, otherwise,
    an error message is sent.

    Args:
        message (Message): The incoming message from the user containing the password.
        state (FSMContext): The state of the conversation.
    """
    await state.update_data(password=message.text)
    credentials = await state.get_data()
    email = credentials.get("email")
    password = credentials.get("password")

    async with aiohttp.ClientSession() as session:
        if not (token := await get_token(session, email, password)):
            await message.answer(
                "🛑 Failed connection to Blog API.\n"
                "🔄 Please check your credentials and try again.")
            await state.clear()
            return

        headers = {"Authorization": f"Token {token}"}
        data = {"telegram_id": message.from_user.id}

        async with session.patch(
                os.getenv("PROFILE_URL"),
                headers=headers,
                data=data
        ) as response:
            if response.status == 200:
                await message.answer("✅ You're successfully subscribed.")
            else:
                await message.answer("🛑 Something went wrong. Please try again.")
            await state.clear()
