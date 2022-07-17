from .imports import *


@login_required
@is_superuser
def order_create(request):
    context = {}
    if request.method == 'POST':
        order = Order.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            period=request.POST.get('period')
        )
        order.save()
        request.session['save'] = True
        return redirect(reverse('order:order_edit', kwargs={'order_id': order.id}))
    return render(request, f'{__name__.replace(".", "/")}.html', context)
