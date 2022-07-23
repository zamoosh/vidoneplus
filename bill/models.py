from django.db import models
from order.models import OrderItem


class Bill(models.Model):
    order_item = models.OneToOneField(OrderItem, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    pay_date = models.DateTimeField(null=True)
