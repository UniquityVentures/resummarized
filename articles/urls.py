from django.urls import path

from .views import ArticlePage, progress_view
from .components.articles_datalist.articles_datalist import ArticlesDatalistComponent
from .components.for_you_articles.for_you_articles import ForYouArticles
from .components.latest_articles.latest_articles import LatestArticles

urlpatterns = [
    path("<int:article_id>/", ArticlePage.as_view(), name="article"),
    path("progress/", progress_view, name="article_generation_progress"),
    path("for_you/", ForYouArticles.as_view(), name="for_you_articles_view"),
    path("latest/", LatestArticles.as_view(), name="latest_articles_view"),
    path(
        "search_datalist/", ArticlesDatalistComponent.as_view(), name="article_search"
    ),
]
