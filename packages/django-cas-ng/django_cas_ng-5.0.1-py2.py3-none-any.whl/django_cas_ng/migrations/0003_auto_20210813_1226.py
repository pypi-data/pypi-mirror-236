# Generated by Django 3.1.13 on 2021-08-13 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_cas_ng', '0002_auto_20201023_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessionticket',
            name='ticket',
            field=models.CharField(max_length=1024),
        ),
    ]
