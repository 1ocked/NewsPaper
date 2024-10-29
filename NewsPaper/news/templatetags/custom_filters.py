from django import template
from better_profanity import profanity

register = template.Library()

@register.filter(name='censor')
def censor(value):
    if isinstance(value, str):  # Проверка на строку
        return profanity.censor(value, '$')
    return value  # Возвращаем значение без изменений, если это не строка