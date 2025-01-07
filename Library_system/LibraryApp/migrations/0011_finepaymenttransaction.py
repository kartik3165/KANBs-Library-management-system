# Generated by Django 5.1.4 on 2025-01-07 13:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibraryApp', '0010_fine_paid_amount_fine_remaining_amount_finepayment'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinePaymentTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('remaining_balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_transactions', to='LibraryApp.fine')),
            ],
        ),
    ]
