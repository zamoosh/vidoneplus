import requests
from django.core import serializers
import json

from library.kubectl import Kubectl
from .imports import *


def _configpodname(tld):
    return tld + "-site", tld + "-app", tld + "-pwa"


@login_required
@allowed_users(allowed_roles=['admin'])
def check_or_createuser(request, id):
    import secrets
    import string
    alphabet = string.ascii_letters + string.digits
    kubectl = Kubectl()
    settingconf = usetting.objects.get(owner__id=id)
    context = {'domain': settingconf.domain,
               'username': settingconf.fullname,
               'site_name': _configpodname(settingconf.domain.split('.')[0])[0],
               'app_name': _configpodname(settingconf.domain.split('.')[0])[1],
               'pwa_name': _configpodname(settingconf.domain.split('.')[0])[2],
               'password': ''.join(secrets.choice(alphabet) for i in range(8))}

    if kubectl.vidone_getsuperuser(context['site_name']) is not None:
        context['superusers'] = kubectl.vidone_getsuperuser(context['site_name'])
        # vidone_updateuser(self, appname, username, password)
    if not context['superusers']:
        context['create_user'] = True
        context['username'] = context['setting'].owner.username
        if '+98' in context['username']:
            context['username'] = context['username'].replace('+98', '0')
        kubectl.vidone_createsuperuser(context['site_name'], context['username'], context['setting'].owner.email,
                                       context['password'])
        PasswordGenerator(setting=settingconf, username=context['username'], password=context['password']).save()
        pgenarator = PasswordGenerator.objects.filter(setting=settingconf, username=context['username'],
                                                      password=context['password'])
        pgenarator = serializers.serialize("json", pgenarator)
        requests.post('https://%s/update_admin_password/' % (settingconf.domain), data=json.dumps(pgenarator))
    return render(request, f"{app_name.name}/{__name__.split('.')[-1]}.html", context)


@login_required
@allowed_users(allowed_roles=['admin'])
def resetpassword(request, id, user):
    import secrets
    import string
    alphabet = string.ascii_letters + string.digits
    kubectl = Kubectl()
    setting = usetting.objects.get(id=id)
    context = {'update_user': True,
               'password': ''.join(secrets.choice(alphabet) for i in range(8)),
               'username': user,
               'domain': setting.domain,
               'site_name': _configpodname(setting.domain.split('.')[0])[0],
               'app_name': _configpodname(setting.domain.split('.')[0])[1],
               'pwa_name': _configpodname(setting.domain.split('.')[0])[2]}

    context['updateuser'] = kubectl.vidone_updateuser(context['site_name'], context['username'], context['password'])
    PasswordGenerator(setting=setting, username=context['username'], password=context['password']).save()
    pgenarator = PasswordGenerator.objects.filter(setting=setting, username=context['username'],
                                                  password=context['password'])
    pgenarator = serializers.serialize("json", pgenarator)
    requests.post('https://%s/update_admin_password/' % (setting.domain), data=json.dumps(pgenarator))
    return render(request, f"{app_name.name}/{__name__.split('.')[-1]}.html", context)
