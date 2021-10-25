from .imports import *
from ..models import *


@login_required
def admin(request):
    context = {}
    context['users'] = User.objects.filter(is_staff=False)
    context['domain'] = Setting.objects.filter(user__in=context['users'])
    context['status'] = Status.objects.filter(user__in=context['users'])
    return render(request, "client/admin.html", context)
