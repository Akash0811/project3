# Generated by Django 2.0.3 on 2018-10-10 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20181011_0220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dinnerplatter',
            name='LargePrice',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='dinnerplatter',
            name='SmallPrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='pasta',
            name='LargePrice',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='pasta',
            name='SmallPrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='regularpizza',
            name='LargePrice',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='regularpizza',
            name='SmallPrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='salad',
            name='LargePrice',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='salad',
            name='SmallPrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='sicilianpizza',
            name='LargePrice',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='sicilianpizza',
            name='SmallPrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='sub',
            name='LargePrice',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='sub',
            name='SmallPrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='templatedinnerplatter',
            name='LargePrice',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='templatedinnerplatter',
            name='SmallPrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='templatepasta',
            name='SmallPrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='templateregularpizza',
            name='LargePrice',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='templateregularpizza',
            name='SmallPrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='templateregularpizza',
            name='Topping1LargePrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='templateregularpizza',
            name='Topping1SmallPrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='templateregularpizza',
            name='Topping2LargePrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='templateregularpizza',
            name='Topping2SmallPrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='templateregularpizza',
            name='Topping3LargePrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='templateregularpizza',
            name='Topping3SmallPrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='templatesalad',
            name='SmallPrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='templatesicilianpizza',
            name='LargePrice',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='templatesicilianpizza',
            name='SmallPrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='templatesicilianpizza',
            name='Topping1LargePrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='templatesicilianpizza',
            name='Topping1SmallPrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='templatesicilianpizza',
            name='Topping2LargePrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='templatesicilianpizza',
            name='Topping2SmallPrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='templatesicilianpizza',
            name='Topping3LargePrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='templatesicilianpizza',
            name='Topping3SmallPrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='templatesub',
            name='LargePrice',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='templatesub',
            name='SmallPrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='templatesub',
            name='XCheesePrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
    ]
