import os

from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_project.settings.local")

# name celery app
# an instance of the application is created
app = Celery("blog_api")

# config_from_object() method: loads any custom configuration from your project settings
# namespace: specifies the prefix that Celery-related settings(E.g. CELERY_BROKER_URL) will have in settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# celery auto-discovers asynchronous tasks in any app.
# It looks for task.py in each application that's added to INSTALLED_APPS
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
