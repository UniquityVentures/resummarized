from django.views.generic import TemplateView


from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import ArticlePins

# Assuming you have a template fragment called 'articles/_pin_button.html'
from django.template.loader import render_to_string
from django.shortcuts import render
from .models import Article, UserArticleHistory

class ArticlePage(TemplateView):
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_id = self.kwargs.get('article_id')
        context['article'] = Article.objects.get(id=article_id)
        if self.request.user.is_authenticated:
            UserArticleHistory.objects.create(article_id=article_id, user=self.request.user)
            context['history'] = UserArticleHistory.objects.filter(article_id=article_id)
        return context


def progress_view(request):
    task_id = request.GET.get('task_id')
    
    if not task_id:
        return render(request, 'admin/task_error.html', {'message': 'Task ID not provided.'})

    return render(request, 'admin/task_progress.html', {'task_id': task_id})



@require_POST
@login_required
def pin_article(request, article_id):
    """
    Toggles the pin status for an article for the current user.
    Returns an HTML fragment for HTMX to swap the button text/state.
    """
    try:
        article = Article.objects.get(id=article_id)
    except Article.DoesNotExist:
        return HttpResponse(status=404)

    user = request.user
    pinned = False
    
    try:
        pin = ArticlePins.objects.get(article=article, user=user)
        pin.delete()
        
    except ArticlePins.DoesNotExist:
        ArticlePins.objects.create(article=article, user=user)
        pinned = True
    
    context = {
        'article': article,
        'user': user,
        'is_pinned': pinned, 
    }
    
    return HttpResponse(render_to_string('_pin_button.html', context, request=request))
