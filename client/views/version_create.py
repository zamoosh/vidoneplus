from .imports import *


def version_create(request):
    if request.user.is_superuser:
        pass
    context = {}
    if request.method == "POST":
        image_tag = Imagetag()
        image_tag.pwa_version = request.POST.get('pwa_version')
        image_tag.pwa_description = request.POST.get('pwa_description')
        image_tag.admin_version = request.POST.get('admin_version')
        image_tag.admin_description = request.POST.get('admin_description')
        image_tag.site_version = request.POST.get('site_version')
        image_tag.site_description = request.POST.get('site_description')
        image_tag.android_version = request.POST.get('android_version')
        image_tag.android_description = request.POST.get('android_description')
        image_tag.ios_version = request.POST.get('ios_version')
        image_tag.ios_description = request.POST.get('ios_description')
        if request.POST.get('force_update'):
            image_tag.forceupdate = True
        image_tag.save()
    return render(request, f'{__name__.replace("views.", ".").replace(".", "/")}.html', context)
