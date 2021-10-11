from .imports import *

def user(request):
    # perms_list = ('client.add_user', 'client.change_user', 'client.delete_user')
    context = {}
    # if request.user.has_perms(perms_list):
    #     # GET METHOD
    #     if request.method == "GET":
    #         q = Q()
    #         if 'id' in request.GET:
    #             q = q & Q(id=int(request.GET['id']))
    #         context['users'] = UserSerializer(User.objects.filter(q), many=True).data
    #         status_code = HTTP_200_OK
    #     # POST METHOD
    #     elif request.method == "POST":
    #         is_mobile_number = re.compile("^09?\d{9}$", re.IGNORECASE)
    #         if User.objects.filter(username=request.data.get('username')):
    #             context['msg'] = 'این نام کاربری وجود دارد.'
    #             status_code = HTTP_400_BAD_REQUEST
    #         if request.data.get('cellphone', None):
    #             if is_mobile_number.match(request.data.get('cellphone')):
    #                 if User.objects.filter(cellphone=request.data.get('cellphone')):
    #                     context['msg'] = 'این شماره تماس وجود دارد.'
    #                     status_code = HTTP_400_BAD_REQUEST
    #             else:
    #                 context['msg'] = 'شماره تماس صحیح نیست.'
    #                 status_code = HTTP_400_BAD_REQUEST
    #         if request.data.get('email', None):
    #             if '@' in request.data.get('email', None):
    #                 if User.objects.filter(email=request.data.get('email')):
    #                     context['msg'] = 'این ایمیل وجود دارد.'
    #                     status_code = HTTP_400_BAD_REQUEST
    #             else:
    #                 context['msg'] = 'ایمیل صحیح نیست.'
    #                 status_code = HTTP_400_BAD_REQUEST
    #         if not request.data.get('email', None) and not request.data.get('cellphone', None):
    #             context['msg'] = 'شماره تماس یا ایمیل وارد نشده است.'
    #             status_code = HTTP_400_BAD_REQUEST
    #         if 'msg' not in context:
    #             user = User.objects.create(**request.data)
    #             user.set_password(request.data.get('password'))
    #             user.save()
    #             status_code = HTTP_201_CREATED
    #             context['users'] = UserSerializer(user).data
    #     # PUT METHOD
    #     elif request.method == "PUT":
    #         try:
    #             q = Q(id=int(request.data.get('id')))
    #             user = User.objects.get(q)
    #             if request.data.get('username', None):
    #                 if User.objects.filter(username=request.data.get('username')) and user.username != request.data.get(
    #                         'username'):
    #                     context['msg'] = 'این نام کاربری وجود دارد.'
    #                     status_code = HTTP_400_BAD_REQUEST
    #             # CHECK EMAIL VALIDATION AND NOT DUPLICATED
    #             if request.data.get('email', None):
    #                 if '@' in request.data.get('email'):
    #                     if user.email != request.data.get('email', None):
    #                         if User.objects.filter(email=request.data.get('email')).exists():
    #                             context['msg'] = "این ایمیل قبلا در سیستم ثبت شده است."
    #                 else:
    #                     context['msg'] = "این ایمیل صحیح نیست."
    #             # CHECK CELLPHONE VALIDATION AND NOT DUPLICATED
    #             is_mobile_number = re.compile("^09?\d{9}$", re.IGNORECASE)
    #             if request.data.get('cellphone', None):
    #                 if is_mobile_number.match(request.data.get('cellphone')):
    #                     if user.cellphone != request.data.get('cellphone', None):
    #                         if User.objects.filter(cellphone=request.data.get('cellphone')).exists():
    #                             context['msg'] = "این شماره موبایل قبلا در سیستم ثبت شده است."
    #                 else:
    #                     context['msg'] = "این شماره موبایل صحیح نیست."
    #             if 'msg' in context:
    #                 status_code = HTTP_400_BAD_REQUEST
    #             else:
    #                 user = User.objects.filter(q)
    #                 user.update(**request.data)
    #                 if request.data.get('password', None):
    #                     user[0].set_password(request.data.get('password'))
    #                     user.save()
    #                 context['msg'] = 'کاربر با موفقیت به روز شد.'
    #                 context['users'] = UserSerializer(user[0], many=False).data
    #                 status_code = HTTP_200_OK
    #         except:
    #             context['msg'] = 'این کاربر وجود ندارد.'
    #             status_code = HTTP_404_NOT_FOUND
    #     else:
    #         context['msg'] = 'method not allowed.'
    #         status_code = HTTP_405_METHOD_NOT_ALLOWED
    # else:
    #     context['msg'] = 'شما به این قسمت دسترسی ندارید.'
    #     status_code = HTTP_403_FORBIDDEN
    return JsonResponse(context, status=200)
