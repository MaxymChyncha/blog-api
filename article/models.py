from django.contrib.auth import get_user_model
from django.db import models


class Article(models.Model):
    """
    Serializer for the Article model.

    This serializer handles the serialization and deserialization of
    Article instances.
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
