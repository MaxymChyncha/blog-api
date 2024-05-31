from django.urls import path, include
from rest_framework.routers import DefaultRouter

from article.views import ArticleViewSet

router = DefaultRouter()
router.register("articles", ArticleViewSet, basename="article")

urlpatterns = [
    path("", include(router.urls))
]

app_name = "article"
