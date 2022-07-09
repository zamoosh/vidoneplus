from django.http import HttpResponse
from django.shortcuts import redirect, reverse


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *arg, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles or request.user.is_superuser:
                return view_func(request, *arg, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator


def can_see_this_page(function):
    def wrapper(request, **kwargs):
        if request.user.is_superuser:
            return function(request, **kwargs)
        return redirect(reverse('page_not_found'))

    return wrapper
