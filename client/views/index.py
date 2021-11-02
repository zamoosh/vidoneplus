from .imports import *
from ..models import Setting as Usetting, Status


@login_required
def index(request):
    # from domainholder.models import Domainns
    context = {}
    context['settings'] = Usetting.objects.get(user=request.user).domain
    context['status'] = Status.objects.get(user=request.user).status
    if not context['settings']:
        context['msg'] = "شما هنوز دامنه ای ثبت نکرده اید"
    if not context['status']:
        context['msg'] = "حساب کاربری شما فعال نشده است"
    return render(request, 'client/index.html', context)
