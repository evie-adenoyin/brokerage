# Generated by Django 5.0.8 on 2025-02-16 12:20

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0002_bankaccount_account_balance_transaction_currency_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BankAccount',
            new_name='Account',
        ),
    ]
