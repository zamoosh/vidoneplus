from .imports import *


@login_required
@allowed_users(allowed_roles=['admin'])
def users(request):
    context = {}
    non_staff_users = User.objects.filter(is_staff=False)
    context['users'] = non_staff_users
    context['status'] = Status.objects.filter(user__in=non_staff_users)
    return render(request, f'{__name__.replace("views.", "").replace(".", "/")}.html', context)
