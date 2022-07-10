from .imports import *


@login_required
@can_see_this_page
def sites(request):
    context = {}
    paginator = Paginator(Setting.objects.all(), 5)
    if request.GET.get('page_number'):
        context['page'] = paginator.get_page(request.GET.get('page_number'))
    else:
        context['page'] = paginator.get_page(1)
    context['page_url'] = 'client:sites'
    return render(request, f'{__name__.replace("views.", "").replace(".", "/")}.html', context)
