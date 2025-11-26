from .models import (
    Source,
)

from .ai import AIArticleGenerator
from celery_progress.backend import ProgressRecorder
from resummarized_django.celery import app


@app.task(bind=True)
def generate_article(self, source: int):
    print("Starting article generation task...")
    source = Source.objects.get(id=source)
    generator = AIArticleGenerator(ProgressRecorder(self), source)
    article = generator.generate_article()
    article.save()
    article.update_tags()
