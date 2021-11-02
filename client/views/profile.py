from .imports import *
import jdatetime

def profile(request, action=None):
    context = {}
    context['user'] = User.objects.filter(id=request.user.id)
    if action == "edit":
        if request.method == "POST":
            context['req'] = {}
            context['req']['first_name'] = request.POST.get('firstname', '').strip()
            context['req']['last_name'] = request.POST.get('lastname', '').strip()
            context['req']['email'] = request.POST.get('email', '').strip()
            context['req']['organization_name'] = request.POST.get('organization_name', None)
            context['req']['educational_interface_name'] = request.POST.get('educational_interface_name').strip()
            context['req']['description'] = request.POST.get('description').strip()
            context['req']['dateofestablishment'] = request.POST.get('dateofestablishment').strip()
            user = User.objects.get(id=request.user.id)
            user.first_name = context['req']['first_name']
            user.last_name = context['req']['last_name']
            user.email = context['req']['email']
            user.description = context['req']['description']
            user.organization_name = context['req']['organization_name']
            user.educational_interface_name = context['req']['educational_interface_name']
            if 'dateofestablishment' in request.POST:
                user.dateofestablishment = jdatetime.datetime.strptime(context['req']['dateofestablishment'],"%Y/%m/%d").togregorian()
            user.save()
        return render(request, 'client/profile-edit.html', context)
    return render(request, 'client/profile.html', context)
