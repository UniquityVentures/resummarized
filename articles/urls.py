from django.urls import path

from .views import ArticlePage, progress_view, pin_article
from .components.articles_datalist.articles_datalist import ArticlesDatalistComponent
from .components.for_you_articles.for_you_articles import ForYouArticles
from .components.latest_articles.latest_articles import LatestArticles
from .components.pinned_articles.pinned_articles import PinnedArticles

urlpatterns = [
    path("<int:article_id>/", ArticlePage.as_view(), name="article"),
    path("progress/", progress_view, name="article_generation_progress"),
    path("for_you/", ForYouArticles.as_view(), name="for_you_articles_view"),
    path("latest/", LatestArticles.as_view(), name="latest_articles_view"),
    path("pinned/", PinnedArticles.as_view(), name="pinned_articles_view"),
    path("pin/<int:article_id>/", pin_article, name="pin_article"),
    path(
        "search_datalist/", ArticlesDatalistComponent.as_view(), name="article_search"
    ),
]
