# Generated by Django 3.2.16 on 2023-01-08 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0005_auto_20230108_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='net_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]
