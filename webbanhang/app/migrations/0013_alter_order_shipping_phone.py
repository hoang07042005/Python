# Generated by Django 5.1.1 on 2024-09-15 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_order_shipping_address_order_shipping_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
