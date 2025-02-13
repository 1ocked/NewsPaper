from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Post, Subscription


@shared_task
def send_weekly_newsletter():
    today = timezone.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(created__gte=last_week)

    categories = set(posts.values_list('cats__name', flat=True))
    for category in categories:
        subscribers = Subscription.objects.filter(category__name=category).values_list('user__email', 'user__username')

        for email, username in subscribers:
            post_links = ""
            for post in posts.filter(cats__name=category):
                post_url = f"{settings.SITE_URL}{reverse('news_detail', args=[post.pk])}"
                post_links += f'<li><a href="{post_url}">{post.title}</a></li>'

            send_mail(
                subject=f'Еженедельная рассылка новостей для категории {category}',
                message=f'Здравствуйте, {username}. Вот список новых статей за последнюю неделю в категории {category}.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=f'<h1>Новые статьи за неделю</h1><ul>{post_links}</ul>'
            )
