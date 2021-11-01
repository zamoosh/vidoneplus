from .imports import *
import jdatetime

def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    context = {}
    context['error'] = 0
    if request.method == 'POST':
        context['request'] = {}
        context['request']['firstname'] = request.POST.get('firstname', '').strip()
        context['request']['lastname'] = request.POST.get('lastname', '').strip()
        # context['request']['organization_name'] = request.POST.get('organization_name', '').strip().lower()
        # context['request']['educational_interface_name'] = request.POST.get('educational_interface_name', '').strip().lower()
        # context['request']['description'] = request.POST.get('description', '').strip().lower()
        # context['request']['dateofestablishment'] = request.POST.get('dateofestablishment')
        # context['request']['email'] = request.POST.get('email', '').strip().lower()
        context['request']['password'] = request.POST.get('password', '')
        context['request']['confirm_password'] = request.POST.get('confirm_password', '')
        context['request']['password'] = context['request']['confirm_password']
        context['request']['cellphone'] = request.POST.get('cellphone', '').strip()
        # if context['request']['dateofestablishment']:
        #     context['dateofestablishment'] = jdatetime.datetime.strptime(context['request']['dateofestablishment'], "%Y/%m/%d").togregorian()
        # FirstName Checking
        # if recaptcha(request)['success']==False:
        #     context['captcha']=1
        #     context['error']=1
        # if len(context['request']['firstname']) < 3:
        #     context['Firstname'] = 1
        #     context['error'] = 1
        # LastName Checking
        # if len(context['request']['lastname']) < 3:
        #     context['Lastname'] = 1
        #     context['error'] = 1
        # username Checking
        pattern = re.compile("^[a-zA-Z0-9.]{6,}$", re.IGNORECASE)
        # if pattern.match(context['request']['username']) is None:
        #     context['username_length'] = 1
        #     context['error'] = 1
        # else:
        #     if User.objects.filter(username_clear=context['request']['username'].replace(".", "")).exists():
        #         context['username_confilict'] = 1
        #         context['error'] = 1
        # Email Checking
        # try:
        #     validate_email(context['request']['email'])
        #     if User.objects.filter(email=context['request']['email']).exists():
        #         context['email_confilict'] = 1
        # except forms.ValidationError:
        #     context['email'] = 1
        #     context['error'] = 1
        # password Checking
        if context['request']['password']:
            context['Strength'] = pwStrength(context['request']['password'])
            if context['Strength'] < 60:
                context['error'] = 1
        elif context['request']['password'] != request.POST.get('password2', ''):
            context['passconfilict'] = 1
            context['error'] = 1
        else:
            context['error'] = 1
            context['password'] = 1
        # postcode Checking
        pattern = re.compile("^09?\d{9}$", re.IGNORECASE)
        if pattern.match(context['request']['cellphone']):
            context['request']['cellphone'] = "+989" + context['request']['cellphone'][2:]
        if User.objects.filter(cellphone=context['request']['cellphone']).exists():
            context['cellphone_confilict'] = 1
            context['error'] = 1
        # Register New User
        if context['error'] == 0:
            request.session['user'] = context['request']
            # user = User.objects.create_user(context['request']['username'], context['request']['email'], context['request']['password'],cellphone=context['request']['cellphone'],username_clear=context['request']['username'].replace(".",""))
            # user.first_name = context['request']['firstname']
            # user.last_name = context['request']['lastname']
            # user.save()
            return HttpResponseRedirect("/accounts/verify")
    return render(request, "client/signup.html", context)
