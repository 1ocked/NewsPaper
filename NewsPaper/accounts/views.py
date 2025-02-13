
#D93
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from news.models import Category


@login_required
def subscribe_to_category(request, category_id):
    category = Category.objects.get(id=category_id)

    # Проверяем, не подписан ли уже пользователь
    if request.user not in category.subscribers.all():
        category.subscribers.add(request.user)

    return redirect('category_detail', category_id=category.id)  # Перенаправляем на страницу категории