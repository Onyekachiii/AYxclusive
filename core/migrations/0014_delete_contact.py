# Generated by Django 4.2.6 on 2023-11-29 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_contact_address_alter_contact_description'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Contact',
        ),
    ]
