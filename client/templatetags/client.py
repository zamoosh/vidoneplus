from django import template
import os
from django.conf import settings
from client.models import Setting as Usetting
register = template.Library()

@register.filter(name='coursebuyed')
def coursebuyed(value, value2):
    return value.buyed(value2)

@register.filter(name='domain')
def domain(value):
    try:
        return Usetting.objects.get(user=value).domain
    except:
        return None

def free(value):
    if value == 0:
        return 'رایگان'
    else:
        value = f"{value:,}"
        return value + 'تومان '
register.filter('free', free)

