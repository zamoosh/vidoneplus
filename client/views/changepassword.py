from .imports import *

@login_required
def changepassword(request):
    context = {}
    if request.method == "POST":
        if not request.POST.get("newpassword", None) or not request.POST.get("password", None):
            context['error'] = "گذرواژه صحیح نیست."
        elif not authenticate(username=request.user.username, password=request.POST.get("password", None)):
            context['error'] = "گذرواژه صحیح نیست."
        elif pwStrength(request.POST.get("newpassword", "")) <= 60:
            context['error'] = "گذر واژه ی جدید آسان می باشد."
        else:
            user = request.user
            user.set_password(request.POST["newpassword"])
            user.save()
            context['result'] = "گذر واژه با موفقیت تغییر کرد."
            
    return render(request, "client/profile_change_password.html", context)