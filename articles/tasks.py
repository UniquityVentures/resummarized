from celery import Celery
from .models import (
    Source,
)

from .ai import AIArticleGenerator
from celery_progress.backend import ProgressRecorder

app = Celery("tasks", backend="redis://localhost", broker="redis://localhost")


@app.task(bind=True)
def generate_article(self, source: int):
    source = Source.objects.get(id=source)
    generator = AIArticleGenerator(ProgressRecorder(self), source)
    article = generator.generate_article()
    article.save()
