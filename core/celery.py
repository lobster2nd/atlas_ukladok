import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('atlas_ukladok')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
