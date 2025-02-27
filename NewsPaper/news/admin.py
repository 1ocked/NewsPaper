from django.contrib import admin
from .models import Author, Post, Category, PostCategory, Comment

from django_celery_beat.models import PeriodicTask, CrontabSchedule
from datetime import datetime

admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Comment)

schedule, created = CrontabSchedule.objects.get_or_create(
    minute='0',
    hour='8',
    day_of_week='monday',
)

PeriodicTask.objects.create(
    crontab=schedule,
    name='weekly_newsletter',
    task='your_app.tasks.send_weekly_newsletter',
    start_time=datetime.now(),
)