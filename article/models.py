from django.contrib.auth import get_user_model
from django.db import models


class Article(models.Model):
    """
    Model representing an article in the blog.

    Attributes:
        title (str): The title of the article. Maximum length is 255 characters.
        content (str): The main content of the article.
        publication_date (datetime): The date and time when the article was published.
                                     Automatically set to the current date and time when the article is created.
        author (User): The author of the article. References a user from the user model.
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
