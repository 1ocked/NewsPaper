# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView
from .models import Post
from datetime import datetime


class PostList(ListView):                                      ### Есть видео от ментора!
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, по которому будет выполняться сортировка
    ordering = '-created'  # Сортировка от новых к старым
    # Указываем имя шаблона
    template_name = 'news.html'
    # Имя списка, в котором будут лежать все объекты
    context_object_name = 'posts'

class NewsDetails(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'new.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'Post'

