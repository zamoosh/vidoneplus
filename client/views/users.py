from .imports import *


@login_required
@can_see_this_page
def users(request):
    context = {}
    paginator = Paginator(User.objects.filter(is_staff=False), 1)
    if request.GET.get('page_number'):
        context['page'] = paginator.get_page(request.GET.get('page_number'))
    else:
        context['page'] = paginator.get_page(1)
    context['page_url'] = 'client:users'
    return render(request, f'{__name__.replace("views.", "").replace(".", "/")}.html', context)
