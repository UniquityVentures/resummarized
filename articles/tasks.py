from .models import Source, Article

from .ai import AIArticleGenerator, VideoGenerator
from celery_progress.backend import ProgressRecorder
from resummarized_django.celery import app

@app.task(bind=True)
def generate_video(self, article: int):
    print("Starting article generation task...")
    article = Article.objects.get(id=article)
    generator = VideoGenerator(ProgressRecorder(self), article)
    script = generator.generate_manim_script()
    print(script)
    return script

@app.task(bind=True)
def generate_article(self, source: int):
    print("Starting article generation task...")
    source = Source.objects.get(id=source)
    generator = AIArticleGenerator(ProgressRecorder(self), source)
    article = generator.generate_article()
    article.save()
    article.update_tags()
    generate_video.delay(article.id)


