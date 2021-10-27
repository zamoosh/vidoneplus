from django import template
from client.models import Setting as Usetting
from client.models import Status as Usstatus
register = template.Library()

@register.filter(name='coursebuyed')
def coursebuyed(value, value2):
    return value.buyed(value2)

@register.filter(name='status')
def status(value):
    try:
        return Usstatus.objects.get(user=value).status
    except:
        return None

@register.filter(name='domain')
def domain(value):
    try:
        return Usetting.objects.get(user=value).domain
    except:
        return "بدون دامنه"

def free(value):
    if value == 0:
        return 'رایگان'
    else:
        value = f"{value:,}"
        return value + 'تومان '
register.filter('free', free)

