from django.views.generic import TemplateView
from .models import Article

class ArticlePage(TemplateView):
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_id = self.kwargs.get('article_id')
        context['article'] = Article.objects.get(id=article_id)
        return context
