# News portal API 📰

This API allows you to read, create, and share your articles. Also, you can always connect to our Telegram bot to be
up-to-date with the newest articles. But if that isn't enough for you we also scrape articles from different resources
and allow you the possibility to read them very soon.

## Features
- **Powerful API**: API with possibility of creating your own account and managing all the articles that you create or read.
- **Telegram Bot**: Very convenient bot that allow you to get all the information about new articles from API.
- **Articles Parser**: Get the newest articles every ten minutes.


## Tools and Technologies Used

* Programming language: `Python`
* App framework: `Django`, `DRF`
* Telegram bot: `aiogram`
* Parsing tool: `Httpx`, `BeautifulSoup`
* Database, ORM: `PosgreSQL`, `SQLAlchemy`, `Django ORM`

## Installation

To clone this project from GitHub, follow these steps:

1. **Open your terminal or command prompt.**
2. **Navigate to the directory where you want to clone the project.**
3. **Run the following commands:**
```shell
git clone https://github.com/MaxymChyncha/news-portal-api
python -m venv venv
source venv/bin/activate  #for Windows use: venv\Scripts\activate
```
5. **Fill your .env file using .env.sample as example**


There are links where you can find all the data for it
- Register your TG bot and get a token you can [here](https://t.me/BotFather).
- You can find your Telegram ID using this [bot](https://t.me/username_to_id_bot).
- Find information about how you can adjust your email for sending mails from app you can [here](https://mailtrap.io/blog/gmail-smtp/).

6. **Build and Run Docker:**
```shell
docker-compose build
docker-compose up
```
7. **Run your parser**
```shell
python -m parser
```

## Possible improvements
- Use Celery for creating task for Telegram notifications.
- Add possibility of creating articles using TG bot.
- Add interactions with parsed articles in TG bot.
- Add parser in Dokcer to make running easier.
- Add interaction with logger and TG bot for admin.
- Deploy project on server like AWS.
