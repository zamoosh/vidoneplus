from .imports import *


@login_required
def versions(request):
    context = {}
    context['images'] = Imagetag.objects.filter(status=True)
    return render(request, f'{__name__.replace("views.", "").replace(".", "/")}.html', context)
