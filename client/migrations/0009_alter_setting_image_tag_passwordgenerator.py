# Generated by Django 4.0.4 on 2022-05-23 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0008_alter_setting_image_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='image_tag',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='client.imagetag'),
        ),
        migrations.CreateModel(
            name='PasswordGenerator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('setting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.setting')),
            ],
        ),
    ]