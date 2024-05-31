from rest_framework import viewsets

from article.models import Article
from article.serializers import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing articles.

    This viewset provides CRUD operations for articles.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        """
        Perform additional actions during article creation.

        This method is called during article creation to set the author
        of the article to the authenticated user making the request.
        """
        serializer.save(author=self.request.user)
