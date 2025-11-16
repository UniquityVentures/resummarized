from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, FormView

import logging
from .forms import LoginForm, ProfileForm

logger = logging.getLogger(__name__)

# Server-side rendered views
class LoginPage(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True


class LogoutPage(LogoutView):
    next_page = 'login'

class ProfilePage(FormView):
    template_name = 'profile.html'
    form_class = ProfileForm
    success_url = "/accounts/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class DashboardPage(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        from articles.models import Article
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['latest'] = Article.objects.all().order_by('-id')
        return context
