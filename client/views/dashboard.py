from .imports import *
from ..models import Setting as Usetting, Status


@login_required
def dashboard(request):
    context = {}
    try:
        context['settings'] = Usetting.objects.get(owner=request.user).domain
        context['status'] = Status.objects.get(user=request.user).site_created
        if not context['settings']:
            context['msg'] = "شما هنوز دامنه ای ثبت نکرده اید"
        if not context['status']:
            context['site'] = False
    except (Exception, Exception):
        pass
    return render(request, f'{__name__.replace("views.", "").replace(".", "/")}.html', context)

