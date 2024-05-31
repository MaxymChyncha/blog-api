from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from article.models import Article
from user.tests.test_user_api import create_user

ARTICLE_URL = reverse("blog:article-list")


class ArticleAPITest(TestCase):

    def setUp(self):
        """
        Set up test data and authenticate a user.
        """
        self.client = APIClient()
        self.user_data = {
            "email": "user@user.com",
            "password": "1234test",
        }
        self.user = create_user(**self.user_data)
        self.client.force_authenticate(user=self.user)
        self.article_data = {
            "title": "Test Article",
            "content": "This is a test article content."
        }

    def test_create_article_authenticated_user(self):
        """
        Test creating an article by an authenticated user.

        Ensure that an article can be created by an authenticated user,
        and the article's author is correctly set to the authenticated user.
        """
        res = self.client.post(ARTICLE_URL, self.article_data, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.get().author, self.user)
        self.assertEqual(Article.objects.get().title, self.article_data["title"])

    def test_create_article_unauthenticated_user(self):
        """
        Test creating an article by an unauthenticated user.

        Ensure that an unauthenticated user cannot create an article
        and receives a 401 Unauthorized response.
        """
        self.client.logout()
        res = self.client.post(ARTICLE_URL, self.article_data, format="json")

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Article.objects.count(), 0)
