from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

# Set the default settings module for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth.settings')

app = Celery('auth')

# Load task modules from all registered Django app configs
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all registered Django app configs
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
