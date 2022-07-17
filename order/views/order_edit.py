from .imports import *


@login_required
def order_edit(request, order_id):
    context = {}
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        order.title = request.POST.get('title')
        order.description = request.POST.get('description')
        order.price = request.POST.get('price')
        order.period = request.POST.get('period')
        order.save()
        request.session['update'] = True
        return redirect(reverse('order:order_edit', kwargs={'order_id': order_id}))
    context['order'] = order
    if request.session.get('save'):
        context['save'] = True
        del request.session['save']
    if request.session.get('update'):
        context['update'] = True
        del request.session['update']
    return render(request, f'{__name__.replace(".", "/")}.html', context)
