from django.core import serializers

from .imports import *
from django.http import JsonResponse, HttpResponse
from ..models import Setting as usetting

@login_required
def settings(request, action=None):
    context = {}
    if action == "edit":
        if request.method == "POST":
            context = {}
            context['user'] = request.user
            context['org_colore'] = request.POST.get('org_colore', '').strip()
            context['sub_colore'] = request.POST.get('sub_colore', '').strip()
            context['app_name'] = request.POST.get('app_name', '').strip()
            context['domain'] = request.POST.get('domain', '').strip()
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
                seeting.kuberid = context['kuberid'] + str(context['user'])[9:]
                seeting.save()
                context['result'] = "تنظیمات با موفقیت ثبت شد."
            else:
                try:
                    setting = usetting.objects.get(id=request.user.id)
                    setting.org_colore = context['org_colore']
                    setting.sub_colore = context['sub_colore']
                    setting.app_name = context['app_name']
                    setting.domain = context['domain']
                    setting.save()
                    context['result'] = "تنظیمات با موفقیت تغییر کرد."
                except:
                    context['error'] = "خطا در ثبت اطلاعات"
        return render(request, "client/edit-setting.html", context)
    context['settings'] = usetting.objects.filter(user=request.user)
    if not usetting.objects.filter(user=request.user):
        context['edit_setting'] = 0
    return render(request, "client/setting.html", context)


def configs(request, domain):
    context = {}
    config = usetting.objects.get(domain=domain)
    context['domain'] = config.domain
    context['org_colore'] = config.org_colore
    context['sub_colore'] = config.sub_colore
    context['app_name'] = config.app_name
    context['site_name'] = config.site_name
    context['admin_name'] = config.admin_name
    context['pwa_name'] = config.pwa_name
    context['fullname'] = config.fullname
    return JsonResponse(context)