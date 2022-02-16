import os
from django.contrib.auth.models import User
from library.cpanel import Cpanel
from library.helm import Helm
from library.kubectl import Kubectl
from library.smsir import Smsir
from .imports import *
from ..models import Setting as usetting
from ..models import *
from django.contrib.sessions.models import Session
import uuid


@login_required
def users(request):
    context = {}
    context['users'] = User.objects.filter(is_staff=False)
    context['status'] = Status.objects.filter(user__in=context['users'])
    return render(request, "client/activeuser.html", context)

@login_required
def activeuser(request, id):
    context = {}
    context['users'] = User.objects.filter(is_staff=False)
    context['status'] = Status.objects.filter(user__in=context['users'])
    context['user'] = User.objects.get(id=id)
    context['cellphone'] = User.objects.get(id=id).cellphone
    print(context['cellphone'])
    status = Status.objects.get(user=context['user'])
    status.active_user = 1
    status.save()
    sms = Smsir()
    sms.sendsms('اکانت شما در ویدان فعال شد.', context['cellphone'])
    context['msg'] = "کاربر  %s تایید شد" % (context['user'].first_name + " " + context['user'].last_name)
    return render(request, "client/activeuser.html", context)

@login_required
def deactiveuser(request, id):
    context = {}
    context['users'] = User.objects.filter(is_staff=False)
    context['status'] = Status.objects.filter(user__in=context['users'])
    context['user'] = User.objects.get(id=id)
    status = Status.objects.get(user=context['user'])
    status.active_user = 0
    status.save()
    session_profiles = Session.objects.filter(user__username__exact='johndoe')
    [sp.session.delete() for sp in session_profiles if sp.get_decoded().get('_auth_user_id') == id]
    context['msg'] = "کاربر  %s غیرفعال شد" % (context['user'].first_name + " " + context['user'].last_name)
    return render(request, "client/activeuser.html", context)