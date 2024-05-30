import pathlib
import uuid

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import slugify

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


def avatar_image_path(instance: "User", filename: str) -> pathlib.Path:
    filename = (
        f"{slugify(instance.email)}-{uuid.uuid4()}" + pathlib.Path(filename).suffix
    )
    return pathlib.Path("uploads/avatars/") / pathlib.Path(filename)
