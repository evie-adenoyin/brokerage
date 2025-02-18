from decimal import Decimal
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

# Create your models here.


class Wallet(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallet"
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s Wallet"


class Trade(models.Model):
    BUY_TRADE = "BUY"
    SELL_TRADE = "SELL"
    TRADE_TYPES = [
        (BUY_TRADE, "Buy"),
        (SELL_TRADE, "Sell"),
    ]
    USD_CURRENCY = "USD"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="trades"
    )
    instrument_symbol = models.CharField(
        max_length=10
    )  # Symbol of the instrument (e.g., AAPL)
    trade_type = models.CharField(max_length=4, choices=TRADE_TYPES)
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per unit
    currency = models.CharField(max_length=3, default=USD_CURRENCY)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trade_type} - {self.instrument_symbol} - {self.quantity} @ {self.price}"
