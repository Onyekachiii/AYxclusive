# Generated by Django 4.2.6 on 2023-11-30 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0007_alter_contactus_options_alter_contactus_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_email_verified',
            field=models.BooleanField(default=False),
        ),
    ]
