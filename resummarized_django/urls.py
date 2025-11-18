"""
URL configuration for resummarized_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from .views import HomeRedirectView
from users.views import DashboardPage

urlpatterns = [
    path("", include("django_components.urls")),
    path("admin/", admin.site.urls),
    path("", HomeRedirectView.as_view()),
    path("accounts/", include("users.urls")),
    path('dashboard/', DashboardPage.as_view(), name='dashboard'),
    path("articles/", include("articles.urls")),
    path(r'celery-progress/', include('celery_progress.urls')),  
]

if settings.DEBUG:
    # Include django_browser_reload URLs only in DEBUG mode
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
