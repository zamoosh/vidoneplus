from .imports import *


@login_required
def orders(request):
    context = {}
    paginator = Paginator(Order.objects.filter(status=True), 2)
    context['page'] = paginator.get_page(1)
    if request.GET.get('page_number'):
        context['page'] = paginator.get_page(request.GET.get('page_number'))
    context['page_url'] = 'order:orders'
    now = datetime.datetime.now()
    future = now + datetime.timedelta(seconds=10)
    diff = math.floor(future.timestamp() - now.timestamp())
    context['diff'] = diff
    return render(request, f'{__name__.replace(".", "/")}.html', context)
