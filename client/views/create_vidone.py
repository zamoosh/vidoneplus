from library.cpanel import Cpanel
from .imports import *
from ..models import *


@login_required
def createvidone(request):
    context = {}

    return render(request, "client/create_vidone.html", context)