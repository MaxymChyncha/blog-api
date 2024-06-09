from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode

from config import settings
from user.models import User, PasswordResetToken


def send_reset_password_email(user: User) -> None:
    """
    Sends a password reset email to the specified user.

    This function generates a password reset token for the user, stores
    the token in the database with a timeout of 1 hour, and sends an email
    to the user with a link to reset their password. The link contains
    the generated token as a query parameter.

    Args:
        user (User): The user who requested a password reset.

    Returns:
        None
    """
    token = default_token_generator.make_token(user)
    expiration_time = timezone.now() + timezone.timedelta(hours=1)

    PasswordResetToken.objects.create(
        user=user,
        token=token,
        expires_at=expiration_time
    )

    reset_password_url = reverse("user:password_reset_confirm")
    query_params = urlencode({"token": token})
    url = f"{settings.BACKEND_URL}{reset_password_url}?{query_params}"

    send_mail(
        "Password Reset",
        f"Use the link below to reset your password:\n{url}",
        settings.EMAIL_HOST_USER,
        [user.email],
    )
