# Generated by Django 4.2.6 on 2023-12-02 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_wallettransaction_balance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallettransaction',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='wallettransaction',
            name='balance',
        ),
        migrations.AddField(
            model_name='wallettransaction',
            name='added_amount',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=10),
        ),
        migrations.AddField(
            model_name='wallettransaction',
            name='deducted_amount',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=10),
        ),
    ]
