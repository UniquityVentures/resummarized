from django.urls import path

from .views import ArticlePage, progress_view
from .components.articles_datalist.articles_datalist import ArticlesDatalistComponent

urlpatterns = [
    path("<int:article_id>/", ArticlePage.as_view(), name="article"),
    path("progress/", progress_view, name="article_generation_progress"),
    path(
        "search_datalist/", ArticlesDatalistComponent.as_view(), name="article_search"
    ),
]
