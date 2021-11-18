from django.db import models
from PIL import Image
from django.contrib.auth import get_user_model

User = get_user_model()


def teacher_image(instance, filename):
    return "%s/%s/%s" % ('teacher', instance.id, filename)


def banner_image(instance, filename):
    return "%s/%s/%s" % ('banner', instance.id, filename)


def course_image(instance, filename):
    return "%s/%s/%s" % ('course', instance.id, filename)


def zone_image(instance, filename):
    return "%s/%s/%s" % ('zone', instance.id, filename)


class Teacher(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(blank=True, null=True, upload_to=teacher_image)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    extra = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        super(Teacher, self).save()
        # if self.image:
        #     img = Image.open(self.image)
        #     img.save(self.image.path, quality=95)

    def get_alias(self):
        alias = self.name.replace(" ", "-")
        while '--' in alias:
            alias = alias.replace("--", '-')
        return alias

    def get_old_image(self):
        return 'https://cdn1.vidone.ir/scale/143x143/media/teachers/%s/%s' % (self.id, self.image)


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    subdescription = models.TextField()
    price = models.BigIntegerField()
    price_with_discount = models.BigIntegerField(default=0)
    image = models.ImageField(blank=True, null=True, upload_to=course_image)
    video = models.FileField()
    teacher = models.ManyToManyField(Teacher)
    extra = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    free_course = models.BooleanField(default=False)
    lesson_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.price == 0:
            self.free_course = True
        if 'appstatus' not in self.extra:
            self.extra['appstatus'] = False
        if 'sitestatus' not in self.extra:
            self.extra['sitestatus'] = False
        if 'status' not in self.extra:
            self.extra['status'] = False
        if 'hastest' not in self.extra:
            self.extra['hastest'] = False
        if 'powerd' not in self.extra:
            self.extra['powerd'] = ''
        if 'is_intruduction' not in self.extra:
            self.extra['is_intruduction'] = False
        if 'stream' not in self.extra:
            self.extra['stream'] = False
        if 'private' not in self.extra:
            self.extra['private'] = False
        if 'duration' not in self.extra:
            self.extra['duration'] = 0
        if self.price <= self.price_with_discount:
            self.price_with_discount = 0
        super(Course, self).save()
        # if self.image:
        #     # img = Image.open(self.image)
        #     # img.save(self.image.path, quality=95)

    def delete(self, *args, **kwargs):
        Vote.objects.filter(type="3", pid=self.id).delete()
        Note.objects.filter(type=1, pid=self.id).delete()
        BookMarkObjacts.objects.filter(type=1, pid=self.id).delete()
        super(Course, self).delete(*args, **kwargs)

    def get_file_number(self):
        return len(Lesson_file.objects.filter(lesson__in=Lesson.objects.filter(course=self)))

    def get_lesson_number(self):
        return len(Lesson.objects.filter(course=self))

    def get_price(self):
        if self.price_with_discount:
            return self.price_with_discount
        return self.price

    def get_alias(self):
        alias = self.title.replace(" ", "-")
        while '--' in alias:
            alias = alias.replace("--", '-')
        return alias


class Banner(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(blank=True, null=True, upload_to=banner_image)
    image_app = models.ImageField(blank=True, null=True, upload_to=banner_image)
    description = models.TextField(null=True, blank=True)
    link = models.URLField()
    status = models.BooleanField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    banner_place = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        super(Banner, self).save()
        # if self.image:
        #     img = Image.open(self.image)
        #     img.save(self.image.path, quality=95)
        # if self.image_app:
        #     img = Image.open(self.image_app)
        #     img.save(self.image_app.path, quality=95)


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    order_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(Lesson, self).save()


class Lesson_file(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='media', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    media_file = models.FileField()
    duration = models.CharField(max_length=10)
    size = models.FloatField(default=0)
    order_id = models.IntegerField(default=0)
    MEDIA_TYPE = (
        (1, 'file'),
        (2, 'video'),
        (3, 'audio'),
    )
    media_type = models.IntegerField(choices=MEDIA_TYPE)
    free_lesson = models.BooleanField(default=False)
    stream_name = models.CharField(null=True, blank=True, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(Lesson_file, self).save()


class Main_Type(models.Model):
    title = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        super(Main_Type, self).save()


class Type(models.Model):
    title = models.CharField(max_length=200)
    logo = models.ImageField(blank=True, null=True, upload_to=zone_image)
    count = models.IntegerField(null=True, blank=True)
    order_id = models.IntegerField(default=0)
    menu = models.BooleanField(default=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    main_type = models.ForeignKey(Main_Type, on_delete=models.CASCADE)

    def get_course_list(self):
        return Course.objects.filter(
            id__in=Type_course.objects.values_list('course', flat=True).filter(type=self).order_by("-order_id"))

    def get_alias(self):
        alias = self.title.replace(" ", "-")
        while '--' in alias:
            alias = alias.replace("--", '-')
        return alias

    def save(self, *args, **kwargs):
        super(Type, self).save()
        # if self.logo:
        #     img = Image.open(self.logo)
        #     img.save(self.logo.path, quality=95)


class Type_course(models.Model):
    order_id = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Type_course, self).save()


class Vote(models.Model):
    VOTE_TYPE = [
        (1, 'teacher'),
        (2, 'lp'),
        (3, 'course'),
    ]
    type = models.IntegerField(choices=VOTE_TYPE, default=3)
    rate = models.FloatField(default=0)
    count = models.IntegerField(default=0)
    pid = models.IntegerField()
    sum = models.IntegerField(default=0)

    class Meta:
        unique_together = ('type', 'pid',)

    def save(self, *args, **kwargs):
        self.rate = round(self.rate, 2)
        super(Vote, self).save()


class Vote_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    NOTE_TYPE = [
        (1, 'course'),
        (2, 'lesson'),
        (3, 'lesso_file'),
    ]
    type = models.IntegerField(choices=NOTE_TYPE, default=3)
    note = models.TextField()
    pid = models.IntegerField()

    class Meta:
        unique_together = ('type', 'pid', 'user')


class BookMarkList(models.Model):
    list_name = models.CharField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class BookMarkObjacts(models.Model):
    bookmarklist = models.ForeignKey(BookMarkList, on_delete=models.CASCADE)
    pid = models.IntegerField()
    BOOK_TYPE = [
        (1, 'course'),
        (2, 'lesson'),
        (3, 'lesso_file'),
    ]
    type = models.IntegerField(choices=BOOK_TYPE, default=3)

    class Meta:
        unique_together = ('type', 'pid', 'bookmarklist')


class CourseUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)