import uuid

from django.db import models
from django.conf import settings


class Wallet(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallet"
    )
    wallet_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Wallet - {self.wallet_id}"

    def deposit(self, amount):
        """Increase wallet balance when a user funds their wallet."""
        if amount > 0:
            self.balance += amount
            self.save()
            return True
        return False

    def withdraw(self, amount):
        """Decrease wallet balance when a user withdraws to their bank."""
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False


class Instrument(models.Model):

    INSTRUMENTS_TYPES = [
        ("stock", "Stock"),
        ("crypto", "Cryptocurrency"),
        ("bond", "Bond"),
    ]
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=10, choices=INSTRUMENTS_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.symbol})"


class Trade(models.Model):
    TRADE_TYPES = [
        ("buy", "Buy"),
        ("sell", "Sell"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    trade_type = models.CharField(max_length=4, choices=TRADE_TYPES)
    quantity = models.PositiveIntegerField()
    price_at_trade = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, default="pending"
    )  # pending, completed, canceled
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.trade_type} {self.quantity} {self.asset.symbol}"
