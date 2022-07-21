from .imports import *


def verify(request, user_cellphone):
    context = {}
    if request.GET.get('recode'):  # if user request for new login code
        context['user_cellphone'] = user_cellphone
        if request.session.get('sent_sms'):
            del request.session['sent_sms']
        return redirect(reverse('client:verify', kwargs={'user_cellphone': user_cellphone}))
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
        if request.user.is_authenticated:
            return redirect(reverse('index'))
        if request.method == 'POST':
            if request.POST.get("code", "") == u.get_verificationcode():
                u = User.get_user(user_cellphone)
                if u.is_active:
                    login(request, u)
                    if request.session.get('sent_sms'):
                        del request.session['sent_sms']
                    return redirect(reverse('index'))
        context['user_cellphone'] = user_cellphone
        return render(request, f'{__name__.replace("views.", "").replace(".", "/")}.html', context)
    return redirect(reverse('index'))
