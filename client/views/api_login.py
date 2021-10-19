# from rest_framework_simplejwt.tokens import RefreshToken
# from .imports import *
# from unidecode import unidecode
#
#
# @swagger_auto_schema(method='POST', request_body=TokenCreateDto, responses={200: TokenViewDto(many=False)})
# @api_view(['POST'])
# @permission_classes((AllowAny,))
# def login(request):
#     context = {}
#     username = unidecode(request.data.get('username'))
#     is_mobile_number = re.compile("^09?\d{9}$", re.IGNORECASE)
#
#     if request.data.get('code', None):
#         verify_token = VerificationCode.objects.filter(code=request.data.get('code'), name=request.data.get('username'))
#         if len(verify_token) > 0:
#             q = Q(cellphone=request.data.get('username')) | Q(email=request.data.get('username'))
#             user = User.objects.get(q)
#     elif request.data.get('password', None):
#         if is_mobile_number.match(username):
#             username = User.objects.get(cellphone=request.data.get('username')).username
#         else:
#             username = User.objects.get(email=request.data.get('username')).username
#         user = authenticate(username=username, password=request.data.get('password', None))
#     if user:
#         refresh = RefreshToken.for_user(user)
#         context['access'] = str(refresh.access_token)
#         context['refresh'] = str(refresh)
#         context['msg'] = "ورود با موفقیت انجام شد"
#         context.update(UserSerializer(user).data)
#         status_code = HTTP_200_OK
#     else:
#         context['msg'] = 'نام کاربری یا کد ارسال شده اشتباه می باشد'
#         status_code = HTTP_400_BAD_REQUEST
#     return Response(context, status=status_code)
