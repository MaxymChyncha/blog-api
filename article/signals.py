import os

import requests
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from dotenv import load_dotenv

from article.models import Article

load_dotenv()


User = get_user_model()


@receiver(post_save, sender=Article)
def send_telegram_notification(sender, instance, created, **kwargs):
    """
    Send Telegram notification to users with telegram_id field filled when a new article is created.
    """
    if created:
        users_with_telegram_id = (
            User.objects.filter(telegram_id__isnull=False).exclude(telegram_id="")
        )

        for user in users_with_telegram_id:
            telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
            chat_id = user.telegram_id
            message = f"📰 New article was added to Blog API: {instance.title}"

            url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
            params = {"chat_id": chat_id, "text": message}
            requests.post(url, data=params)
