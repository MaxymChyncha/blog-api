import pathlib
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from user.managers import CustomUserManager


def avatar_image_path(instance: "User", filename: str) -> pathlib.Path:
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
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)
    avatar = models.ImageField(upload_to=avatar_image_path, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email
