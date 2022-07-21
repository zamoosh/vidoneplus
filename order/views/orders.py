from .imports import *


@login_required
def orders(request):
    context = {}
    paginator = Paginator(Order.objects.filter(status=True), 12)
    context['page'] = paginator.get_page(12)
    if request.GET.get('page_number'):
        context['page'] = paginator.get_page(request.GET.get('page_number'))
    context['page_url'] = 'order:orders'
    now = datetime.datetime.now()
    future = now + datetime.timedelta(seconds=10)
    diff = math.floor(future.timestamp() - now.timestamp())
    context['diff'] = diff
    if request.session.get('active_order'):
        context['active_order'] = True
        del request.session['active_order']
    return render(request, f'{__name__.replace(".", "/")}.html', context)
