from .imports import *


def user_orders(request):
    context = {}
    return render(request, f'{__name__.replace(".", "/")}.html', context)
