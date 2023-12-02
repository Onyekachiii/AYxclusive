# Generated by Django 4.2.6 on 2023-12-02 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_remove_wallettransaction_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallettransaction',
            name='added_amount',
        ),
        migrations.RemoveField(
            model_name='wallettransaction',
            name='deducted_amount',
        ),
        migrations.AddField(
            model_name='wallettransaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=10),
        ),
    ]
