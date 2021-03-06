from django import template
from client.models import Setting as Usetting
from client.models import Status as Usstatus
from course.models import CourseUser

register = template.Library()


@register.filter(name='coursebuyed')
def coursebuyed(value, value2):
    return CourseUser.objects.filter(course=value, owner=value2)


def free(value):
    if value == 0:
        return 'رایگان'
    else:
        value = f"{value:,}"
        return value + 'تومان '


register.filter('free', free)
