import requests
from django.conf import settings
import json


class Smsir:
    _base_url = "https://restfulsms.com/api/"

    def __init__(self):
        self.api_key = settings.SMSIR_APIKEY
        self.secret_key = settings.SMSIR_SECRETKEY
        self.lineNumber = settings.SMSIR_NUMBER
        self.gettoken()

    def gettoken(self):
        headers = {
            'content-type': 'application/json',
        }
        data = {}
        data['UserApiKey'] = self.api_key
        data['SecretKey'] = self.secret_key
        response = requests.post(self._base_url + "Token", data=json.dumps(data), headers=headers)
        self.token_key = response.json()["TokenKey"]

    def sendsms(self, message=[], mobileNumbers=[]):
        headers = {
            'content-type': 'application/json',
            'x-sms-ir-secure-token': self.token_key,
        }
        data = {"Messages": message, "MobileNumbers": mobileNumbers, "LineNumber": self.lineNumber,
                "SendDateTime": "",
                "CanContinueInCaseOfError": "false"}
        response = requests.post(self._base_url + "MessageSend", headers=headers, data=json.dumps(data))
        return response.json()

    def sendwithtemplate(self, params, mobile, tempId):
        #sendwithtemplate({'verificationCode':'1234'},"09120773485",1387) vidone verification code
        headers = {
            'content-type': 'application/json',
            'x-sms-ir-secure-token': self.token_key,
        }
        data = {}
        data['ParameterArray'] = []
        for i in params.items():
            data['ParameterArray'].append({"Parameter": i[0], "ParameterValue": i[1]})
        data['Mobile'] = mobile
        data['TemplateId'] = tempId
        response = requests.post(self._base_url + "UltraFastSend", headers=headers, data=json.dumps(data))
        return response.json()
