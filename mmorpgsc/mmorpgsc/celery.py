import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mmorpgsc.settings')

app = Celery('mmorpgsc')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'msg_every_mon_morning': {
        'task': 'wall.tasks.weekly_post',
        'schedule': crontab(), #hour=8, minute=0, day_of_week='monday'
    },
}
