import requests

from .imports import *
import os
from django.urls import reverse
from django.contrib import messages
from library.cpanel import Cpanel
from library.helm import Helm
import mimetypes


@login_required
def user_settings(request, action=None):
    context = {}
    if Status.objects.get(user=request.user).active_user:
        try:
            context['settings'] = usetting.objects.get(owner=request.user)
            context['site_created'] = Status.objects.get(user=request.user)
        except usetting.DoesNotExist:
            action = "edit"
        if action == "edit":
            if request.method == "POST":
                context = {}
                context['user'] = request.user
                context['app_name'] = request.POST.get('app_name', '').strip()
                context['org_color'] = request.POST.get('org_colore', '').strip()
                context['sub_color'] = request.POST.get('sub_colore', '').strip()
                context['smsir_key'] = request.POST.get('smsir_key', '').strip()
                context['instagram'] = request.POST.get('instagram', '').strip()
                context['twitter'] = request.POST.get('twitter', '').strip()
                context['facebook'] = request.POST.get('facebook', '').strip()
                context['aparat'] = request.POST.get('aparat', '').strip()
                context['youtube'] = request.POST.get('youtube', '').strip()
                context['short_title'] = request.POST.get('short_title', '').strip()
                context['slogan'] = request.POST.get('slogan', '').strip()
                context['domain_type'] = request.POST.get('domain_type', '').strip()
                context['zarinpal'] = request.POST.get('zarinpal', '').strip()
                context['domain_fix'] = "vidoneplus.ir"
                if 'mydomain' in context['domain_type']:
                    context['domain'] = request.POST.get('domain', '').strip()
                if 'vidondomain' in context['domain_type']:
                    context['sub_domain'] = request.POST.get('sub_domain', '').strip()
                    context['domain'] = context['sub_domain'] + '.' + context['domain_fix']
                context['contact_phone'] = request.POST.get('contact_phone', '').strip()
                context['download_link'] = request.POST.get('download_link', '').strip()
                if '.' in context['domain'] and 'vidoneplus.ir' in context['domain']:
                    context['domain'] = context['domain'].split('.')[0] + '.' + context['domain_fix']
                if len(context['domain'].split("/")) > 1:
                    context['domain'] = context['domain'].split("/")[2]
                if context['domain'][:4] == "www.":
                    context['domain'] = context['domain'][4:]
                context['kuberid'] = context['domain'].split('.')[0]
                if not usetting.objects.filter(owner=request.user):
                    context['edit_setting'] = 1
                    seeting = usetting()
                    seeting.owner = context['user']
                    seeting.org_color = request.POST.get('org_colore', '').strip()
                    seeting.sub_color = request.POST.get('sub_colore', '').strip()
                    seeting.app_name = context['app_name']
                    seeting.instagram = context['instagram']
                    seeting.twitter = context['twitter']
                    seeting.aparat = context['aparat']
                    seeting.facebook = context['facebook']
                    seeting.youtube = context['youtube']
                    seeting.short_title = context['short_title']
                    seeting.slogan = context['slogan']
                    seeting.zarinpal = context['zarinpal']
                    seeting.smsir_key = context['smsir_key']
                    seeting.domain = context['domain']
                    if 'company_logo' in request.FILES:
                        seeting.company_logo = request.FILES['company_logo']
                    seeting.contact_phone = context['contact_phone']
                    seeting.download_link = context['download_link']
                    if 'splashscreen' in request.FILES:
                        seeting.splashscreen = request.FILES['splashscreen']
                    if 'favicon' in request.FILES:
                        seeting.favicon = request.FILES['favicon']
                    seeting.kuberid = context['kuberid'] + str(context['user'])[9:]
                    seeting.save()
                    appupdate = requests.get("https://app.vidone.org/update/")
                    context['result'] = "تنظیمات با موفقیت ثبت شد."
                else:
                    context['usreq'] = usetting.objects.get(owner=request.user)
                    context['username'] = context['usreq'].fullname
                    if context['domain'] and context['username'] and context['domain'] is not usetting.objects.get(
                            owner=request.user).domain:
                        context['app_name'] = context['usreq'].admin_name
                        context['pwa_name'] = context['usreq'].pwa_name
                        context['site_name'] = context['usreq'].site_name
                        context['secretName'] = context['domain'].replace('.', '-')
                        mylist = []
                        dirtemp = os.path.join(settings.MEDIA_ROOT, context['username'], 'config', '1')
                        with open(os.path.join(dirtemp, 'dbdata.txt')) as f:
                            lines = f.readlines()
                            for line in lines:
                                mylist.append(line)
                        newlist = []
                        for i in mylist:
                            if ':' not in i:
                                continue
                            newlist.append(i.split("\n")[0].split(": ")[1])
                        context['dbname'] = newlist[0]
                        context['dbuser'] = newlist[1]
                        context['dbpassword'] = newlist[2]
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
    """.format(sitename=context['site_name'], username=context['username'],
                                       domain=context['domain'], dbuser=context['dbuser'], dbpass=context['dbpassword'], dbname=context['dbname'],
                                       secretname=context['secretName'])
                        appyaml = """nameOverride: "%s"
