from django.contrib import admin

from article.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_date")
    search_fields = ("title", "content")
    list_filter = ("publication_date",)
