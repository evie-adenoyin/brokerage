from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from .models import Account, Transaction


def deposit_funds(user, bank_account_pk, amount, description=None):
    bank_account = Account.objects.get(user=user, pk=bank_account_pk)
    if amount <= 0:
        raise ValidationError("Deposit amount must be greater than zero.")

    with transaction.atomic():  # Ensure atomicity
        # Create a deposit transaction
        deposit = Transaction.objects.create(
            user=user,
            bank_account=bank_account,
            # wallet_account = wallet_account
            transaction_type=Transaction.TRANSACTION_TYPE_DEPOSIT,
            amount=amount,
            status=Transaction.STATUS_COMPLETED,
            description=description,
        )

        # Update the bank account balance
        bank_account.account_balance += amount
        bank_account.save()
        message = {
            "status": "COMPLETED",
            "message": f"Deposit of {amount} completed for user {user.email}.",
        }

    return Response(message, status=status.HTTP_201_CREATED)


def withdraw_funds(user, bank_account_pk, amount, description=None):

    bank_account = Account.objects.get(pk=bank_account_pk, user=user)
    if amount <= 0:
        raise ValidationError("Withdrawal amount must be greater than zero.")

    if amount > bank_account.account_balance:
        raise ValidationError("Insufficient funds for withdrawal.")

    with transaction.atomic():  # Ensure atomicity
        # Create a withdrawal transaction
        withdrawal = Transaction.objects.create(
            user=user,
            bank_account=bank_account,
            transaction_type=Transaction.TRANSACTION_TYPE_WITHDRAWAL,
            amount=amount,
            status=Transaction.STATUS_COMPLETED,
            description=description,
        )

        # Update the bank account balance
        bank_account.account_balance -= amount
        bank_account.save()

    message = {
        "status": "COMPLETED",
        "message": f"Withdrawal of {amount} completed for user {user.email}.",
    }

    return Response(message, status=status.HTTP_201_CREATED)
