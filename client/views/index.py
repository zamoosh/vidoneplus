from .imports import *
from ..models import Setting as Usetting, Status


@login_required
def index(request):
    context = {}
    try:
        context['settings'] = Usetting.objects.get(user=request.user).domain
        context['status'] = Status.objects.get(user=request.user).site_created
        if not context['settings']:
            context['msg'] = "شما هنوز دامنه ای ثبت نکرده اید"
        if not context['status']:
            context['site'] = False
    except:
        pass
    return render(request, 'client/index.html', context)

