import os

import requests
from django.contrib.auth.models import User
from django.core import serializers
import json

from library.cpanel import Cpanel
from library.helm import Helm
from library.kubectl import Kubectl
from .imports import *
import uuid


def _configpodname(tld):
    return tld + "-site", tld + "-app", tld + "-pwa"


@login_required
def admin(request):
    context = {}
    context['users'] = User.objects.filter(is_staff=False)
    context['status'] = Status.objects.filter(user__in=context['users'])
    return render(request, "client/admin.html", context)


@login_required
def admininstall(request, id):
    uid = uuid.uuid4().hex
    context = {}
    context['domain'] = usetting.objects.get(owner__id=id).domain
    context['status'] = Status.objects.get(user__id=id)
    context['curent_user'] = User.objects.get(id=id)
    context['useremail'] = context['curent_user'].email
    context['username'] = ''.join(context['domain'].split('.')[:-1])[:10] + uid[:4]
    context['site_name'], context['app_name'], context['pwa_name'] = _configpodname(context['domain'].split('.')[0])
    save_setting = usetting.objects.get(owner=context['curent_user'])
    save_setting.site_name = context['site_name']
    save_setting.admin_name = context['app_name']
    save_setting.pwa_name = context['pwa_name']
    save_setting.fullname = context['username']
    save_setting.save()
    context['secretName'] = context['domain'].replace('.', '-')
    createVidone = Cpanel(context['username'], context['domain'])
    print('cp class generated', context['username'], context['domain'])
    createVidone.create_acc()
    print('acc created.')
    createVidone.add_or_edit_zone()
    dbname, dbuser, dbpass = createVidone.create_db()
    dirtemp = os.path.join(settings.MEDIA_ROOT, context['username'], 'config', '1')
    if not os.path.exists(dirtemp):
        direct = os.makedirs(dirtemp)
    siteyaml = """nameOverride: "{sitename}"
fullnameOverride: {sitename}
database:
  dbengine: 'django.db.backends.mysql'
  dbname: '{dbname}'
  dbuser: '{dbuser}'
  dbpassword: '{dbpass}'
  dbhost: 'cpanel.vidone.org'
storage:
  media_root: '/storage/{username}'
  buket: '{username}'
domain: '{domain}'
ingress:
  hosts:
    - host: {domain}
      paths: ["/"]
  tls:
  - hosts:
    - {domain}
    secretName: {secretname}
    """.format(sitename=context['site_name'], username=context['username'], domain=context['domain'], dbuser=dbuser,
               dbpass=dbpass, dbname=dbname, secretname=context['secretName'])
    appyaml = """nameOverride: "{sitename}"
fullnameOverride: "{sitename}"
ingress:
  hosts:
    - host: admin.{domain}
      paths: ["/"]
  tls:
  - hosts:
    - admin.{domain}
    secretName: app-{secretname}
    """.format(sitename=context['app_name'], domain=context['domain'], dbuser=dbuser, secretname=context['secretName'])
    pwayaml = """nameOverride: "{sitename}"
fullnameOverride: "{sitename}"
ingress:
  hosts:
    - host: site.{domain}
      paths: ["/"]
  tls:
  - hosts:
    - site.{domain}
    secretName: pwa-{secretname}
    """.format(sitename=context['pwa_name'], domain=context['domain'], dbuser=dbuser, secretname=context['secretName'])
    dbdata = """dbname: {dbname}
dbuser: {dbuser}
dbpassword: {dbpass}""".format(dbname=dbname, dbuser=dbuser, dbpass=dbpass)
    with open(os.path.join(dirtemp, 'site-Chart.yaml'), 'w') as yaml_file:
        yaml_file.write(siteyaml)
    with open(os.path.join(dirtemp, 'app-Chart.yaml'), 'w') as yaml_file:
        yaml_file.write(appyaml)
    with open(os.path.join(dirtemp, 'pwa-Chart.yaml'), 'w') as yaml_file:
        yaml_file.write(pwayaml)
    with open(os.path.join(dirtemp, 'dbdata.txt'), 'w') as yaml_file:
        yaml_file.write(dbdata)
    context['result'] = "هاست با موفقیت ایجاد شد."
    return render(request, "client/create_vidone.html", context)


