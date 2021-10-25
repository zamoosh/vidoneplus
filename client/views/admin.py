import os
import yaml
from django.conf import settings
from library.cpanel import Cpanel
from .imports import *
from ..models import *
import uuid

@login_required
def admin(request):
    context = {}
    context['users'] = User.objects.filter(is_staff=False)
    context['status'] = Status.objects.filter(user__in=context['users'])
    if request.method == "POST":
        uid = uuid.uuid4().hex
        data = [key for key in request.POST.keys()][1].split("|")
        context['cellphone'] = data[0]
        context['username'] = ''.join(data[1].split('.')[:-1]) + uid[:4]
        context['domain'] = data[1]
        createVidone = Cpanel(context['username'],context['domain'])
        createVidone.create_acc()
        createVidone.add_or_edit_zone()
        dbname,dbpass,dbuser = createVidone.create_db()
        dirtemp = os.path.join(settings.MEDIA_ROOT, context['username'], 'config', '1')
        if not os.path.exists(dirtemp):
            direct = os.makedirs(dirtemp)
        print(dirtemp)
        datayaml ="""
nameOverride: "vidone-stage"
fullnameOverride: "vidone-stage"
database:
  dbengine: 'django.db.backends.mysql'
  dbname: '%s'
  dbuser: '%s'
  dbpassword: '%s'
  dbhost: 'cpanel.vidone.org'
ingress:
  hosts:
    - host: app.vidone.org
      paths: ["/"]
  tls:
  - hosts:
    - app.vidone.org
    secretName: app-vidone-cert
"""%(dbname,dbuser,dbpass)
        with open(os.path.join(dirtemp, 'Chart.yml'), 'w') as yaml_file:
            yaml_file.write(datayaml)
        return render(request, "client/create_vidone.html", context)
    return render(request, "client/admin.html", context)
