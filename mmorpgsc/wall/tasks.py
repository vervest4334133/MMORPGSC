from datetime import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from celery import shared_task

from mmorpgsc import settings

from accounts.models import User

from wall.models import Post


@shared_task
def weekly_post():
    day = datetime.datetime.now()
    last_week = day - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_of_creation__gte=last_week).order_by('time_of_creation')

    forum_users = User.objects.all().values_list('email', flat=True)

    for user in forum_users:
        html_content = render_to_string('notifications/weekly_post.html',
                                    {'link': settings.SITE_URL, 'posts': posts})
        msg = EmailMultiAlternatives(subject="Публикации за неделю:", body='', from_email=settings.DEFAULT_FROM_EMAIL,
                                     to=[user])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
