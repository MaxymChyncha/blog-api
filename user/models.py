import pathlib
import uuid
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from user.managers import CustomUserManager


def avatar_image_path(instance: "User", filename: str) -> pathlib.Path:
    """
    Generate a path for saving user avatar images.

    This function generates a unique file path for saving avatar images uploaded by users.

    Args:
        instance (User): The user instance.
        filename (str): The original filename of the uploaded image.

    Returns:
        pathlib.Path: The generated file path.
    """
    filename = (
        f"{slugify(instance.email)}-{uuid.uuid4()}" + pathlib.Path(filename).suffix
    )
    return pathlib.Path("uploads/avatars/") / pathlib.Path(filename)


class User(AbstractUser):
    """
    Custom user model.

    This model extends the AbstractUser class to include email as the
    unique identifier for authentication.
    """
    username = models.CharField(max_length=63, unique=True, blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)
    avatar = models.ImageField(upload_to=avatar_image_path, blank=True, null=True)
    telegram_id = models.BigIntegerField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email


class PasswordResetToken(models.Model):
    """
    Model to store password reset tokens for users.

    This model stores the password reset tokens generated for users,
    along with the expiration time of each token. It ensures that
    tokens are unique and can be validated to check if they are still
    valid based on their expiration time.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        """
        Check if the token is still valid.

        Returns:
            bool: True if the token is still valid, False otherwise.
        """
        return timezone.now() < self.expires_at

    def __str__(self) -> str:
        return f"{self.user} token. Expires at {self.expires_at}"
