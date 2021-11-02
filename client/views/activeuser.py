import os
from django.contrib.auth.models import User
from library.cpanel import Cpanel
from library.helm import Helm
from library.kubectl import Kubectl
from .imports import *
from ..models import Setting as usetting
from ..models import *
import uuid


@login_required
def users(request):
    context = {}
    context['users'] = User.objects.filter(is_staff=False)
    context['status'] = Status.objects.filter(user__in=context['users'])
    return render(request, "client/activeuser.html", context)

def activeuser(request, id):
    context = {}
    context['users'] = User.objects.filter(is_staff=False)
    context['status'] = Status.objects.filter(user__in=context['users'])
    context['user'] = User.objects.get(id=id)
    status = Status.objects.get(user=context['user'])
    status.status = 1
    status.save()
    context['msg'] = "کاربر  %s تایید شد" % (context['user'].first_name + context['user'].last_name)
    return render(request, "client/activeuser.html", context)

def deactiveuser(request, id):
    context = {}
    context['users'] = User.objects.filter(is_staff=False)
    context['status'] = Status.objects.filter(user__in=context['users'])
    context['user'] = User.objects.get(id=id)
    status = Status.objects.get(user=context['user'])
    status.status = 0
    status.save()
    context['msg'] = "کاربر  %s غیرفعال شد" % (context['user'].first_name + " " + context['user'].last_name)
    return render(request, "client/activeuser.html", context)