from django import template
from client.models import Setting as Usetting
from client.models import Status as Usstatus
register = template.Library()

@register.filter(name='status')
def status(value):
    try:
        return Usstatus.objects.get(user=value).site_created
    except:
        return None

@register.filter(name='domain')
def domain(value):
    try:
        return Usetting.objects.get(user=value).domain
    except:
        return "بدون دامنه"

@register.filter(name='contact_phone')
def contact_phone(value):
    try:
        return Usetting.objects.get(user=value).contact_phone
    except:
        return "بدون شماره"


@register.filter(name='persian_numbers')
def persian_numbers(english_int):
    devanagari_nums = ('۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹')
    number = str(english_int)
    return ''.join(devanagari_nums[int(digit)] for digit in number)
