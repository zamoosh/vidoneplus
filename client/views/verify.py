import time
from .imports import *
from library.smsir import Smsir
from random import randrange
from ..models import Status
import jdatetime


def verify(request):
    context = {}
    if 'user' in request.session:
        context = request.session['user']
        print(context)
        if request.method == 'POST':
            if request.POST.get("code", "") == str(request.session['key']):
                pattern = re.compile("^\+989?\d{9}$", re.IGNORECASE)
                if pattern.match(context['cellphone']) is None:
                    context['cellphone'] = "+989" + context['cellphone'][2:]
                if User.objects.filter(cellphone=context['cellphone']).exists():
                    user = User.objects.get(cellphone=context['cellphone'])
                    print(user)
                    if user is not None:
                        # the password verified for the user
                        if user.is_active:
                            login(request, user)
                            if len(request.GET.get("next", "/")) == 0:
                                return HttpResponseRedirect("/")
                            return HttpResponseRedirect(request.GET.get("next", "/"))
                    else:
                        # the authentication system was unable to verify the username and password
                        print("The username and password were incorrect.")
                else:
                    user = User.objects.create_user(
                        # context['email'],
                        cellphone=context['cellphone'],
                        username=context['cellphone']
                    )
                    if 'referall' in request.session:
                        if User.objects.filter(username_clear=request.session['referall']).exists():
                            user.extra['referall'] = request.session['referall']
                    user.save()
                    status = Status()
                    status.status = False
                    status.user = user
                    status.duration = 0
                    status.save()
                    del request.session['user']
                    # try:
                    #     sms = Smsir()
                    #     code = randrange(1000, 9999, 1)
                    #     sms.sendwithtemplate({'verificationCode': code}, context['cellphone'], 55907)
                    # except:
                    #     pass
                    context['register'] = 1
                    user = User.objects.get(cellphone=context['cellphone'])
                    print(user)
                    if user is not None:
                        # the password verified for the user
                        if user.is_active:
                            login(request, user)
                            if len(request.GET.get("next", "/")) == 0:
                                return HttpResponseRedirect("/")
                            return HttpResponseRedirect("/accounts/profile/edit")
            else:
                context['error'] = 1
        else:
            import random
            try:
                sms = Smsir()
                key = str(random.randrange(10000, 99999))
                request.session['key'] = key
                sms.sendwithtemplate({'verificationCode': key}, context['cellphone'], 55907)
                return render(request, "client/verify.html", context)
            except:
                context['sms'] = False
                time.sleep(5)
                return HttpResponseRedirect("/accounts/login")
        return render(request, "client/verify.html", context)
    else:
        return HttpResponseRedirect("/accounts")
