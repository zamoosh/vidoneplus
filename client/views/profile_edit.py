from .imports import *


@login_required
def profile_edit(request, user_id):
    context = {}
    if not User.objects.filter(id=user_id).exists():
        return HttpResponse('کاربر وجود ندارد')
    if not (request.user.is_superuser or request.user.id == user_id):
        return HttpResponse('کاربر وجود ندارد')
    if request.method == 'POST':
        if User.not_empty(request, request.method, 'first_name', 'last_name', 'email'):
            u: User = User.objects.get(id=user_id)
            u.first_name = request.POST.get('first_name')
            u.last_name = request.POST.get('last_name')
            u.organization_name = request.POST.get('organization_name')
            u.educational_interface_name = request.POST.get('educational_interface_name')
            u.description = request.POST.get('description')
            u.dateofestablishment = User.str_to_date(request.POST.get('dateofestablishment'))
            u.email = request.POST.get('email')
            u.save()
        return redirect(reverse('client:profile_edit', kwargs={'user_id': user_id}))
    context['user'] = User.objects.get(id=user_id)
    return render(request, f'{__name__.split(".")[0]}/{__name__.split(".")[-1]}.html', context)
