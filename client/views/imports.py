from django.core.mail import send_mail
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import render
import re
from django.core.validators import validate_email
from django import forms
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.conf import settings
from django.http.response import HttpResponseRedirect
import datetime

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import *

from client.dto import *
from client.serializers import *
from client.models import *


def error_handler(lang, status, exist):
    if lang and lang == 'en':
        if status == 200:
            return {'msg': 'Operation successfully done.'}
        elif status == 429:
            return {'msg': 'Operation successfully done with some limits because of your package type.'}
        elif status == 400:
            return {'msg': 'Operation failed because of your package type.'}
        elif exist and exist is True:
            return {'msg': 'This item exist'}
        else:
            return {'msg': 'Operation failed.'}

    else:
        if status == 200:
            return {'msg': 'عملیات با موفقیت انجام شد'}
        elif status == 429:
            return {'msg': 'عملیات به علت محدودیت بسته خریداری شده شما با محدودیت انجام شد'}
        elif status == 400:
            return {'msg': 'پکیج خریداری شده توسط شما امکان انجام این فعالیت را ندارد'}
        elif exist and exist is True:
            return {'msg': 'این آیتم از قبل ذخیره گردیده است'}
        else:
            return {'msg': 'در انجام عملیات خطایی رخ داده است'}


def send_mail_func(message, email_address):
    status = send_mail(
        "درخواست فعال سازی حساب کاربری {title}".format(title="ویدان"),
        str(message),
        'app@vidone.org',
        [email_address],
        # fail_silently=False,
    )
    print(status)
