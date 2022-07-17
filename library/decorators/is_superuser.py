from .imports import *


def is_superuser(function):
    def wrapper(request, **kwargs):
        if request.user.is_superuser:
            return function(request, **kwargs)
        return redirect(reverse('page_not_found'))

    return wrapper