@login_required
def verion(request):
    context = {}
    try:
        context['show_versions'] = Imagetag.objects.all()
        print(context['versions'])
    except:
        pass

    return render(request, "client/view_version.html", context)


@login_required
def edit_verion(request, id, action=None):
    context = {}
    context['version'] = Imagetag.objects.get(id=id)
    if action == "active":
        imagetag = Imagetag.objects.get(id=id)
        imagetag.status = True
        return render(request, "client/view_version.html")

    if action == "deactive":
        imagetag = Imagetag.objects.get(id=id)
        imagetag.status = False
        return render(request, "client/view_version.html")

    if request.method == "POST":
        context['req'] = {}
        context['req']['pwa_version'] = request.POST.get('pwa_version', '').strip()
        context['req']['pwa_description'] = request.POST.get('pwa_description', '').strip()
        context['req']['admin_version'] = request.POST.get('admin_version', '').strip()
        context['req']['admin_description'] = request.POST.get('admin_description', '').strip()
        context['req']['site_version'] = request.POST.get('site_version', '').strip()
        context['req']['site_description'] = request.POST.get('site_description', '').strip()
        context['req']['android_version'] = request.POST.get('android_version', '').strip()
        context['req']['android_description'] = request.POST.get('android_description', '').strip()
        context['req']['ios_version'] = request.POST.get('ios_version', '').strip()
        context['req']['ios_description'] = request.POST.get('ios_description', '').strip()
        context['req']['force_update'] = request.POST.get('force_update', '').strip()
        imagetag = Imagetag.objects.get(id=id)
        imagetag.pwa_version = context['req']['pwa_version']
        imagetag.pwa_description = context['req']['pwa_description']
        imagetag.admin_version = context['req']['admin_version']
        imagetag.admin_description = context['req']['admin_description']
        imagetag.site_version = context['req']['site_version']
        imagetag.site_description = context['req']['site_description']
        imagetag.android_version = context['req']['android_version']
        imagetag.android_description = context['req']['android_description']
        imagetag.ios_version = context['req']['ios_version']
        imagetag.ios_description = context['req']['ios_description']
        if 'force' in context['req']['force_update']:
            imagetag.forceupdate = True
        else:
            imagetag.forceupdate = False
        imagetag.save()
    return render(request, "client/create_version.html", context)


@login_required
def create_verion(request):
    context = {}
    if request.method == "POST":
        context['req'] = {}
        context['req']['pwa_version'] = request.POST.get('pwa_version', '').strip()
        context['req']['pwa_description'] = request.POST.get('pwa_description', '').strip()
        context['req']['admin_version'] = request.POST.get('admin_version', '').strip()
        context['req']['admin_description'] = request.POST.get('admin_description', '').strip()
        context['req']['site_version'] = request.POST.get('site_version', '').strip()
        context['req']['site_description'] = request.POST.get('site_description', '').strip()
        context['req']['android_version'] = request.POST.get('android_version', '').strip()
        context['req']['android_description'] = request.POST.get('android_description', '').strip()
        context['req']['ios_version'] = request.POST.get('ios_version', '').strip()
        context['req']['ios_description'] = request.POST.get('ios_description', '').strip()
        context['req']['force_update'] = request.POST.get('force_update', '').strip()
        imagetag = Imagetag()
        imagetag.pwa_version = context['req']['pwa_version']
        imagetag.pwa_description = context['req']['pwa_description']
        imagetag.admin_version = context['req']['admin_version']
        imagetag.admin_description = context['req']['admin_description']
        imagetag.site_version = context['req']['site_version']
        imagetag.site_description = context['req']['site_description']
        imagetag.android_version = context['req']['android_version']
        imagetag.android_description = context['req']['android_description']
        imagetag.ios_version = context['req']['ios_version']
        imagetag.ios_description = context['req']['ios_description']
        if 'force' in context['req']['force_update']:
            imagetag.forceupdate = True
        imagetag.save()
    return render(request, "client/create_version.html", context)


