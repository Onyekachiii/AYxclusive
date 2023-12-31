# Generated by Django 4.2.6 on 2023-10-10 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=1.99, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='cartorderproducts',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=1.99, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='cartorderproducts',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, default=1.99, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='old_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=2.99, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=1.99, max_digits=10, null=True),
        ),
    ]
