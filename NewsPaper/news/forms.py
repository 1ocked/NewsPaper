from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class NewsSearchForm(forms.Form):
    title = forms.CharField(required=False, label='Название', max_length=100)
    author = forms.CharField(required=False, label='Автор', max_length=100)
    date_after = forms.DateField(required=False, label='Дата после', widget=forms.SelectDateWidget)

    class Meta:
        model = Post
        fields = ['title', 'text', 'cats', 'post_type']  # изменил 'category' на 'cats'

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        # Проверка, чтобы заголовок не совпадал с текстом
        if title and text:
            if title.lower() in text.lower():
                raise ValidationError(
                    "Заголовок не должен быть частью текста статьи."
                )

        return cleaned_data


# class PostForm(forms.ModelForm):
#     title = forms.CharField(min_length=5, label='Заголовок')
#     text = forms.CharField(min_length=20, widget=forms.Textarea, label='Текст статьи')
#     category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False, label='Категории')
#
#     class Meta:
#         model = Post
#         fields = ['title', 'text', 'category', 'post_type']
#
#     def clean(self):
#         cleaned_data = super().clean()
#         title = cleaned_data.get("title")
#         text = cleaned_data.get("text")
#
#         # Проверка, чтобы заголовок не совпадал с текстом
#         if title and text:
#             if title.lower() in text.lower():
#                 raise ValidationError(
#                     "Заголовок не должен быть частью текста статьи."
#                 )
#
#         return cleaned_data


