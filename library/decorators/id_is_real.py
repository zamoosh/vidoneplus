from .imports import *


def id_is_real(model):
    def decorator(function):
        def wrapper(request, **kwargs):
            for key, value in request.resolver_match.kwargs.items():
                if model.__name__.lower() in key:
                    if model.objects.filter(id=value).exists():
                        return function(request, **kwargs)
            p = request.path.split('/')
            p = p[1]
            return redirect(reverse(
                'page_not_found',
                kwargs={'text': 'آی‌دی مورد‌نظر وجود ندارد!', 'previous_url': p}
            ))

        return wrapper

    return decorator
