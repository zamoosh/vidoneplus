from unidecode import unidecode

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    cellphone = models.CharField(max_length=15, unique=True)
    organization_name = models.CharField(max_length=15, unique=True)
    educational_interface_name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    dateofestablishment = models.DateTimeField()

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
    org_colore = models.IntegerField()
    sub_colore = models.IntegerField()
    app_name = models.CharField(max_length=250)


class CourseVitrin(models.Model):
    name = models.CharField(max_length=500)
    status = models.BooleanField(default=False)


class Status(models.Model):
    status = models.BooleanField(default=False)
    duration = models.IntegerField()


class Admin(models.Model):
    organization_name = models.CharField(max_length=15)
    organization_satatus = models.BooleanField(default=False)
    date_of_start = models.DateTimeField()
    date_of_finish = models.DateTimeField()


class ViewInformation(models.Model):
    cellphone = models.CharField(max_length=15, unique=True)
    organization_name = models.CharField(max_length=15, unique=True)
    educational_interface_name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    dateofestablishment = models.DateTimeField()
