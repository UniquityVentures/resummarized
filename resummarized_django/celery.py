from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resummarized_django.settings')

app = Celery(
    "resummarized_django", broker="redis://localhost:6379/0"
)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
