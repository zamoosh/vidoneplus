from .imports import *


def _configpodname(tld):
    return tld + "-site", tld + "-app", tld + "-pwa"


@login_required
def edit_verion(request, id, action=None):
    context = {}
    context['version'] = Imagetag.objects.get(id=id)
    if action == "active":
        imagetag = Imagetag.objects.get(id=id)
        imagetag.status = True
        return render(request, "client/view_version.html")

    if action == "deactive":
        imagetag = Imagetag.objects.get(id=id)
        imagetag.status = False
        return render(request, "client/view_version.html")

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


# @login_required
# def create_verion(request):
#     context = {}
#     if request.method == "POST":
#         context['req'] = {}
#         for key, value in request.POST.items():
#             if key == 'force_update' or key == 'csrfmiddlewaretoken':
#                 continue
#             context['req'][key] = value
#         context['req']['force_update'] = request.POST.get('force_update', '').strip()
#         imagetag = Imagetag()
#         imagetag.pwa_version, imagetag.pwa_description, imagetag.admin_version, imagetag.admin_description, \
#         imagetag.site_version, imagetag.site_description, imagetag.android_version, imagetag.android_description, \
#         imagetag.ios_version, imagetag.ios_description, _ = context['req'].values()
#         if 'force' in context['req']['force_update']:
#             imagetag.forceupdate = True
#         imagetag.save()
#     return render(request, "client/create_version.html", context)
