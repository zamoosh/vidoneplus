# Generated by Django 3.2.8 on 2021-11-09 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0015_status_active_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='status',
            old_name='status',
            new_name='site_created',
        ),
    ]
