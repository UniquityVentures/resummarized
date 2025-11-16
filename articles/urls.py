from django.urls import path

from .views import ArticlePage

urlpatterns = [
    path('<int:article_id>/', ArticlePage.as_view(), name='article'),
]
