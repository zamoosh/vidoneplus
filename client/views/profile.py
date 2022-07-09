from .imports import *


@login_required
def profile(request):
    context = {}
    context['user'] = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        if not User.objects.filter(id=request.user.id).exists():
            return HttpResponse('کاربر وجود ندارد')
        if not (request.user.is_superuser or request.user.id == request.user.id):
            return HttpResponse('کاربر وجود ندارد')
        if User.not_empty(request, request.method, 'first_name', 'last_name', 'email'):
            u: User = User.objects.get(id=request.user.id)
            u.first_name = request.POST.get('first_name')
            u.last_name = request.POST.get('last_name')
            u.organization_name = request.POST.get('organization_name')
            u.educational_interface_name = request.POST.get('educational_interface_name')
            u.description = request.POST.get('description')
            if request.POST.get('dateofestablishment'):
                u.dateofestablishment = User.str_to_date(request.POST.get('dateofestablishment'))
            u.email = request.POST.get('email')
            u.save()
            request.session['save'] = True
            return redirect(reverse('client:profile'))
        request.session['not_null'] = True
        return redirect(reverse('client:profile'))
    if request.session.get('save'):
        context['save'] = True
        del request.session['save']
    if request.session.get('not_null'):
        context['not_null'] = True
        del request.session['not_null']
    return render(request, f'{__name__.replace("views.", "").replace(".", "/")}.html', context)
