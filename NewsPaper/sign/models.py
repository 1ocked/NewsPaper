# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from django import forms
#
#
# class BaseRegisterForm(UserCreationForm):
#     email = forms.EmailField(label = "Email")
#     first_name = forms.CharField(label = "Имя")
#     last_name = forms.CharField(label = "Фамилия")
#
#     class Meta:
#         model = User
#         fields = ("username",
#                   "first_name",
#                   "last_name",
#                   "email",
#                   "password1",
#                   "password2", )

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class CommonSignupForm(SignupForm):  #http://127.0.0.1:8000/accounts/login/?next=/ путь для регистрации с авто добавлением в группу "common"

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        basic_group = Group.objects.get(name='Common')
        basic_group.user_set.add(user)
        return user


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )