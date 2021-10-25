from .imports import *
from ..models import Status


def status(request):
    context = {}
    try:
        userstatus = Status.objects.get(user=request.user)
        if userstatus.status:
            context['msg'] = 'اکانت شما فعال است '
        else:
            context['msg'] = 'اکانت شما غیر فعال است '
    except:
        context['msg'] = 'اکانت شما هنوز تایید نشده است '
    return render(request, 'client/status.html', context)
