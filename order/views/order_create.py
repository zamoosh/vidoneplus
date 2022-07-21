from .imports import *


@login_required
@is_superuser
def order_create(request):
    context = {}
    if request.method == 'POST':
        order = Order()
        order.title = request.POST.get('title')
        order.description = request.POST.get('description')
        order.price = request.POST.get('price')
        if not request.POST.get('period').isnumeric():
            return redirect(reverse('order:order_create'))
        order.period = int(request.POST.get('period'))
        if request.FILES.get('image'):
            order.image = request.FILES.get('image')
        order.save()
        request.session['save'] = True
        return redirect(reverse('order:order_edit', kwargs={'order_id': order.id}))
    return render(request, f'{__name__.replace(".", "/")}.html', context)
