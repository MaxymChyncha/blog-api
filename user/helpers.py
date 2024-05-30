from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from config import settings
from user.models import User


def send_reset_password_email(user: User) -> None:
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    url = f"{settings.BACKEND_URL}/api/user/password_reset_confirm/{uid}/{token}/"
    send_mail(
        "Password Reset",
        f"Use the link below to reset your password:\n{url}",
        settings.EMAIL_HOST_USER,
        [user.email],
    )
