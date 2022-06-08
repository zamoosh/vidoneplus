from library.cpanel import Cpanel
from .imports import *
from ..models import *
import uuid
from library.helm_yaml import core_yaml, admin_yaml, site_yaml, dbdata
from client.decorators import allowed_users
from library.helm import Helm
import os


def _configpodname(tld):
    return tld + "-core", tld + "-admin", tld + "-site"


@login_required
def createvidone(request):
    context = {}

    return render(request, f"{app_name.name}/{__name__.split('.')[-1]}.html", context)


@login_required
@allowed_users(allowed_roles=['admin'])
def admininstall(request, id):
    uid = uuid.uuid4().hex
    domain = usetting.objects.get(owner__id=id).domain
    context = {'domain': domain,
               'status': Status.objects.get(user__id=id),
               'curent_user': User.objects.get(id=id),
               'useremail': User.objects.get(id=id).email,
               'username': ''.join(domain.split('.')[:-1])[:10] + uid[:4],
               'site_name': _configpodname(domain.split('.')[0])[0],
               'app_name': _configpodname(domain.split('.')[0])[1],
               'pwa_name': _configpodname(domain.split('.')[0])[2],
               'secretName': domain.replace('.', '-')}

    save_setting = usetting.objects.get(owner=context['curent_user'])
    save_setting.site_name = context['site_name']
    save_setting.admin_name = context['app_name']
    save_setting.pwa_name = context['pwa_name']
    save_setting.fullname = context['username']
    save_setting.save()
    createVidone = Cpanel(context['username'], context['domain'])
    createVidone.create_acc()
    createVidone.add_or_edit_zone()
    dbname, dbuser, dbpass = createVidone.create_db()
    dirtemp = os.path.join(settings.MEDIA_ROOT, context['username'])
    if not os.path.exists(dirtemp):
        direct = os.makedirs(dirtemp)
    with open(os.path.join(dirtemp, 'core-Chart.yaml'), 'w') as yaml_file:
        yaml_file.write(core_yaml(context['site_name'], context['username'], context['domain'], dbuser, dbpass, dbname,
                                  context['secretName']))
    with open(os.path.join(dirtemp, 'app-Chart.yaml'), 'w') as yaml_file:
        yaml_file.write(admin_yaml(context['app_name'], context['domain'], context['secretName']))
    with open(os.path.join(dirtemp, 'pwa-Chart.yaml'), 'w') as yaml_file:
        yaml_file.write(site_yaml(context['pwa_name'], context['domain'], context['secretName']))
    with open(os.path.join(dirtemp, 'dbdata.txt'), 'w') as yaml_file:
        yaml_file.write(dbdata(dbname, dbuser, dbpass))
    context['result'] = "هاست با موفقیت ایجاد شد."
    return render(request, f"{app_name.name}/{__name__.split('.')[-1]}.html", context)


@login_required
@allowed_users(allowed_roles=['admin'])
def install_sites(request, id):
    settingconf = usetting.objects.get(owner__id=id)
    context = {'domain': settingconf.domain,
               'username': settingconf.fullname,
               'site_name': _configpodname(settingconf.domain.split('.')[0])[0],
               'app_name': _configpodname(settingconf.domain.split('.')[0])[1],
               'pwa_name': _configpodname(settingconf.domain.split('.')[0])[2],
               'status': Status.objects.get(user__id=id)}
    print(context['site_name'])
    print(context['app_name'])

    dirtemp = os.path.join(settings.MEDIA_ROOT, context['username'], 'config', '1')
    print(dirtemp)
    helm_install = Helm()
    print('site')
    helm_install.install_app("website", context['site_name'], dirtemp + "/site-Chart.yaml",
                             settingconf.image_tag.site_version)
    print('app')
    helm_install.install_app("admindashvidone", context['app_name'], dirtemp + "/app-Chart.yaml",
                             settingconf.image_tag.admin_version)
    print('pwa')
    helm_install.install_app("frontvidone", context['pwa_name'], dirtemp + "/pwa-Chart.yaml",
                             settingconf.image_tag.pwa_version)
    userStatus = context['status']
    userStatus.site_created = 1
    userStatus.save()
    context['result'] = "سایت ها با موفقیت نصب شدند."
    return render(request, f"{app_name.name}/{__name__.split('.')[-1]}.html", context)


@login_required
@allowed_users(allowed_roles=['admin'])
def adminremove(request, id):
    domain = Setting.objects.get(owner__id=id)
    context = {'domain': domain,
               'dellApp': domain.admin_name,
               'dellSite': domain.site_name,
               'dellPwa': domain.pwa_name}
    helm_remove = Helm()
    helm_remove.delete_app(context['dellApp'])
    helm_remove.delete_app(context['dellSite'])
    helm_remove.delete_app(context['dellPwa'])
    return render(request, f"{app_name.name}/{__name__.split('.')[-1]}.html")
