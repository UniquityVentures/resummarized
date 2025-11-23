from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, FormView

import logging
from .forms import LoginForm, ProfileForm

from .forms import SignupForm

from django.urls import reverse_lazy

logger = logging.getLogger(__name__)

# Server-side rendered views
class LoginPage(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True
    next_page = reverse_lazy("homepage")


class LogoutPage(LogoutView):
    next_page = 'login'

class ProfilePage(FormView):
    template_name = 'profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy("homepage")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class HomePageView(TemplateView):
    def get_context_data(self, **kwargs):
        from articles.models import Article
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user'] = self.request.user
            context['for_you'] = self.request.user.for_you()[:3]
        context['latest'] = Article.objects.all().order_by('-id')[:3]
        return context
    def get_template_names(self):
        if self.request.user.is_authenticated:
            return "dashboard.html"
        return "homepage.html"



class SignupPage(FormView):
    template_name = 'signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('signup_success')
    
    def form_valid(self, form):
        # Save the user
        form.save()
        return super().form_valid(form)


class SignupSuccessPage(TemplateView):
    template_name = 'signup_success.html'
