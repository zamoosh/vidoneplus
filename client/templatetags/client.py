from django import template
import os
from django.conf import settings

register = template.Library()


@register.simple_tag
def version(debug=None):
    """Removes all values of arg from the given string"""
    if settings.DEBUG == False and debug:
        return "-" + os.environ.get("VERSION")
    elif settings.DEBUG == True and debug:
        return ''
    if os.environ.get("VERSION"):
        return os.environ.get("VERSION")
    else:
        return 'local'


def count(value):
    try:
        value = int(value)
    except:
        value = 0

    if value <= 5000:
        return value
    value = str(value)
    if len(value) < 7:
        return value[:-3] + "K"
    else:
        return value[:-6] + "M"


def toman(value, arg=None):
    try:
        value = int(value)
    except:
        return 'توافقی'
    value = f"{value:,}"
    if arg:
        return value + ' ' + arg
    else:
        return value + 'تومان '


@register.simple_tag
def listChecked(value):
    if type(value) == list:
        return True
    else:
        return False


@register.simple_tag
def listCheckedCount(value):
    if type(value) == list:
        return len(value)
    return 1


@register.filter(name='coursebuyed')
def coursebuyed(value, value2):
    return value.buyed(value2)


register.filter('count', count)
register.filter('toman', toman)
