from django.db import models


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=500, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)


class Tag_use(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    uid = models.IntegerField()
    TAG_TYPE = (
        (1, 'teacher'),
        (2, 'lp'),
        (3, 'course'),
    )
    tag_type = models.IntegerField(choices=TAG_TYPE)

    class Meta:
        unique_together = ('uid', 'tag_type', 'tag')

    def save(self, *args, **kwargs):
        super(Tag_use, self).save()
