from .imports import *


def version_edit(request):
    if request.user.is_superuser:
        pass
    context = {}
    if request.method == "POST":
        context['req'] = {}
        for key, value in request.POST.items():
            if key == 'force_update' or key == 'csrfmiddlewaretoken':
                continue
            context['req'][key] = value
        context['req']['force_update'] = request.POST.get('force_update', '').strip()
        imagetag = Imagetag.objects.get(id=id)
        imagetag.pwa_version, imagetag.pwa_description, imagetag.admin_version, imagetag.admin_description, \
        imagetag.site_version, imagetag.site_description, imagetag.android_version, imagetag.android_description, \
        imagetag.ios_version, imagetag.ios_description, _ = context['req'].values()
        if 'force' in context['req']['force_update']:
            imagetag.forceupdate = True
        else:
            imagetag.forceupdate = False
        imagetag.save()
    return render(request, "client/create_version.html", context)
