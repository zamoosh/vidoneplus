from .imports import *


def Login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(request.GET.get("next", "/"))
    context = {}
    if request.GET.get("next", None):
        context['next'] = request.GET.get("next", None)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # check if id is phone number convert it to username
        pattern = re.compile("^\+989?\d{9}$", re.IGNORECASE)
        if pattern.match(username) is None:
            for items in User.objects.filter(cellphone="+989" + username[2:]):
                username = items.username
        else:
            for items in User.objects.filter(cellphone=username):
                username = items.username
        # Convert Email To username
        try:
            validate_email(username)
            if User.objects.filter(email=username).exists():
                username = User.objects.get(email=username).username
        except forms.ValidationError:
            pass

        user = authenticate(username=username, password=password)
        # request.session['password']=request.POST['password']
        if user is not None:
            # the password verified for the user
            if user.is_active:
                login(request, user)
                if len(request.GET.get("next", "/")) == 0:
                    return HttpResponseRedirect("/")
                return HttpResponseRedirect(request.GET.get("next", "/"))
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")
    return render(request, "client/login.html", context)
