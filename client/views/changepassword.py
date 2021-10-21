from .imports import *

@login_required
def changepassword(request):
    context = {}
    if request.method == "POST":
        if request.POST.get("newpassword", None) and request.POST.get("password", None):
            if authenticate(username=request.user.username, password=request.POST.get("password", None)):
                if pwStrength(request.POST.get("newpassword", "")) > 60:
                    user = request.user
                    user.set_password(request.POST["newpassword"])
                    user.save()
                    context['result'] = "گذر واژه با موفقیت تغییر کرد."
                else:
                    context['error'] = "گذر واژه ی جدید آسان می باشد."
            else:
                context['error'] = "گذرواژه صحیح نیست."
        else:
            context['error'] = "گذرواژه صحیح نیست."
    return render(request, "client/profile_change_password.html", context)