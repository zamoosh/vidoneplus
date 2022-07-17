from .imports import *


@login_required
@is_superuser
def order_delete(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = False
    order.save()
    return redirect(reverse('order:orders'))
