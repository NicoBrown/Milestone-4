# Generated by Django 3.2.16 on 2023-01-26 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20230117_2020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='default_country',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='default_phone_number',
            field=models.IntegerField(blank=True, max_length=100, null=True),
        ),
    ]
