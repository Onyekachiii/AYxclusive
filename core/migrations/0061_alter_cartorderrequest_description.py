# Generated by Django 4.2.6 on 2024-02-01 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0060_alter_cartorderrequest_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorderrequest',
            name='description',
            field=models.TextField(default=None, null=True),
        ),
    ]