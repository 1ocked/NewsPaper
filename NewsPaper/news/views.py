# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Post
from django.views import View
from datetime import datetime
#Добавим представление NewsSearch для обработки фильтрации
from .forms import NewsSearchForm


class PostList(ListView):                                      ### Есть видео от ментора!
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, по которому будет выполняться сортировка
    ordering = '-created'  # Сортировка от новых к старым
    # Указываем имя шаблона
    template_name = 'news.html'
    # Имя списка, в котором будут лежать все объекты
    context_object_name = 'posts'
    paginate_by = 10  # Количество постов на странице

class NewsDetails(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'new.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'Post'

class NewsSearch(View):
    def get(self, request):
        form = NewsSearchForm(request.GET)  # Инициализируем форму с GET параметрами
        posts = Post.objects.all()  # Извлекаем все посты

        # Применяем фильтрацию по критериям
        if form.is_valid():
            if form.cleaned_data['title']:
                posts = posts.filter(title__icontains=form.cleaned_data['title'])
            if form.cleaned_data['author']:
                posts = posts.filter(author__username__icontains=form.cleaned_data['author'])
            if form.cleaned_data['date_after']:
                posts = posts.filter(created__gte=form.cleaned_data['date_after'])

        # Пагинация
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Рендерим шаблон с формой и результатами
        return render(request, 'news/search.html', {'form': form, 'page_obj': page_obj})