from .imports import *


@login_required
@allowed_users(allowed_roles=['admin'])
def deactivate_user(request, user_id):
    context = {}
    context['users'] = User.objects.filter(is_staff=False)
    context['status'] = Status.objects.filter(user__in=User.objects.filter(is_staff=False))
    context['user'] = User.objects.get(id=user_id)
    status = Status.objects.get(user=context['user'])
    status.active_user = 0
    status.save()
    context['msg'] = "کاربر  %s غیرفعال شد" % (context['user'].first_name + " " + context['user'].last_name)
    return render(request, 'client/activeuser.html', context)
