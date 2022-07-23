from .imports import *


@login_required
@id_is_real(Order)
def order_buy(request, order_id, setting_id=None):
    context = {}
    user = User.objects.get(id=request.user.id)
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        user_setting = Setting.objects.get(id=setting_id)
        if user_setting.orderitem_set.exists():  # if user's site has order
            order_item = user.setting_set.get(id=setting_id).orderitem_set.last()
            now = datetime.datetime.now()
            if now.timestamp() > order_item.ended_at.timestamp() and (not order_item.status):  # if user's site time end
                order = OrderItem.objects.create(
                    order=order,
                    setting=user_setting
                )
                order.save()
                Bill.objects.create(order_item=order).save()
            else:
                request.session['active_order'] = True
                return redirect(reverse('order:order_buy', kwargs={'order_id': order_id, 'setting_id': setting_id}))
        else:
            order = OrderItem.objects.create(
                order=order,
                setting=user_setting
            )
            order.save()
            Bill.objects.create(order_item=order).save()
        return redirect(reverse('client:profile'))
    context['order'] = order
    if request.session.get('active_order'):
        context['active_order'] = True
        del request.session['active_order']
    return render(request, f'{__name__.replace(".", "/")}.html', context)
