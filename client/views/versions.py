from .imports import *


@login_required
def versions(request):
    context = {}
    paginator = Paginator(Imagetag.objects.filter(status=True), 10)
    context['page'] = paginator.get_page(1)
    if request.GET.get('page_number'):
        context['page'] = paginator.get_page(request.GET.get('page_number'))
    context['page_url'] = 'client:versions'
    return render(request, f'{__name__.replace("views.", "").replace(".", "/")}.html', context)
