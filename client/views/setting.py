import os
from django.core import serializers
from django.urls import reverse

from library.cpanel import Cpanel
from library.helm import Helm
from .imports import *
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from ..models import Setting as usetting, Status


@login_required
def user_settings(request, action=None):
    context = {}
    if Status.objects.get(user=request.user).status:
        try:
            context['settings'] = usetting.objects.get(user=request.user)
            context['site_created'] = Status.objects.get(user=request.user)
        except usetting.DoesNotExist:
            action = "edit"
        if action == "edit":
            if request.method == "POST":
                context = {}
                context['user'] = request.user
                context['org_colore'] = request.POST.get('org_colore', '').strip()
                context['sub_colore'] = request.POST.get('sub_colore', '').strip()
                context['app_name'] = request.POST.get('app_name', '').strip()
                context['domain'] = request.POST.get('domain', '').strip()
                context['contact_phone'] = request.POST.get('contact_phone', '').strip()
                context['download_link'] = request.POST.get('download_link', '').strip()
                if len(context['domain'].split("/")) > 1:
                    context['domain'] = context['domain'].split("/")[2]
                if context['domain'][:4] == "www.":
                    context['domain'] = context['domain'][4:]
                context['kuberid'] = context['domain'].split('.')[0]
                if not usetting.objects.filter(user=request.user):
                    context['edit_setting'] = 1
                    print(context['domain'])
                    seeting = usetting()
                    seeting.user = context['user']
                    seeting.org_colore = context['org_colore']
                    seeting.sub_colore = context['sub_colore']
                    seeting.app_name = context['app_name']
                    seeting.domain = context['domain']
                    if 'company_logo' in request.FILES:
                        seeting.company_logo = request.FILES['company_logo']
                    seeting.contact_phone = context['contact_phone']
                    seeting.download_link = context['download_link']
                    if 'splashscreen' in request.FILES:
                        seeting.splashscreen = request.FILES['splashscreen']
                    seeting.kuberid = context['kuberid'] + str(context['user'])[9:]
                    seeting.save()
                    context['result'] = "تنظیمات با موفقیت ثبت شد."
                else:
                    if context['domain'] is not usetting.objects.get(user=request.user).domain:
                        print(context['domain'])
                        context['usreq'] = usetting.objects.get(user=request.user)
                        print(context['usreq'])
                        context['username'] = context['usreq'].fullname
                        print(context['username'])
                        context['app_name'] = context['usreq'].admin_name
                        context['pwa_name'] = context['usreq'].pwa_name
                        context['site_name'] = context['usreq'].site_name
                        context['secretName'] = context['domain'].replace('.', '-')
                        dirtemp = os.path.join(settings.MEDIA_ROOT, context['username'], 'config', '1')
                        mylist = []
                        with open(os.path.join(dirtemp, 'dbdata.txt')) as f:
                            lines = f.readlines()
                            for line in lines:
                               mylist.append(line)
                        newlist = []
                        for i in mylist:
                            newlist.append(i.split("\n")[0].split(": ")[1])
                        context['dbname'] = newlist[0]
                        context['dbuser'] = newlist[1]
                        context['dbpassword'] = newlist[2]
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
                            """ % (context['site_name'], context['site_name'], context['dbname'], context['dbuser'],
                                   context['dbpassword'], context['domain'],
                                   context['domain'],
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
    secretName: app-%s
                            """ % (context['app_name'], context['app_name'], context['domain'], context['domain'],
                                   context['secretName'])
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
    secretName: pwa-%s
                            """ % (context['pwa_name'], context['pwa_name'], context['domain'], context['domain'],
                                   context['secretName'])
                        with open(os.path.join(dirtemp, 'site-Chart.yaml'), 'w') as yaml_file:
                            yaml_file.write(siteyaml)
                        with open(os.path.join(dirtemp, 'app-Chart.yaml'), 'w') as yaml_file:
                            yaml_file.write(appyaml)
                        with open(os.path.join(dirtemp, 'pwa-Chart.yaml'), 'w') as yaml_file:
                            yaml_file.write(pwayaml)
                        upcpanel = Cpanel(context['username'], context['domain'])
                        upcpanel.update_acc_domain(context['domain'])
                        helm_install = Helm()
                        helm_install.install_app("website", context['site_name'], dirtemp + "/site-Chart.yaml",
                                                 "0.0.0-beta70")
                        helm_install.install_app("admindashvidone", context['app_name'], dirtemp + "/app-Chart.yaml",
                                                 "0.0.1")
                        helm_install.install_app("frontvidone", context['pwa_name'], dirtemp + "/pwa-Chart.yaml", "0.0.25")
                    setting = usetting.objects.get(user=request.user)
                    setting.org_colore = context['org_colore']
                    setting.sub_colore = context['sub_colore']
                    setting.app_name = context['app_name']
                    setting.domain = context['domain']
                    if 'company_logo' in request.FILES:
                        setting.company_logo = request.FILES['company_logo']
                    setting.contact_phone = context['contact_phone']
                    setting.download_link = context['download_link']
                    if 'splashscreen' in request.FILES:
                        setting.splashscreen = request.FILES['splashscreen']
                    setting.save()
                    context['result'] = "تنظیمات با موفقیت تغییر کرد."
                context['settings'] = usetting.objects.get(user=request.user)
            return render(request, "client/edit-setting.html", context)
    else:
        context['msg'] = "حساب کاربری شما تایید نشده است"
    return render(request, "client/setting.html", context)

def configs(request, domain):
    context = {}
    try:
        config = usetting.objects.get(domain=domain)
        context['domain'] = config.domain
        context['org_colore'] = config.org_colore
        context['sub_colore'] = config.sub_colore
        context['app_name'] = config.app_name
        context['site_name'] = config.site_name
        context['admin_name'] = config.admin_name
        context['pwa_name'] = config.pwa_name
        context['fullname'] = config.fullname
    except:
        pass
    return JsonResponse(context)
