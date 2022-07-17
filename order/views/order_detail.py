from .imports import *


@login_required
def order_detail(request, order_id):
    context = {}
    print(order_id)
    context['order'] = Order.objects.get(id=order_id)
    return render(request, f'{__name__.replace(".", "/")}.html', context)
