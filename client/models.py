from unidecode import unidecode

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    cellphone = models.CharField(max_length=15, unique=True)
    organization_name = models.CharField(max_length=15, unique=True)
    educational_interface_name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    dateofestablishment = models.DateField(null=True)
    verfication_status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.cellphone = unidecode(self.cellphone)
        self.username = self.cellphone
        super(User, self).save()


class VerificationCode(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.IntegerField()

    def save(self, *args, **kwargs):
        self.name = unidecode(self.name)
        super(VerificationCode, self).save()


class Setting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    org_colore = models.CharField(max_length=50)
    sub_colore = models.CharField(max_length=50)
    app_name = models.CharField(max_length=250)
    domain = models.CharField(max_length=50)
    kuberid = models.CharField(max_length=250)


class CourseVitrin(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.BigIntegerField()
    price_with_discount = models.BigIntegerField(default=0)
    teacher = models.CharField(max_length=200)
    lesson_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super(CourseVitrin, self).save()

    def buyed(self, user):
        try:
            CourseUser.objects.get(course=self, user=user)
            return True
        except:
            return False


class Status(models.Model):
    status = models.BooleanField(default=False)
    duration = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class CourseUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseVitrin, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
