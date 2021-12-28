from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Ho_Chi_Minh')

app.config_from_object(settings, namespace='CELERY')

app.conf.beat_schedule = {
    # 'every-30-seconds': {
    #     'task': 'notifications.task.send_review_email_task',
    #     'schedule': 30,
    #     # 'args': (['RELIANCE.NS', 'BAJAJFINSV.NS'],)
    # },
    'every-fifth-day-of-each-month': {
        'task': 'mailer.tasks.send_scheduled_mails',
        # 'schedule': crontab(0, 0, day_of_month='5'),
        'schedule': 30,

    },
}
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
