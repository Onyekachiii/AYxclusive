# Generated by Django 4.2.6 on 2023-12-02 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_remove_wallettransaction_added_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallettransaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
