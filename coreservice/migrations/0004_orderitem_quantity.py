# Generated by Django 4.0.3 on 2022-08-23 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreservice', '0003_alter_order_options_alter_vehicles_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
