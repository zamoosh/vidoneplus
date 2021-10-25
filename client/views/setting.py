from .imports import *
from ..models import Setting


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
            if not Setting.objects.filter(user=request.user):
                context['edit_setting'] = 1
                seeting = Setting()
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
                    setting = Setting.objects.get(id=request.user.id)
                    setting.org_colore = context['org_colore']
                    setting.sub_colore = context['sub_colore']
                    setting.app_name = context['app_name']
                    setting.domain = context['domain']
                    setting.save()
                    context['result'] = "تنظیمات با موفقیت تغییر کرد."
                except:
                    context['error'] = "خطا در ثبت اطلاعات"
        return render(request, "client/edit-setting.html", context)
    context['settings'] = Setting.objects.filter(user=request.user)
    if not Setting.objects.filter(user=request.user):
        context['edit_setting'] = 0
    return render(request, "client/setting.html", context)
