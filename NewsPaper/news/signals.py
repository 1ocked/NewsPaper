
from django.urls import reverse
from .models import Post, Subscription
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User


@receiver(post_save, sender=Post)
def send_news_notification(sender, instance, created, **kwargs):
    if created:
        categories = instance.cats.all()  # Получаем все категории, к которым относится пост
        for category in categories:
            subscribers = Subscription.objects.filter(category=category).values_list('user__email', 'user__username')  # Получаем список подписчиков
            for email, username in subscribers:
                # Создаем URL гиперссылки на статью
                post_url = reverse('news_detail', args=[instance.pk])
                full_url = f"{settings.SITE_URL}{post_url}"

                # Отправляем письмо подписчикам
                send_mail(
                    subject=instance.title,  # Заголовок статьи в теме письма
                    message=f'Здравствуй, {username}. Новая статья в твоём любимом разделе! Перейдите по ссылке, чтобы прочитать её: {full_url}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    html_message=f'<h1>{instance.title}</h1><p>{instance.text[:50]}...</p><p>Здравствуй, {username}. Новая статья в твоём любимом разделе! Перейдите по ссылке, чтобы прочитать её: <a href="{full_url}">Читать статью</a></p>'
                )


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject='Добро пожаловать на наш новостной портал!',
            message=f'Здравствуйте, {instance.username}. Добро пожаловать на наш новостной портал!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            html_message=f'<h1>Добро пожаловать!</h1><p>Здравствуйте, {instance.username}. Добро пожаловать на наш новостной портал!</p>'
        )