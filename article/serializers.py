from rest_framework import serializers

from article.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Article model.

    This serializer handles the serialization and deserialization of
    Article instances.
    """
    class Meta:
        model = Article
        fields = ["id", "title", "content", "publication_date", "author"]
        read_only_fields = ["id", "publication_date", "author"]
