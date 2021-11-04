from django.core import serializers
from django.urls import reverse

from .imports import *
from django.http import JsonResponse, HttpResponse
from ..models import Setting as usetting, Status


@login_required
def settings(request, action=None):
    context = {}
    if Status.objects.get(user=request.user).status:
        try:
            context['settings'] = usetting.objects.get(user=request.user)
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
                # context['company_logo'] = request.FILES['company_logo']
                # context['splashscreen'] = request.FILES['splashscreen']
                if len(context['domain'].split("/")) > 1:
                    context['domain'] = context['domain'].split("/")[2]
                if context['domain'][:4] == "www.":
                    context['domain'] = context['domain'][4:]
                context['kuberid'] = context['domain'].split('.')[0]
                print(context['kuberid'])
                if not usetting.objects.filter(user=request.user):
                    context['edit_setting'] = 1
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
