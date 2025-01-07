# Generated by Django 5.1.4 on 2025-01-07 12:27

import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibraryApp', '0009_alter_bookissue_status_fine'),
    ]

    operations = [
        migrations.AddField(
            model_name='fine',
            name='paid_amount',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
        migrations.AddField(
            model_name='fine',
            name='remaining_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='FinePayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('fine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partial_payments', to='LibraryApp.fine')),
            ],
        ),
    ]