from django.contrib import messages
from django.urls import reverse

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
            user = User.objects.get(id=request.user.id)
            user.first_name = context['req']['first_name']
            user.last_name = context['req']['last_name']
            user.email = context['req']['email']
            user.description = context['req']['description']
            user.organization_name = context['req']['organization_name']
            user.educational_interface_name = context['req']['educational_interface_name']
            if request.POST.get('dateofestablishment') :
                user.dateofestablishment = jdatetime.datetime.strptime(request.POST.get('dateofestablishment'),"%Y/%m/%d").togregorian()
            user.save()
            messages.success(request, "Profile is Change!")
            return HttpResponseRedirect(reverse('client:profile'))
        return render(request, 'client/profile-edit.html', context)
    return render(request, 'client/profile.html', context)
