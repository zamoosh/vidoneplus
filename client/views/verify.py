from .imports import *


def verify(request, user_cellphone):
    context = {}
    if request.GET.get('recode'):
        context['user_cellphone'] = user_cellphone
        if request.session.get('sent_sms'):
            del request.session['sent_sms']
        return redirect(reverse('client:verify_get', kwargs={'user_cellphone': user_cellphone}))
    if user_cellphone:
        """check if request.user is exists in database or not"""
        u = User.get_user(user_cellphone)
        if not u.id:
            """creating new user"""
            u.cellphone = user_cellphone
            u.username = user_cellphone
            u.save()
            Status.objects.create(user=u, duration=0).save()
        if not request.session.get('sent_sms'):
            u.sendsms()
            request.session['sent_sms'] = True
        if request.method == 'POST':
            u.get_verificationcode()
            if request.POST.get("code", "") == str(request.session['key']):
                u = User.get_user(user_cellphone)
                if not u.id:
                    return redirect(reverse('client:login'))
                if u.is_active:
                    login(request, u)
                    return redirect(reverse('index'))
        context['user_cellphone'] = user_cellphone
        return render(request, f"{app_name.name}/{__name__.split('.')[-1]}.html", context)
    return redirect(reverse('index'))
