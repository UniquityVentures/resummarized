from django.urls import reverse
from django.views.generic.base import RedirectView


class HomeRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        user = getattr(self.request, "user", None)
        if user is not None and user.is_authenticated:
            return reverse('dashboard')
        return reverse("login")
