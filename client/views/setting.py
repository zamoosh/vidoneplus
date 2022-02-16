import requests
from django.shortcuts import get_object_or_404

from .imports import *
import os
from django.urls import reverse
from django.contrib import messages
from library.cpanel import Cpanel
from library.helm import Helm
import mimetypes
from library.helm_yaml import siteyaml, appyaml, pwayaml


@login_required
def user_settings(request, action=None):
    context = {}
    is_user_active = False
    try:
        if Status.objects.get(user=request.user).active_user:
            is_user_active = True
    except:
        context['msg'] = "حساب کاربری شما تایید نشده است"
    if is_user_active:
        try:
            context['settings'] = usetting.objects.get(owner=request.user)
            context['site_created'] = Status.objects.get(user=request.user)
        except usetting.DoesNotExist:
            action = "edit"
        if action == "edit":
            if request.method == "POST":
                context = {}
                context['user'] = request.user
                for key, value in request.POST.items():
                    if key == 'csrfmiddlewaretoken' or key == 'splashscreen' or key == 'favicon':
                        continue
                    context[key] = value
                context['domain_fix'] = "vidoneplus.ir"
                if 'vidondomain' in context['domain_type']:
                    context['domain'] = context['sub_domain'] + '.' + context['domain_fix']
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
                    seeting.owner, seeting.org_color, seeting.sub_color, seeting.app_name, _, seeting.domain, _ \
                        , seeting.contact_phone, seeting.instagram, seeting.twitter, seeting.aparat, seeting.facebook \
                        , seeting.youtube, seeting.slogan, seeting.short_title, seeting.zarinpal, seeting.smsir_key \
                        , seeting.download_link, _ = context.values()
                    if 'company_logo' in request.FILES:
                        seeting.company_logo = request.FILES['company_logo']
                    if 'splashscreen' in request.FILES:
                        seeting.splashscreen = request.FILES['splashscreen']
                    if 'favicon' in request.FILES:
                        seeting.favicon = request.FILES['favicon']
                    seeting.kuberid = context['kuberid'] + str(context['user'])[9:]
                    seeting.save()
                    # appupdate = requests.get("https://%s/update/"%(seeting.domain))
                    context['result'] = "تنظیمات با موفقیت ثبت شد."
                else:
                    setting = usetting.objects.get(owner=request.user)
                    setting.owner, setting.org_color, setting.sub_color, setting.app_name, _, setting.domain, _ \
                        , setting.contact_phone, setting.instagram, setting.twitter, setting.aparat, setting.facebook \
                        , setting.youtube, setting.slogan, setting.short_title, setting.zarinpal, setting.smsir_key \
                        , setting.download_link, _, _, _ = context.values()
                    context['usreq'] = usetting.objects.get(owner=request.user)
                    context['username'] = context['usreq'].fullname
                    if context['domain'] and context['username'] and context['domain'] is not usetting.objects.get(
                            owner=request.user).domain:
                        context['app_name'] = context['usreq'].admin_name
                        setting.app_name = context['app_name']
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
                        with open(os.path.join(dirtemp, 'site-Chart.yaml'), 'w') as yaml_file:
                            yaml_file.write(siteyaml(context['site_name'], context['username'], context['domain'],
                                                     context['dbuser'], context['dbpassword'], context['dbname'],
                                                     context['secretName']))
                        with open(os.path.join(dirtemp, 'app-Chart.yaml'), 'w') as yaml_file:
                            yaml_file.write(appyaml(context['app_name'], context['domain'], context['secretName']))
                        with open(os.path.join(dirtemp, 'pwa-Chart.yaml'), 'w') as yaml_file:
                            yaml_file.write(pwayaml(context['pwa_name'], context['domain'], context['secretName']))
                        upcpanel = Cpanel(context['username'], context['domain'])
                        print(context['username'], context['domain'])
                        upcpanel.update_acc_domain(context['domain'])
                        helm_install = Helm()
                        helm_install.install_app("website", context['site_name'], dirtemp + "/site-Chart.yaml",
                                                 context['usreq'].image_tag.site_version)
                        helm_install.install_app("admindashvidone", context['app_name'], dirtemp + "/app-Chart.yaml",
                                                 context['usreq'].image_tag.admin_version)
                        helm_install.install_app("frontvidone", context['pwa_name'], dirtemp + "/pwa-Chart.yaml",
                                                 context['usreq'].image_tag.pwa_version)
                    if 'company_logo' in request.FILES:
                        setting.company_logo = request.FILES['company_logo']
                    if 'splashscreen' in request.FILES:
                        setting.splashscreen = request.FILES['splashscreen']
                    if 'favicon' in request.FILES:
                        setting.favicon = request.FILES['favicon']
                    setting.save()
                    appupdate = requests.get("https://%s/update/" % (setting.domain))
                    messages.success(request, "Setting is Change!")
                    return HttpResponseRedirect(reverse('client:setting'))
                context['settings'] = usetting.objects.get(owner=request.user)
            return render(request, f"{app_name.name}/{__name__.split('.')[-1]}.html", context)
    else:
        context['msg'] = "حساب کاربری شما تایید نشده است"
    return render(request, f"{app_name.name}/{__name__.split('.')[-1]}.html", context)


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
        if config.splashscreen:
            if config.splashscreen.path.split('/')[-1] == path:
                path = config.splashscreen.path
        if config.company_logo:
            if config.company_logo.path.split('/')[-1] == path:
                path = config.company_logo.path
        if config.favicon:
            if config.favicon.path.split('/')[-1] == path:
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
