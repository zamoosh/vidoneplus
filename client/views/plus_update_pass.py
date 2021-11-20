import json

from django.views.decorators.csrf import csrf_exempt

from client.views.imports import *
from client.models import *
from course.models import *
from django.core import serializers
import requests
from .imports import *


@csrf_exempt
def plus_update_pass(request):
    context = {}
    context['status'] = False
    print(json.loads(request.body))
    body = json.loads(json.loads(request.body))[0]
    pw = PasswordGenerator.objects.get(id=body['pk'])
    if pw.username == body['fields']['username'] and pw.setting_id == body['fields']['setting'] and pw.password == \
            body['fields']['password']:
        context['status'] = True
        pw.delete()
    return JsonResponse(context)
