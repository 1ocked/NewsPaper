# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Post
from django.views import View
from datetime import datetime
#Добавим представление NewsSearch для обработки фильтрации
from .forms import NewsSearchForm
from .filters import PostFilter
from django_filters.views import FilterView



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
        #!!!!!return render(request, 'news/search.html', {'form': form, 'page_obj': page_obj})
        return render(request, 'search.html', {'form': form, 'page_obj': page_obj})

#Добавление фильтрации 'Поиска по дате'
class PostListView(FilterView):
    model = Post
    filterset_class = PostFilter  # Указываем фильтр
    template_name = 'data_search.html'
    context_object_name = 'filter'  # Название переменной в контексте для фильтра


class PostCreateView(CreateView):
    model = Post
    # template_name = 'news_edit.html'  # Указываем шаблон new_edit.html
    template_name = 'new_edit.html'  # Указываем шаблон new_edit.html
    fields = ['title', 'text', 'cats', 'post_type']  # Поля формы для создания новости
    success_url = reverse_lazy('news_list')  # Направление на страницу списка новостей после успешного создания
    # model = NewsSearchForm
    # form_class = Post
    # template_name = 'news/create.html'

    def form_valid(self, form):
        # Сохраняем форму и устанавливаем автора (или можно оставить для редактирования через админку)
        form.instance.author = self.request.user.author  # Пример, если автор связан с User
        return super().form_valid(form)

    def get_success_url(self):
        # После создания перенаправляем на страницу новостей
        return reverse_lazy('news_list')  # Замените на ваше имя URL для списка новостей