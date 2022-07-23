from django.db import models
import datetime


def order_image(instance, filename):
    return "%s/%s/%s" % ('order', instance.id, filename)


class Order(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    period = models.IntegerField()
    status = models.BooleanField(default=True)
    image = models.ImageField(upload_to=order_image)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    setting = models.ForeignKey('client.Setting', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField()
    status = models.BooleanField(default=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.ended_at = datetime.datetime.now() + datetime.timedelta(days=self.order.period * 31)
        return super(OrderItem, self).save()
