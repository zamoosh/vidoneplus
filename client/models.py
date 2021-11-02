from unidecode import unidecode

from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


def user_image(instance, filename):
    return "%s/%s/%s" % ('setting', instance.user.id, filename)


class User(AbstractUser):
    cellphone = models.CharField(max_length=15, unique=True)
    organization_name = models.CharField(max_length=15, unique=True)
    educational_interface_name = models.CharField(max_length=200, unique=True, null=True)
    description = models.TextField()
    dateofestablishment = models.DateField(null=True)

    def save(self, *args, **kwargs):
        self.cellphone = unidecode(self.cellphone)
        self.username = self.cellphone
        super(User, self).save()


class Setting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    org_colore = models.CharField(max_length=50)
    sub_colore = models.CharField(max_length=50)
    app_name = models.CharField(max_length=250)
    domain = models.CharField(max_length=50)
    kuberid = models.CharField(max_length=250, null=True)
    site_name = models.CharField(max_length=250, null=True)
    admin_name = models.CharField(max_length=250, null=True)
    pwa_name = models.CharField(max_length=250, null=True)
    fullname = models.CharField(max_length=250, null=True)
    contact_phone = models.CharField(max_length=250)
    download_link = models.CharField(max_length=500)
    company_logo = models.ImageField(upload_to=user_image)
    splashscreen = models.ImageField(upload_to=user_image)
    image_tag = models.CharField(max_length=20, null=True)


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


class Imagetag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currenttag = models.CharField(null=True, max_length=20)
    releasetag = models.CharField(null=True, max_length=20)
