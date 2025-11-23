from django.urls import path

from .views import LoginPage, LogoutPage, ProfilePage, SignupPage, SignupSuccessPage

urlpatterns = [
    path('login/', LoginPage.as_view(), name='login'),
    path('logout/', LogoutPage.as_view(), name='logout'),
    path('profile/', ProfilePage.as_view(), name='profile'),
    path('signup/', SignupPage.as_view(), name='signup'),
    path('signup/success/', SignupSuccessPage.as_view(), name='signup_success'),
]
