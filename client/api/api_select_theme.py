from .imports import *


def api_select_theme(request):
    if request.GET.get('mode') == 'dark':
        request.user.extra['dark_mode'] = True
    else:
        if request.user.extra.get('dark_mode'):
            del request.user.extra['dark_mode']
    request.user.save()
    return JsonResponse({}, status=200)
