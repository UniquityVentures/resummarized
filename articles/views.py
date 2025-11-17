from django.views.generic import TemplateView
from django.shortcuts import render
from .models import Article, UserArticleHistory

class ArticlePage(TemplateView):
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_id = self.kwargs.get('article_id')
        context['article'] = Article.objects.get(id=article_id)
        UserArticleHistory.objects.create(article_id=article_id, user=self.request.user)
        context['history'] = UserArticleHistory.objects.filter(article_id=article_id)
        return context


def progress_view(request):
    task_id = request.GET.get('task_id')
    
    if not task_id:
        return render(request, 'admin/task_error.html', {'message': 'Task ID not provided.'})

    return render(request, 'admin/task_progress.html', {'task_id': task_id})
