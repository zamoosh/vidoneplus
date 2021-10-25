from .imports import *


@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect("/")
