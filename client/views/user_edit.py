from .imports import *


@login_required
@can_see_this_page
def user_edit(request, user_id):
    context = {}
    if not User.objects.filter(id=user_id).exists():
        return redirect(reverse('page_not_found'))
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
            status = Status.objects.get(user=u)
            if request.POST.get('status') == 'True':
                status.active_user = True
            elif request.POST.get('status') == 'False':
                status.active_user = False
            status.save()
            u.save()
            request.session['save'] = True
        return redirect(reverse('client:user_edit', kwargs={'user_id': user_id}))
    context['user'] = User.objects.get(id=user_id)
    if request.session.get('save'):
        context['save'] = True
        del request.session['save']
    return render(request, f'{__name__.replace("views.", "").replace(".", "/")}.html', context)
