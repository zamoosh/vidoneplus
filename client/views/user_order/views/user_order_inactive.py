from .imports import *


def user_order_inactive(request):
    context = {}
    user = User.objects.get(id=request.user.id)
    inactive_orders = Paginator(OrderItem.objects.filter(id__in=user.setting_set.all().values_list('orderitem__id', flat=True), status=False), 1)
    context['page'] = inactive_orders.get_page(1)
    if request.GET.get('page_number'):
        context['page'] = inactive_orders.get_page(request.GET.get('page_number'))
    context['page_url'] = 'client:user_order:user_order_inactive'
    return render(request, f'{__name__.replace(".", "/")}.html', context)
