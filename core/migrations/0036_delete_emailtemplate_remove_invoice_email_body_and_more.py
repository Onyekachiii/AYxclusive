# Generated by Django 4.2.6 on 2023-12-09 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_document_document_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EmailTemplate',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='email_body',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='email_subject',
        ),
        migrations.AddField(
            model_name='invoice',
            name='amount_to_be_paid',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=10),
        ),
        migrations.AddField(
            model_name='invoice',
            name='bank_details',
            field=models.TextField(default='Assemble Yourself Exclusive furnitures ltd, MCB Acct: 000449502171'),
        ),
    ]
