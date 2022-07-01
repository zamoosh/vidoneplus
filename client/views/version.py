from .imports import *


@login_required
def version(request):
    context = {}
    context['images'] = Imagetag.objects.filter(id__in=Setting.objects.filter(owner=request.user).values_list('image_tag_id', flat=True))
    return render(request, f'{__name__.replace("views.", "").replace(".", "/")}.html', context)
