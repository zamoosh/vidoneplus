from .imports import *

def profile(request):
    context = {}
    return render(request, 'client/profile.html', context)