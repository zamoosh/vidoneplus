import datetime
import jdatetime
from unidecode import unidecode
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import login


def user_image(instance, filename):
    return "%s/%s/%s" % ('setting', instance.owner.id, filename)


class User(AbstractUser):
    cellphone = models.CharField(max_length=15, unique=True)
    organization_name = models.CharField(max_length=15)
    educational_interface_name = models.CharField(max_length=200)
    description = models.TextField()
    dateofestablishment = models.DateField(null=True)
    extra = models.JSONField(default=dict)

    @staticmethod
    def get_user(username):
        user = User.objects.filter(Q(cellphone=username) | Q(email=username) | Q(username=username)).first()
        if user:
            return user
        return User()

    def save(self, *args, **kwargs):
        self.cellphone = unidecode(self.cellphone)
        self.username = self.cellphone
        super(User, self).save()

    def sendsms(self):
        if not self.cellphone:
            return False
        code = self.create_verificationcode()
        try:
            from library.smsir import Smsir
            sms = Smsir()
            sms.sendwithtemplate({'verificationCode': code}, self.cellphone, 55907)
        except (Exception, Exception):
            print('احتمالا اعتبار سامانه‌ی پیامکی تمام شده است!')
        print(code)

    def login(self, request):
        if self.is_active:
            login(request, self)
            return True
        return False

    def check_code(self, request, code):
        status = False
        if self.get_verificationcode() == code:
            status = self.login(request)
            VerificationCode.objects.filter(name=self.username).delete()
        return status

    def create_verificationcode(self):
        self.username = unidecode(self.username)
        VerificationCode.objects.filter(name=self.username).delete()
        vc = VerificationCode(name=self.username)
        vc.save()
        return str(vc.code)

    def get_verificationcode(self):
        VerificationCode.objects.filter(name=self.username, trying__gte=5).delete()
        try:
            vc = VerificationCode.objects.get(name=self.username)
            vc.trying += 1
            vc.save()
            return str(vc.code)
        except (VerificationCode.DoesNotExist, Exception):
            pass
        return None

    @staticmethod
    def check_phone_validate(self):
        prev_numbers = [
            '+93', '+355', '+213', '+1684', '+376', '+244', '+1264', '+1268', '+54', '+374', '+297',
            '+61', '+43', '+994', '+1242', '+973', '+880', '+1246', '+375', '+32', '+501', '+229',
            '+1441', '+975', '+591', '+599', '+387', '+267', '+55', '+1284', '+673', '+359', '+226',
            '+257', '+855', '+237', '+1', '+238', '+1345', '+236', '+235', '+56', '+86', '+57', '+269',
            '+243', '+242', '+682', '+506', '+225', '+385', '+53', '+599', '+357', '+420', '+45', '+246',
            '+253', '+1767', '+1809', '+1829', '+1849', '+593', '+20', '+503', '+240', '+291', '+372',
            '+268', '+251', '+500', '+298', '+679', '+358', '+33', '+594', '+689', '+241', '+220', '+995',
            '+49', '+233', '+350', '+30', '+299', '+1473', '+590', '+1671', '+502', '+224', '+245',
            '+592', '+509', '+504', '+852', '+36', '+354', '+91', '+62', '+98', '+964', '+353', '+972',
            '+39', '+1876', '+81', '+962', '+7', '+254', '+686', '+383', '+965', '+996', '+856', '+371',
            '+961', '+266', '+231', '+218', '+423', '+370', '+352', '+853', '+261', '+265', '+60', '+960',
            '+223', '+356', '+692', '+596', '+222', '+230', '+52', '+691', '+373', '+377', '+976', '+382',
            '+1664', '+212', '+258', '+95', '+264', '+674', '+977', '+31', '+687', '+64', '+505', '+227',
            '+234', '+683', '+672', '+850', '+389', '+1670', '+47', '+968', '+92', '+680', '+970', '+507',
            '+675', '+595', '+51', '+63', '+48', '+351', '+1787', '+1939', '+974', '+262', '+40', '+7',
            '+250', '+247', '+290', '+1869', '+1758', '+508', '+1784', '+685', '+378', '+239', '+966',
            '+221', '+381', '+248', '+232', '+65', '+1721', '+421', '+386', '+677', '+252', '+27', '+82',
            '+211', '+34', '+94', '+249', '+597', '+46', '+41', '+963', '+886', '+992', '+255', '+66',
            '+670', '+228', '+690', '+676', '+1868', '+216', '+90', '+993', '+1649', '+688', '+256',
            '+380', '+971', '+44', '+598', '+1340', '+1', '+998', '+678', '+58', '+84', '+681', '+967',
            '+260', '+263'
        ]
        if self.cellphone:
            prev = self.cellphone[:-10]
            if prev in prev_numbers:
                return True
        return False

    def get_status(self):
        return self.status

    @staticmethod
    def not_empty(request, request_method, *args):
        if request_method == 'POST':
            for input_name in args:
                if not request.POST.get(input_name):
                    return False
        else:
            for input_name in args:
                if not request.GET.get(input_name):
                    return False
        return True

    @staticmethod
    def str_to_date(string_date):
        d = datetime.datetime.strptime(string_date, '%Y/%m/%d').date()
        return jdatetime.date(d.year, d.month, d.day).togregorian()


class VerificationCode(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.IntegerField()
    trying = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        import random
        if not self.code:
            self.code = random.randint(1000, 9999)
        super(VerificationCode, self).save()


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
    image_tag = models.ForeignKey(Imagetag, on_delete=models.CASCADE, null=True)
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

class PasswordGenerator(models.Model):
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
