from unidecode import unidecode
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


def user_image(instance, filename):
    return "%s/%s/%s" % ('setting', instance.owner.id, filename)


class User(AbstractUser):
    cellphone = models.CharField(max_length=15, unique=True)
    organization_name = models.CharField(max_length=15)
    educational_interface_name = models.CharField(max_length=200)
    description = models.TextField()
    dateofestablishment = models.DateField(null=True)

    def save(self, *args, **kwargs):
        self.cellphone = unidecode(self.cellphone)
        self.username = self.cellphone
        super(User, self).save()


class Imagetag(models.Model):
    status = models.BooleanField(default=True)
    forceupdate = models.BooleanField(default=False)
    pwa_version = models.CharField(max_length=20)
    pwa_description = models.CharField(max_length=200)
    admin_version = models.CharField(max_length=20)
    admin_description = models.CharField(max_length=200)
    site_version = models.CharField(max_length=20)
    site_description = models.CharField(max_length=200)
    android_version = models.CharField(max_length=20)
    android_description = models.CharField(max_length=200)
    ios_version = models.CharField(max_length=20)
    ios_description = models.CharField(max_length=200)


class Setting(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    org_color = models.CharField(max_length=50)
    sub_color = models.CharField(max_length=50)
    app_name = models.CharField(max_length=250)
    domain = models.CharField(max_length=50)
    kuberid = models.CharField(max_length=250, null=True, blank=True)
    site_name = models.CharField(max_length=250, null=True, blank=True)
    admin_name = models.CharField(max_length=250, null=True, blank=True)
    pwa_name = models.CharField(max_length=250, null=True, blank=True)
    fullname = models.CharField(max_length=250, null=True, blank=True)
    contact_phone = models.CharField(max_length=250)
    download_link = models.CharField(max_length=500)
    company_logo = models.ImageField(upload_to=user_image)
    splashscreen = models.ImageField(upload_to=user_image)
    image_tag = models.ForeignKey(Imagetag, on_delete=models.CASCADE, default=1)
    instagram = models.CharField(max_length=50, null=True, blank=True)
    aparat = models.CharField(max_length=50, null=True, blank=True)
    facebook = models.CharField(max_length=50, null=True, blank=True)
    twitter = models.CharField(max_length=70, null=True, blank=True)
    youtube = models.CharField(max_length=70, null=True, blank=True)
    favicon = models.ImageField(upload_to=user_image)
    short_title = models.CharField(max_length=50, null=True, blank=True)
    slogan = models.CharField(max_length=50, null=True, blank=True)
    zarinpal = models.CharField(max_length=50, null=True, blank=True)
    smsir_key = models.CharField(max_length=50, null=True, blank=True)

    def get_splashscreen(self):
        return self.splashscreen.path.split('/')[-1]

    def get_company_logo(self):
        return self.company_logo.path.split('/')[-1]

    def get_favicon(self):
        return self.favicon.path.split('/')[-1]


# class CourseVitrin(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     price = models.BigIntegerField()
#     price_with_discount = models.BigIntegerField(default=0)
#     teacher = models.CharField(max_length=200)
#     lesson_count = models.IntegerField(default=0)
#
#     def save(self, *args, **kwargs):
#         super(CourseVitrin, self).save()
#
#     def buyed(self, user):
#         try:
#             CourseUser.objects.get(course=self, user=user)
#             return True
#         except:
#             return False


class Status(models.Model):
    active_user = models.BooleanField(default=False)
    site_created = models.BooleanField(default=False)
    duration = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

# class CourseUser(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     status = models.BooleanField(default=False)
