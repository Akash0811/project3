# Generated by Django 2.0.3 on 2018-10-11 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20181011_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regularpizza',
            name='string',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='sicilianpizza',
            name='string',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
