from django import template
import os
from django.conf import settings

register = template.Library()

@register.filter(name='coursebuyed')
def coursebuyed(value, value2):
    return value.buyed(value2)

def free(value):
    if value == 0:
        return 'رایگان'
    else:
        value = f"{value:,}"
        return value + 'تومان '
register.filter('free', free)

