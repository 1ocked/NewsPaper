"""
Django settings for NewsPaper project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path

from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)zd_-54v(a#%iu@=td)+n0jo(3afk4%^s@g$&_ehk9q2a0@1z-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
# подключаем ещё приложения # Видны в панели admin
    'django.contrib.sites',
    'django.contrib.flatpages',
    'news',
    'accounts',
    'django_filters',
#D8.4 ЕСть отдельный проект Djnaago autorization
    'sign',
    'protect',
#allauth приложения
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.yandex',
]


SITE_ID = 1   #!!!!!!!!!!!!! Без этого не запускается панель админа

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
# Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'NewsPaper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'NewsPaper.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# static папка (И в настройках добавить строчку в самом конце, для подгрузки стилей из папки static :)
#STATICFILES_DIRS = [ BASE_DIR / "static" ]

# Указываем страницу, на которую будет перенаправлен пользователь, если он не авторизован
LOGIN_URL = '/accounts/login/'  # Путь к странице входа, который у вас настроен (например, через allauth)
# Указываем путь, на который будет перенаправляться пользователь после успешного входа
#LOGIN_REDIRECT_URL = '/profile/'  # или другой путь, на который должен быть перенаправлен пользователь #!!!
LOGIN_REDIRECT_URL = reverse_lazy('home')  # Или ваш основной URL


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Для логина с использованием имени пользователя
    'allauth.account.auth_backends.AuthenticationBackend',  # Для использования методов аутентификации allauth
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
#Чтобы allauth распознал нашу форму как ту, что должна выполняться вместо формы
#по умолчанию, необходимо добавить строчку в файл настроек проекта settings.py:
ACCOUNT_FORMS = {'signup': 'sign.models.CommonSignupForm'}

#SMTP Yandex.ru Отправка сообзение на почту Модуль D9.3
# Email Configuration (for sending mail using Yandex SMTP server)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'  # Yandex SMTP server
EMAIL_PORT = 465  # SMTP port for Yandex
EMAIL_HOST_USER = 'ruslan7maslianov'  # Your Yandex email username
EMAIL_HOST_PASSWORD = 'tjggreqqdyqmhoev'  # Your Yandex email password
EMAIL_USE_SSL = True  # Yandex uses SSL, so set this to True

ADMINS = [
    ('habay', 'habay@mail.ru'),
    # список всех админов в формате ('имя', 'их почта')
]
SERVER_EMAIL = 'ruslan7maslianov@yandex.ru'  # это будет у нас вместо аргумента FROM в массовой рассылке

SOCIALACCOUNT_PROVIDERS = {
    'yandex': {
        'SCOPE': ['login:email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'OAUTH_PKCE_ENABLED': True,
    }
}