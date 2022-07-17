from django.db import models
import datetime


class Order(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    period = models.IntegerField()
    status = models.BooleanField(default=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    owner = models.OneToOneField('client.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField()
    status = models.BooleanField(default=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.ended_at = self.ended_at + datetime.timedelta(days=self.order.period)
        return super(OrderItem, self).save()
