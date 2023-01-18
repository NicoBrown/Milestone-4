# Generated by Django 3.2.16 on 2023-01-17 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_rename_stripe_requirements_true_userprofile_stripe_requirements_due'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='default_phone_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='stripe_customer_id',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]