fullnameOverride: "%s"
ingress:
  hosts:
    - host: admin.%s
      paths: ["/"]
  tls:
  - hosts:
    - admin.%s
    secretName: app-%s""" % (
                            context['app_name'], context['app_name'], context['domain'], context['domain'],
                            context['secretName'])
                        pwayaml = """nameOverride: "%s"
fullnameOverride: "%s"
ingress:
  hosts:
    - host: site.%s
      paths: ["/"]
  tls:
  - hosts:
    - site.%s
    secretName: pwa-%s""" % (
                            context['pwa_name'], context['pwa_name'], context['domain'], context['domain'],
                            context['secretName'])
                        with open(os.path.join(dirtemp, 'site-Chart.yaml'), 'w') as yaml_file:
                            yaml_file.write(siteyaml)
                        with open(os.path.join(dirtemp, 'app-Chart.yaml'), 'w') as yaml_file:
                            yaml_file.write(appyaml)
                        with open(os.path.join(dirtemp, 'pwa-Chart.yaml'), 'w') as yaml_file:
                            yaml_file.write(pwayaml)
                        upcpanel = Cpanel(context['username'], context['domain'])
                        print(context['username'], context['domain'])
                        upcpanel.update_acc_domain(context['domain'])
                        helm_install = Helm()
                        helm_install.install_app("website", context['site_name'], dirtemp + "/site-Chart.yaml",
                                                 "0.0.0-beta133")
                        helm_install.install_app("admindashvidone", context['app_name'], dirtemp + "/app-Chart.yaml",
                                                 "0.0.7")
                        helm_install.install_app("frontvidone", context['pwa_name'], dirtemp + "/pwa-Chart.yaml",
                                                 "0.0.27")
                    setting = usetting.objects.get(owner=request.user)
                    setting.org_color = context['org_color']
                    setting.sub_color = context['sub_color']
                    setting.instagram = context['instagram']
                    setting.twitter = context['twitter']
                    setting.aparat = context['aparat']
                    setting.facebook = context['facebook']
                    setting.youtube = context['youtube']
                    setting.short_title = context['short_title']
                    setting.slogan = context['slogan']
                    setting.app_name = context['app_name']
                    setting.zarinpal = context['zarinpal']
                    setting.smsir_key = context['smsir_key']
                    setting.domain = context['domain']
                    if 'company_logo' in request.FILES:
                        setting.company_logo = request.FILES['company_logo']
                    setting.contact_phone = context['contact_phone']
                    setting.download_link = context['download_link']
                    if 'splashscreen' in request.FILES:
                        setting.splashscreen = request.FILES['splashscreen']
                    if 'favicon' in request.FILES:
                        setting.favicon = request.FILES['favicon']
                    setting.save()
                    appupdate = requests.get("https://app.vidone.org/update/")
                    messages.success(request, "Setting is Change!")
                    return HttpResponseRedirect(reverse('client:setting'))
                context['settings'] = usetting.objects.get(owner=request.user)
            return render(request, "client/edit-setting.html", context)
    else:
        context['msg'] = "حساب کاربری شما تایید نشده است"
    return render(request, "client/setting.html", context)


def configs(request, domain):
    context = {}
    try:
        config = usetting.objects.get(domain=domain)
        context['domain'] = config.domain
        context['org_colore'] = config.org_color
        context['sub_colore'] = config.sub_color
        context['contact_phone'] = config.contact_phone
        context['instagram'] = config.instagram
        context['twitter'] = config.twitter
        context['aparat'] = config.aparat
        context['facebook'] = config.facebook
        context['youtube'] = config.youtube
        context['slogan'] = config.slogan
        context['short_title'] = config.short_title
        if config.splashscreen:
            context['splashscreen'] = request.build_absolute_uri() + config.splashscreen.url.split('/')[-1]
        else:
            context['splashscreen'] = ''
        if config.company_logo:
            context['company_logo'] = request.build_absolute_uri() + config.company_logo.url.split('/')[-1]
        if config.favicon:
            context['favicon'] = request.build_absolute_uri() + config.favicon.url.split('/')[-1]
        else:
            context['company_logo'] = ''
    except:
        pass
    return JsonResponse(context)


def static_files(request, domain, path=''):
    try:
        config = usetting.objects.get(domain=domain)
        if config.splashscreen.url.split('/')[-1] == path:
            path = config.splashscreen.path
        elif config.company_logo.url.split('/')[-1] == path:
            path = config.company_logo.path
        elif config.favicon.url.split('/')[-1] == path:
            path = config.favicon.path
        # config.company_logo
        # config.splashscreen
        if os.path.exists(path):
            with open(path, 'rb') as f:
                content = f.read()
                f.close()
            mimetypes.init()
            mime = mimetypes.types_map["." + path.split(".")[-1]]
            return HttpResponse(content, status=200, content_type=mime)
    except:
        pass
