# Generated by Django 3.2.16 on 2023-01-23 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0013_auto_20230123_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlineitem',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='orderlineitem',
            name='quantity',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='orderlineitem',
            name='tax_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]
