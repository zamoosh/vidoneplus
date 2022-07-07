from .imports import *


@login_required
def version_delete(request, image_tag_id):
    if not request.user.is_superuser:
        return redirect(reverse('page_not_found'))
    if not Imagetag.objects.filter(id=image_tag_id).exists():
        return redirect(reverse('page_not_found'))
    image_tag = Imagetag.objects.get(id=image_tag_id)
    image_tag.status = False
    image_tag.save()
    return redirect(reverse('client:versions'))
