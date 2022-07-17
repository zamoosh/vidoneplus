import math

from .imports import *


def timing(request, user_id):
    context = {}
    print(user_id)
    now = datetime.datetime.now()
    future = now + datetime.timedelta(seconds=2)
    diff = math.floor(future.timestamp() - now.timestamp())
    context['diff'] = diff
    return render(request, f'{__name__.replace("views", "").replace(".", "/")}.html', context)
