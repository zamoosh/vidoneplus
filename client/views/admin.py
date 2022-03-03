from .imports import *


@login_required
@allowed_users(allowed_roles=['admin'])
def admin(request):
    context = {'settings': Setting.objects.all()}
    return render(request, f"{app_name.name}/{__name__.split('.')[-1]}.html", context)
