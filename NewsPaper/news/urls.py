from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, NewsDetails, NewsSearch, PostListView, PostCreateView, PostUpdateView, PostDeleteView
from .views import ArticleCreateView, ArticleUpdateView, ArticleDeleteView

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostList.as_view(), name='news_list'),  # Указываем имя маршрута для списка новостей
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   # Путь к отдельной новости, с использованием первичного ключа (pk)
   path('<int:pk>/', NewsDetails.as_view(), name='news_detail'),  # Указываем имя маршрута для деталей новости
   path('search/', NewsSearch.as_view(), name='news_search'),  # Новый маршрут для поиска
   #path('posts/', PostListView.as_view(), name='news_data_search'),
   path('data_search/', PostListView.as_view(), name='post_data_search'),
   path('create/', PostCreateView.as_view(), name='news_create'),
   path('<int:pk>/update/', PostUpdateView.as_view(), name='news_update'), #http://127.0.0.1:8000/news/12/update/
   path('<int:pk>/delete/', PostDeleteView.as_view(), name='news_delete'),
   path('articles/create/', ArticleCreateView.as_view(), name='article_create'), #http://127.0.0.1:8000/news/articles/create/
   path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
   path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
]

