from django.contrib.auth.models import User
from library.smsir import Smsir
from .imports import *
from ..models import *
from client.decorators import allowed_users


@login_required
@allowed_users(allowed_roles=['admin'])
def users(request):
    non_staff_users = User.objects.filter(is_staff=False)
    context = {'users': non_staff_users,
               'status': Status.objects.filter(user__in=non_staff_users)}
    # return render(request, f'{__name__.replace("views.", "").replace(".", "/")}.html', context)
    return render(request, 'client/users.html', context)


@login_required
@allowed_users(allowed_roles=['admin'])
def activate_user(request, user_id):
    context = {}
    non_staff_users = User.objects.filter(is_staff=False)
    context['users'] = non_staff_users
    context['status'] = Status.objects.filter(user__in=non_staff_users)
    context['user'] = User.objects.get(id=user_id)
    context['cellphone'] = User.objects.get(id=user_id).cellphone
    status = Status.objects.get(user=context['user'])
    status.active_user = True
    status.save()
    sms = Smsir()
    sms.sendsms('اکانت شما در ویدان فعال شد.', context['cellphone'])
    context['msg'] = "کاربر  %s تایید شد" % (context['user'].first_name + " " + context['user'].last_name)
    return render(request, f"{app_name.name}/{__name__.split('.')[-1]}.html", context)
