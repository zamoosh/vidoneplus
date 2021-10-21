from .imports import *
from ..models import Setting


@login_required
def settings(request):
    context = {}
    if request.method == "POST":
        context = {}
        context['user'] = request.user
        context['org_colore'] = request.POST.get('forg_colore', '').strip()
        context['sub_colore'] = request.POST.get('sub_colore', '').strip()
        context['app_name'] = request.POST.get('app_name', '').strip()
        if not User.objects.filter(id=request.user.id):
            seeting = Setting()
            seeting.user = context['user']
            seeting.org_colore = context['org_colore']
            seeting.sub_colore = context['sub_colore']
            seeting.app_name = context['app_name']
            seeting.save()
            context['result'] = "تنظیمات با موفقیت ثبت شد."
        else:
            setting = Setting.objects.get(id=request.user.id)
            setting.org_colore = context['org_colore']
            setting.sub_colore = context['sub_colore']
            setting.app_name = context['app_name']
            setting.save()
    context['setting_all'] = Setting.objects.filter(user=request.user)
    return render(request, "client/setting.html", context)
