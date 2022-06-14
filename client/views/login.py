from .imports import *


def login(request):
    context = {}
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    context['error'] = 0
    if request.method == 'POST':
        context['request'] = {}
        context['request']['cellphone'] = request.POST.get('cellphone', '').strip()
        pattern = re.compile("^09?\d{9}$", re.IGNORECASE)
        if pattern.match(context['request']['cellphone']):
            context['request']['cellphone'] = "+989" + context['request']['cellphone'][2:]
            cellphone = context['request']['cellphone']
            return redirect(reverse('client:verify', kwargs={'user_cellphone': cellphone}))
    return render(request, f'{__name__.replace("views.", "").replace(".", "/")}.html', context)
