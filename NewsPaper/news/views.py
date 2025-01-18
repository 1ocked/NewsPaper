# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Post
from django.views import View
from datetime import datetime
#Добавим представление NewsSearch для обработки фильтрации
from .forms import NewsSearchForm
from .filters import PostFilter
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin #Для того чтобы добавить проверку аутентификации в класс ArticleUpdateView, нужно использовать миксин LoginRequiredMixin



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


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'new_edit.html'
    fields = ['author', 'title', 'text', 'cats']
    success_url = reverse_lazy('news_list')
    permission_required = 'news.add_post' ########## Задание 11
class PostUpdateView(LoginRequiredMixin, UpdateView):  #http://127.0.0.1:8000/news/12/update/
    model = Post
    fields = ['author', 'title', 'text', 'cats']
    template_name = 'new_edit.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.add_post'  ########## Задание 11

class PostDeleteView(LoginRequiredMixin, DeleteView): #http://127.0.0.1:8000/news/12/delete/
    model = Post
    template_name = 'new_delete.html'
    success_url = reverse_lazy('news_list')
# class PostDeleteView(DeleteView):  #http://127.0.0.1:8000/news/12/delete/
#     model = Post
#     fields = ['author', 'title', 'text', 'cats']
#     template_name = 'new_delete.html'
#     success_url = reverse_lazy('news_list')

# Создание форм Артикля

#Представление для создания статьи (/articles/create/)
class ArticleCreateView(CreateView):
    model = Post
    template_name = 'article_create.html'  # Укажите ваш шаблон
    fields = ['title', 'text', 'cats']  # Поля для формы, 'post_type' не указываем, так как оно скрыто
    permission_required = 'news.add_post'  ########## Задание 11

    def form_valid(self, form):
        form.instance.post_type = Post.article  # Устанавливаем тип поста как 'статья'
        form.instance.author = self.request.user.author  # Устанавливаем автора, если привязка есть
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.object.pk})  # Перенаправление на страницу статьи после создания


#Представление для редактирования статьи (/articles/<int:pk>/edit/)
class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'article_edit.html'  # Укажите ваш шаблон
    fields = ['title', 'text', 'cats']  # Поля для формы, 'post_type' не указываем
    permission_required = 'news.add_post'  ########## Задание 11

    # Переопределяем метод form_valid для того, чтобы установить тип поста как статью
    def form_valid(self, form):
        form.instance.post_type = Post.article  # Убедитесь, что тип поста остаётся статьей
        return super().form_valid(form)

    # Переопределяем метод get_success_url для перенаправления на страницу статьи
    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.object.pk})  # Перенаправление на страницу статьи после успешного редактирования


#3. Представление для удаления статьи (/articles/<int:pk>/delete/)
class ArticleDeleteView(DeleteView):
    model = Post
    template_name = 'article_confirm_delete.html'  # Шаблон для подтверждения удаления
    context_object_name = 'article'  # Название переменной в шаблоне
    success_url = reverse_lazy('article_list')  # Перенаправление на страницу списка статей после удаления

# class ArticleDetail(DetailView):
#     # Модель всё та же, но мы хотим получать информацию по отдельному товару
#     model = Post
#     # Используем другой шаблон — product.html
#     template_name = 'article_detail.html'
#     # Название объекта, в котором будет выбранный пользователем продукт
#     context_object_name = 'article'