# Generated by Django 4.2.6 on 2024-01-18 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_termsandconditions'),
    ]

    operations = [
        migrations.CreateModel(
            name='RefundPolicy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
            ],
        ),
    ]
