from .imports import *


def version_edit(request, image_tag_id):
    if not request.user.is_superuser:
        return redirect(reverse('page_not_found'))
    context = {}
    if not Imagetag.objects.filter(id=image_tag_id).exists():
        return redirect(reverse('page_not_found'))
    image_tag = Imagetag.objects.get(id=image_tag_id)
    context['image_tag'] = image_tag
    if request.method == "POST":
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
        else:
            image_tag.forceupdate = False
        image_tag.save()
        request.session['save'] = True
        return redirect(reverse('client:version_edit', kwargs={'image_tag_id': image_tag_id}))
    if request.session.get('save'):
        context['save'] = True
        del request.session['save']
    return render(request, f'{__name__.replace("views.", "").replace(".", "/")}.html', context)
