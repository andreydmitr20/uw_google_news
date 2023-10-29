# celery -A back  worker -P threads --loglevel=info --beat

from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "back.settings")

# create a Celery instance and configure it using the settings from Django
celery_app = Celery("back")

# Load task modules from all registered Django app configs.
celery_app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in all installed apps
celery_app.autodiscover_tasks()
# We used CELERY_BROKER_URL in settings.py instead of:
# app.conf.broker_url = ''

# We used CELERY_BEAT_SCHEDULER in settings.py instead of:
# app.conf.beat_scheduler = ''django_celery_beat.schedulers.DatabaseScheduler'


# configured so we can adjust scheduling
# in the Django admin to manage all
# Periodic Tasks like below
# celery_app.conf.beat_schedule = {
#     "multiply-task-crontab": {
#         "task": "multiply_two_numbers",
#         "schedule": crontab(hour=7, minute=30, day_of_week=1),
#         "args": (16, 16),
#     },
# }
