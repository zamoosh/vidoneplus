from .imports import *


@login_required
@id_is_real(Order)
def order_buy(request, order_id, setting_id=None):
    context = {}
    user = User.objects.get(id=request.user.id)
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        user_setting = Setting.objects.get(id=setting_id)
        if user_setting.orderitem_set.exists():
            order_item = user.orderitem_set.last()
            now = datetime.datetime.now()
            if now.timestamp() > order_item.ended_at.timestamp() and (not order_item.status):  # limited order
                OrderItem.objects.create(
                    order=order,
                    owner=user,
                    setting=user_setting
                ).save()
            else:
                request.session['active_order'] = True
                return redirect(reverse('order:orders'))
        else:
            OrderItem.objects.create(
                order=order,
                owner=user,
                setting=user_setting
            ).save()
        return redirect(reverse('client:profile'))
    context['order'] = order
    return render(request, f'{__name__.replace(".", "/")}.html', context)
