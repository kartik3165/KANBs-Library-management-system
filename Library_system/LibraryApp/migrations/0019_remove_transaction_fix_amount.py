# Generated by Django 5.1.4 on 2025-01-08 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LibraryApp', '0018_remove_fine_fix_amount_transaction_fix_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='fix_amount',
        ),
    ]
