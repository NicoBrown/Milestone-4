# Generated by Django 3.2.16 on 2023-01-07 23:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_userprofile_stripe_customer_id'),
        ('expenses', '0002_auto_20221231_1453'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='data',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='expense',
            old_name='amount',
            new_name='paid_amount',
        ),
        migrations.RenameField(
            model_name='expense',
            old_name='sku',
            new_name='supplier_address',
        ),
        migrations.RenameField(
            model_name='expense',
            old_name='unit_price',
            new_name='tip_amount',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='description',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='image',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='quantity',
        ),
        migrations.AddField(
            model_name='expense',
            name='line_item_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='expense',
            name='order_number',
            field=models.CharField(default='', editable=False, max_length=32),
        ),
        migrations.AddField(
            model_name='expense',
            name='supplier_phone',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='expense',
            name='user_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expense', to='profiles.userprofile'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='supplier_name',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.CreateModel(
            name='OrderLineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=1, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('tax_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('tip_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('lineitem_total', models.DecimalField(decimal_places=2, max_digits=6)),
                ('is_paid', models.BooleanField(default=False)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineitems', to='expenses.expense')),
                ('user_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='profiles.userprofile')),
            ],
        ),
    ]
