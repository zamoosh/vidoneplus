# Generated by Django 4.0.4 on 2022-06-08 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, unique=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tag.tag')),
            ],
        ),
        migrations.CreateModel(
            name='Tag_use',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField()),
                ('tag_type', models.IntegerField(choices=[(1, 'teacher'), (2, 'lp'), (3, 'course')])),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tag.tag')),
            ],
            options={
                'unique_together': {('uid', 'tag_type', 'tag')},
            },
        ),
    ]