@login_required
def install_sites(request, id):
    context = {}
    settingconf = usetting.objects.get(owner__id=id)
    context['domain'] = settingconf.domain
    context['username'] = settingconf.fullname
    context['site_name'], context['app_name'], context['pwa_name'] = _configpodname(context['domain'].split('.')[0])
    dirtemp = os.path.join(settings.MEDIA_ROOT, context['username'], 'config', '1')
    print(dirtemp)
    helm_install = Helm()
    helm_install.install_app("website", context['site_name'], dirtemp + "/site-Chart.yaml",
                             settingconf.image_tag.site_version)
    helm_install.install_app("admindashvidone", context['app_name'], dirtemp + "/app-Chart.yaml",
                             settingconf.image_tag.admin_version)
    helm_install.install_app("frontvidone", context['pwa_name'], dirtemp + "/pwa-Chart.yaml",
                             settingconf.image_tag.pwa_version)
    context['status'] = Status.objects.get(user__id=id)
    userStatus = context['status']
    userStatus.site_created = 1
    userStatus.save()
    context['result'] = "سایت ها با موفقیت نصب شدند."
    return render(request, "client/create_vidone.html", context)


@login_required
def check_or_createuser(request, id):
    context = {}
    import secrets
    import string
    alphabet = string.ascii_letters + string.digits
    context['password'] = ''.join(secrets.choice(alphabet) for i in range(8))
    kubectl = Kubectl()
    settingconf = usetting.objects.get(owner__id=id)
    context['domain'] = settingconf.domain
    context['setting'] = settingconf
    context['site_name'], context['app_name'], context['pwa_name'] = _configpodname(context['domain'].split('.')[0])
    context['super_user'] = kubectl.vidone_getsuperuser(context['site_name'])
    if context['super_user'] is not None:
        context['superusers'] = kubectl.vidone_getsuperuser(context['site_name'])
        print(context['superusers'])
        # vidone_updateuser(self, appname, username, password)
    if not context['super_user']:
        context['create_user'] = True
        context['username'] = context['setting'].owner.username
        if '+98' in context['username']:
            context['username'] = context['username'].replace('+98','0')
        kubectl.vidone_createsuperuser(context['site_name'], context['username'], context['setting'].owner.email,
                                       context['password'])
        PasswordGenerator(setting=settingconf, username=context['username'], password=context['password']).save()
        pgenarator = PasswordGenerator.objects.filter(setting=settingconf, username=context['username'],
                                                      password=context['password'])
        pgenarator = serializers.serialize("json", pgenarator)
        requests.post('https://%s/update_admin_password/' % (settingconf.domain), data=json.dumps(pgenarator))
    return render(request, "client/create_super_user.html", context)


@login_required
def resetpassword(request, user):
    context = {}
    import secrets
    import string
    context['update_user'] = True
    alphabet = string.ascii_letters + string.digits
    context['password'] = ''.join(secrets.choice(alphabet) for i in range(8))
    kubectl = Kubectl()
    context['username'] = user
    setting = usetting.objects.get(owner__cellphone=user)
    context['domain'] = setting.domain
    context['site_name'], context['app_name'], context['pwa_name'] = _configpodname(context['domain'].split('.')[0])
    context['updateuser'] = kubectl.vidone_updateuser(context['site_name'], context['username'], context['password'])
    PasswordGenerator(setting=setting, username=context['username'], password=context['password']).save()
    pgenarator = PasswordGenerator.objects.filter(setting=setting, username=context['username'],
                                               password=context['password'])
    pgenarator = serializers.serialize("json", pgenarator)
    requests.post('https://%s/update_admin_password/' % (setting.domain), data=json.dumps(pgenarator))
    return render(request, "client/create_super_user.html", context)


@login_required
def adminremove(request, id):
    context = {}
    context['domain'] = Setting.objects.get(owner__id=id)
    context['dellApp'] = context['domain'].admin_name
    context['dellSite'] = context['domain'].site_name
    context['dellPwa'] = context['domain'].pwa_name
    helm_remove = Helm()
    helm_remove.delete_app(context['dellApp'])
    helm_remove.delete_app(context['dellSite'])
    helm_remove.delete_app(context['dellPwa'])
    return render(request, "client/create_vidone.html")
