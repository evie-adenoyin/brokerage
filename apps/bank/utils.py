from decimal import Decimal
from django.db import transaction
from rest_framework import exceptions
from rest_framework import status


from apps.trade.utils import deposit_to_wallet, withdraw_from_wallet
from .models import Transaction


def deposit_funds(user, account, amount, description=None):
    deposit_amount = Decimal(amount)

    if deposit_amount <= 0:
        raise exceptions.ValidationError(
            detail="Deposit amount must be greater than zero.",
            code=status.HTTP_400_BAD_REQUEST,
        )

    with transaction.atomic():  # Ensure atomicity

        withdraw_from_wallet(user, deposit_amount)
        account.account_balance += deposit_amount
        account.save()

        deposit = Transaction(
            user=user,
            bank_account=account,
            transaction_type=Transaction.TRANSACTION_TYPE_DEPOSIT,
            amount=deposit_amount,
            status=Transaction.STATUS_COMPLETED,
            description=description,
        )

        deposit.save()

        message = {
            "status": "COMPLETED",
            "message": f"Deposit of {deposit_amount} completed for user {user.email}.",
        }

    return message


def withdraw_funds(user, account, amount, description=None):
    withdraw_amount = Decimal(amount)
    if withdraw_amount <= 0:
        raise exceptions.ValidationError(
            detail="Withdrawal amount must be greater than zero.",
            code=status.HTTP_400_BAD_REQUEST,
        )

    if withdraw_amount > account.account_balance:
        raise exceptions.ValidationError(
            detail="Insufficient funds for withdrawal.",
            code=status.HTTP_400_BAD_REQUEST,
        )

    with transaction.atomic():  # Ensure atomicity
        # Create a withdrawal transaction
        # Update the bank account balance
        account.account_balance -= withdraw_amount
        account.save()
        deposit_to_wallet(user, withdraw_amount)
        withdrawal = Transaction(
            user=user,
            bank_account=account,
            transaction_type=Transaction.TRANSACTION_TYPE_WITHDRAWAL,
            amount=withdraw_amount,
            status=Transaction.STATUS_COMPLETED,
            description=description,
        )
        withdrawal.save()

        message = {
            "status": "COMPLETED",
            "message": f"Withdrawal of {amount} completed for user {user.email}.",
        }

    return message
