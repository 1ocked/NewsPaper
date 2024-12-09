import django_filters
from .models import Post
from django import forms

class PostFilter(django_filters.FilterSet):
    #Фильтрация по title и author позволяет пользователю искать посты по названию и автору
    title = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(field_name='author__user__username', lookup_expr='icontains')
    #Фильтрация по дате (date_after, date_before) позволяет фильтровать посты по дате их создания.
    date_after = django_filters.DateFilter(field_name='created', lookup_expr='gte', widget=forms.DateInput(attrs={'type': 'date'}))
    date_before = django_filters.DateFilter(field_name='created', lookup_expr='lte', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = ['title', 'author', 'date_after', 'date_before']
