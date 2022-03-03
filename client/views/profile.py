from django.contrib import messages
from django.urls import reverse

from .imports import *
import jdatetime

@login_required
def profile(request, action=None):
    context = {}
    context['user'] = User.objects.filter(id=request.user.id)
    if action == "edit":
        if request.method == "POST":
            context['req'] = {}
            for key, value in request.POST.items():
                if key == 'csrfmiddlewaretoken' or key == 'dateofestablishment':
                    continue
                context['req'][key] = value
            user = User.objects.get(id=request.user.id)
            user.first_name, user.last_name, user.organization_name, user.educational_interface_name, user.description,\
                user.email = context['req'].values()
            if request.POST.get('dateofestablishment') :
                user.dateofestablishment = jdatetime.datetime.strptime(request.POST.get('dateofestablishment'),"%Y/%m/%d").togregorian()
            user.save()
            messages.success(request, "Profile is Change!")
            return HttpResponseRedirect(reverse('client:profile'))
        return render(request, f"{app_name.name}/{__name__.split('.')[-1]}.html", context)
    return render(request, f"{app_name.name}/{__name__.split('.')[-1]}.html", context)
