# Generated by Django 2.0.3 on 2018-09-30 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20180930_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='regularpizza',
            name='toppings',
            field=models.ManyToManyField(blank=True, null=True, related_name='reg_dish', to='orders.Topping'),
        ),
        migrations.AddField(
            model_name='sicilianpizza',
            name='toppings',
            field=models.ManyToManyField(blank=True, related_name='sic_dish', to='orders.Topping'),
        ),
    ]
