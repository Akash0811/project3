# Generated by Django 2.0.3 on 2018-09-23 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraCheese',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extra', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='NonSizableDish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('SmallPrice', models.FloatField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='MyOrder', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='SmallSize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('big', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Pasta',
            fields=[
                ('nonsizabledish_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.NonSizableDish')),
            ],
            bases=('orders.nonsizabledish',),
        ),
        migrations.CreateModel(
            name='Salad',
            fields=[
                ('nonsizabledish_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.NonSizableDish')),
            ],
            bases=('orders.nonsizabledish',),
        ),
        migrations.CreateModel(
            name='SizableDish',
            fields=[
                ('nonsizabledish_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.NonSizableDish')),
                ('LargePrice', models.FloatField(blank=True, default=None, null=True)),
            ],
            bases=('orders.nonsizabledish',),
        ),
        migrations.AddField(
            model_name='nonsizabledish',
            name='orders',
            field=models.ManyToManyField(blank=True, related_name='dish', to='orders.Order'),
        ),
        migrations.CreateModel(
            name='DinnerPlatter',
            fields=[
                ('sizabledish_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.SizableDish')),
            ],
            bases=('orders.sizabledish',),
        ),
        migrations.CreateModel(
            name='RegularPizza',
            fields=[
                ('sizabledish_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.SizableDish')),
                ('toppings', models.ManyToManyField(blank=True, related_name='reg_dish', to='orders.Topping')),
            ],
            bases=('orders.sizabledish',),
        ),
        migrations.CreateModel(
            name='SicilianPizza',
            fields=[
                ('sizabledish_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.SizableDish')),
                ('toppings', models.ManyToManyField(blank=True, related_name='sic_dish', to='orders.Topping')),
            ],
            bases=('orders.sizabledish',),
        ),
        migrations.CreateModel(
            name='Sub',
            fields=[
                ('sizabledish_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.SizableDish')),
                ('XCheesePrice', models.FloatField(blank=True, default=None, null=True)),
                ('Xcheese', models.ManyToManyField(related_name='subs_dish', to='orders.ExtraCheese')),
            ],
            bases=('orders.sizabledish',),
        ),
        migrations.AddField(
            model_name='sizabledish',
            name='size',
            field=models.ManyToManyField(blank=True, related_name='dish', to='orders.SmallSize'),
        ),
    ]
