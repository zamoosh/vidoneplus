from suds.client import Client
from django.conf import settings

class Zarinpal:
    def __init__(self, amount, CallbackURL):
        self.zarinpal_url = 'https://www.zarinpal.com/pg'
        self.amount = amount
        self.ZARINPAL_WEBSERVICE = self.zarinpal_url + '/services/WebGate/wsdl'
        self.MMERCHANT_ID = settings.MMERCHANT_ID_ZARINPAL
        self.description = u'خرید فایل های استاتیک'  # Required
        self.email = ''  # Optional
        self.mobile = ''  # Optional
        self.CallbackURL = CallbackURL

    def create_transaction(self):
        client = Client(self.ZARINPAL_WEBSERVICE)
        result = client.service.PaymentRequest(self.MMERCHANT_ID, self.amount, self.description, self.email, self.mobile, self.CallbackURL)
        if result.Status == 100:
            self.Authority = result.Authority
            return self.zarinpal_url + '/StartPay/' + result.Authority
        else:
            return False

    def status_transaction(self, authority):
        client = Client(self.ZARINPAL_WEBSERVICE)
        result = client.service.PaymentVerification(self.MMERCHANT_ID, authority, self.amount)
        if result.Status == 100:
            return True
        elif result.Status == 101:
            return True
        else:
            return False
