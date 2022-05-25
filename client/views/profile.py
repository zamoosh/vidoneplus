from .imports import *


@login_required
def profile(request):
    context = {}
    context['user'] = User.objects.get(id=request.user.id)
    return render(request, f"{app_name.name}/{__name__.split('.')[-1]}.html", context)
