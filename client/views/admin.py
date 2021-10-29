import os
import yaml
from django.conf import settings
from library.cpanel import Cpanel
from library.helm import Helm
from .imports import *
from ..models import *
import uuid


@login_required
def admin(request):
    context = {}
    context['users'] = User.objects.filter(is_staff=False)
    context['status'] = Status.objects.filter(user__in=context['users'])
    return render(request, "client/admin.html", context)

def admininstall(request,id):
    uid = uuid.uuid4().hex
    context = {}
    context['domain'] = Setting.objects.get(user__id=id).domain
    context['curent_user'] = User.objects.get(id=id)
    context['username'] = ''.join(context['domain'].split('.')[:-1]) + uid[:4]
    context['tld'] = context['domain'].split('.')[0]
    context['site_name'] = "site-" + context['tld']
    context['app_name'] = "app-" + context['tld']
    context['pwa_name'] = "pwa-" + context['tld']
    save_setting = Setting.objects.get(id=context['curent_user'].id)
    save_setting.site_name = context['site_name']
    save_setting.admin_name = context['app_name']
    save_setting.pwa_name = context['pwa_name']
    save_setting.fullname = context['username']
    save_setting.save()
    context['secretName'] = context['domain'].replace('.', '-')
    createVidone = Cpanel(context['username'], context['domain'])
    createVidone.create_acc()
    createVidone.add_or_edit_zone()
    dbname, dbuser, dbpass = createVidone.create_db()
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
    """ % (context['tld'], context['tld'], dbname, dbuser, dbpass, context['domain'], context['domain'],
           context['secretName'])
    appyaml = """
nameOverride: "app-%s"
fullnameOverride: "app-%s"
ingress:
  hosts:
    - host: admin.%s
      paths: ["/"]
  tls:
  - hosts:
    - admin.%s
    secretName: %s
    """ % (context['tld'], context['tld'], context['domain'], context['domain'], context['secretName'])
    pwayaml = """
nameOverride: "pwa-%s"
fullnameOverride: "pwa-%s"
ingress:
  hosts:
    - host: site.%s
      paths: ["/"]
  tls:
  - hosts:
    - site.%s
    secretName: %s
    """ % (context['tld'], context['tld'], context['domain'], context['domain'], context['secretName'])
    dbdata = """
dbname: '%s'
dbuser: '%s'
dbpassword: '%s'
    """ % (dbname, dbuser, dbpass)
    with open(os.path.join(dirtemp, 'site-Chart.yaml'), 'w') as yaml_file:
        yaml_file.write(siteyaml)
    with open(os.path.join(dirtemp, 'app-Chart.yaml'), 'w') as yaml_file:
        yaml_file.write(appyaml)
    with open(os.path.join(dirtemp, 'pwa-Chart.yaml'), 'w') as yaml_file:
        yaml_file.write(pwayaml)
    with open(os.path.join(dirtemp, 'dbdata.txt'), 'w') as yaml_file:
        yaml_file.write(dbdata)
    helm_install = Helm()
    helm_install.install_app("website", "site-" + context['tld'], dirtemp + "/site-Chart.yaml", "0.0.0-beta59")
    helm_install.install_app("admindashvidone", "app-" + context['tld'], dirtemp + "/app-Chart.yaml", "0.0.1")
    helm_install.install_app("frontvidone", "pwa-" + context['tld'], dirtemp + "/pwa-Chart.yaml", "0.0.25")
    return render(request, "client/create_vidone.html")

def adminremove(request,id):
    context = {}
    context['domain'] = Setting.objects.get(user__id=id)
    context['dellApp'] = context['domain'].admin_name
    context['dellSite'] = context['domain'].site_name
    context['dellPwa'] = context['domain'].pwa_name
    helm_remove = Helm()
    helm_remove.delete_app(context['dellApp'])
    helm_remove.delete_app(context['dellSite'])
    helm_remove.delete_app(context['dellPwa'])
    return render(request, "client/create_vidone.html")