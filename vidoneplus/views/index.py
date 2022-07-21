from .imports import *


def index(request):
    return render(request, 'client/dashboard.html')
