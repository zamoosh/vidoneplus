import os
from django.contrib.auth.models import User
from library.cpanel import Cpanel
from library.helm import Helm
from library.kubectl import Kubectl
from .imports import *
from ..models import Setting as usetting
from ..models import *
import uuid


def _configpodname(tld):
    return tld + "-site", tld + "-app", tld + "-pwa"


# @login_required
def admin(request):
    context = {}
    context['users'] = User.objects.filter(is_staff=False)
    context['status'] = Status.objects.filter(user__in=context['users'])
    return render(request, "client/admin.html", context)


def admininstall(request, id):
    uid = uuid.uuid4().hex
    context = {}
    context['domain'] = usetting.objects.get(user__id=id).domain
    print(context['domain'])
    context['status'] = Status.objects.get(user__id=id)
    context['curent_user'] = User.objects.get(id=id)
    print(context['curent_user'])
    context['useremail'] = context['curent_user'].email
    context['username'] = ''.join(context['domain'].split('.')[:-1]) + uid[:4]
    context['site_name'], context['app_name'], context['pwa_name'] = _configpodname(context['domain'].split('.')[0])
    # save_setting = usetting.objects.get(id=context['curent_user'].id)
    # save_setting.site_name = context['site_name']
    # save_setting.admin_name = context['app_name']
    # save_setting.pwa_name = context['pwa_name']
    # save_setting.fullname = context['username']
    # save_setting.save()
    context['secretName'] = context['domain'].replace('.', '-')
    createVidone = Cpanel(context['username'], context['domain'])
    createVidone.create_acc()
    createVidone.add_or_edit_zone()
    dbname, dbuser, dbpass = createVidone.create_db()
    dirtemp = os.path.join(settings.MEDIA_ROOT, context['username'], 'config', '1')
    if not os.path.exists(dirtemp):
        direct = os.makedirs(dirtemp)
    siteyaml = """
nameOverride: "%s"
fullnameOverride: "%s"
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
    """ % (context['site_name'], context['site_name'], dbname, dbuser, dbpass, context['domain'], context['domain'],
           context['secretName'])
    appyaml = """
nameOverride: "%s"
fullnameOverride: "%s"
ingress:
  hosts:
    - host: admin.%s
      paths: ["/"]
  tls:
  - hosts:
    - admin.%s
    secretName: %s
    """ % (context['app_name'], context['app_name'], context['domain'], context['domain'], context['secretName'])
    pwayaml = """
nameOverride: "%s"
fullnameOverride: "%s"
ingress:
  hosts:
    - host: site.%s
      paths: ["/"]
  tls:
  - hosts:
    - site.%s
    secretName: %s
    """ % (context['pwa_name'], context['pwa_name'], context['domain'], context['domain'], context['secretName'])
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
    helm_install.install_app("website", context['site_name'], dirtemp + "/site-Chart.yaml", "0.0.0-beta70")
    helm_install.install_app("admindashvidone", context['app_name'], dirtemp + "/app-Chart.yaml", "0.0.1")
    helm_install.install_app("frontvidone", context['pwa_name'], dirtemp + "/pwa-Chart.yaml", "0.0.25")
    userStatus = context['status']
    userStatus.status = 1
    userStatus.save()
    return render(request, "client/create_vidone.html")


def createuser(request, domain):
    context = {}
    user_domain = usetting.objects.get(domain=domain)
    context['site_name'], context['app_name'], context['pwa_name'] = _configpodname(domain.split('.')[0])
    kubectl = Kubectl()
    kubectl.vidone_getsuperuser(context['app_name'])
    import secrets
    import string
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(8))
    print(password, user_domain.user.username, user_domain.user.email, context['site_name'])
    kubectl.vidone_createsuperuser(context['site_name'], user_domain.user.username, user_domain.user.email, password)


def adminremove(request, id):
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


def deleteuser(request, id):
    context = {}
    context['user'] = User.objects.get(id=id)
    context['user'].delete()
