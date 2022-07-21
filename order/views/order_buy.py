from .imports import *


@login_required
def order_buy(request, order_id):
    context = {}
    user = User.objects.get(id=request.user.id)
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        if user.orderitem_set.exists():
            order_item = user.orderitem_set.last()
            if datetime.datetime.now().timestamp() > order_item.ended_at.timestamp():
                OrderItem.objects.create(
                    order=order,
                    owner=user,
                ).save()
            else:
                request.session['active_order'] = True
                return redirect(reverse('order:orders'))
        else:
            OrderItem.objects.create(
                order=order,
                owner=user,
            ).save()
        return redirect(reverse('client:profile'))
    context['order'] = order
    return render(request, f'{__name__.replace(".", "/")}.html', context)
