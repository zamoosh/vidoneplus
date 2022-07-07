from .imports import *


@login_required
@allowed_users(allowed_roles=['admin'])
def sites(request):
    context = {}
    context['sites'] = Setting.objects.all()
    return render(request, f'{__name__.replace("views.", "").replace(".", "/")}.html', context)
