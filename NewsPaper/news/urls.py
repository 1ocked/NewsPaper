from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, NewsDetails, NewsSearch, PostListView, PostCreateView


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
   path('create/', PostCreateView.as_view(), name='news_create')
]

