from .imports import *


@login_required
def index(request):
    # from domainholder.models import Domainns
    context = {}
    return render(request, 'client/index.html', context)
