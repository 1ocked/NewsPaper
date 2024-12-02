from django import forms

from .models import Post


#from models import Post

class NewsSearchForm(forms.Form):
    title = forms.CharField(required=False, label='Название', max_length=100)
    author = forms.CharField(required=False, label='Автор', max_length=100)
    date_after = forms.DateField(required=False, label='Дата после', widget=forms.SelectDateWidget)

# from django import forms
# from .models import *
#
# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['title', 'author', 'published_date']
#         widgets = {
#             'published_date': forms.DateInput(attrs={'type': 'date'}),
#         }
