import uuid
from django.db import models
from django.conf import settings


# TODO: Change model Account, to Account
class Account(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bank_accounts"
    )
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50, unique=True)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    account_type = models.CharField(
        max_length=50, choices=[("savings", "Savings"), ("checking", "Checking")]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"


class Transaction(models.Model):
    TRANSACTION_TYPE_DEPOSIT = "deposit"
    TRANSACTION_TYPE_WITHDRAWAL = "withdrawal"
    TRANSACTION_TYPES = [
        (TRANSACTION_TYPE_DEPOSIT, "Deposit"),
        (TRANSACTION_TYPE_WITHDRAWAL, "Withdrawal"),
    ]

    STATUS_PENDING = "pending"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_FAILED, "Failed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_transactions",
        db_index=True,
    )
    bank_account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="bank_transactions"
    )
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    currency = models.CharField(max_length=3, default="USD")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    def __str__(self):
        return f"{self.user} - {self.transaction_type} - {self.amount}"
