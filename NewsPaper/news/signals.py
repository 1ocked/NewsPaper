from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Post, Subscription

@receiver(post_save, sender=Post)
def send_news_notification(sender, instance, created, **kwargs):
    if created:
        categories = instance.cats.all()  # Получаем все категории, к которым относится пост
        for category in categories:
            subscribers = Subscription.objects.filter(category=category).values_list('user__email', 'user__username')  # Получаем список подписчиков
            for email, username in subscribers:
                # Отправляем письмо подписчикам
                send_mail(
                    subject=instance.title,  # Заголовок статьи в теме письма
                    message=f'Здравствуй, {username}. Новая статья в твоём любимом разделе!',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    html_message=f'<h1>{instance.title}</h1><p>{instance.text[:50]}...</p><p>Здравствуй, {username}. Новая статья в твоём любимом разделе!</p>'
                )
