from .imports import *
import jdatetime

def Login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    context = {}
    context['error'] = 0
    if request.method == 'POST':
        context['request'] = {}
        context['request']['cellphone'] = request.POST.get('cellphone', '').strip()
        pattern = re.compile("^09?\d{9}$", re.IGNORECASE)
        if pattern.match(context['request']['cellphone']):
            context['request']['cellphone'] = "+989" + context['request']['cellphone'][2:]
            request.session['user'] = context['request']
            return HttpResponseRedirect("/accounts/verify")
    return render(request, "client/login.html", context)