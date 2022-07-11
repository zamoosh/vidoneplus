from .imports import *


def api_get_available_force_version(request):
    context = {}
    first_force = Imagetag.objects.filter(status=True, forceupdate=True).first()
    for key, value in first_force.__dict__.items():
        if not key.startswith('_'):
            context[key] = value
    return JsonResponse(context, status=200)
