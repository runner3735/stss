
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stss.settings")
app = Celery("stss")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()