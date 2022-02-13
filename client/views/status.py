from .imports import *
from ..models import Status

@login_required
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
    return render(request, f"{app_name.name}/{__name__.split('.')[-1]}.html", context)
