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
        context['tld'] = data[1].split('.')[0]
        context['secretName'] = data[1].replace('.', '-')
        createVidone = Cpanel(context['username'], context['domain'])
        createVidone.create_acc()
        createVidone.add_or_edit_zone()
        dbname, dbpass, dbuser = createVidone.create_db()
        dirtemp = os.path.join(settings.MEDIA_ROOT, context['username'], 'config', '1')
        if not os.path.exists(dirtemp):
            direct = os.makedirs(dirtemp)
        siteyaml = """
nameOverride: "site-%s"
fullnameOverride: "site-%s"
database:
  dbengine: 'django.db.backends.mysql'
  dbname: '%s'
  dbuser: '%s'
  dbpassword: '%s'
  dbhost: 'cpanel.vidone.org'
ingress:
  hosts:
    - host: %s
      paths: ["/"]
  tls:
  - hosts:
    - %s
    secretName: %s
"""%(context['tld'], context['tld'], dbname, dbuser, dbpass, context['domain'], context['domain'], context['secretName'])
        appyaml = """
nameOverride: "app-%s"
fullnameOverride: "app-%s"
ingress:
  hosts:
    - host: %s
      paths: ["/"]
  tls:
  - hosts:
    - %s
    secretName: %s
"""%(context['tld'], context['tld'], context['domain'], context['domain'], context['secretName'])
        pwayaml = """
nameOverride: "pwa-%s"
fullnameOverride: "pwa-%s"
ingress:
  hosts:
    - host: %s
      paths: ["/"]
  tls:
  - hosts:
    - %s
    secretName: %s
"""%(context['tld'], context['tld'], context['domain'], context['domain'], context['secretName'])
        with open(os.path.join(dirtemp, 'site-Chart.yml'), 'w') as yaml_file:
            yaml_file.write(siteyaml)
        with open(os.path.join(dirtemp, 'app-Chart.yml'), 'w') as yaml_file:
            yaml_file.write(appyaml)
        with open(os.path.join(dirtemp, 'pwa-Chart.yml'), 'w') as yaml_file:
            yaml_file.write(pwayaml)
        return render(request, "client/create_vidone.html", context)
    return render(request, "client/admin.html", context)
