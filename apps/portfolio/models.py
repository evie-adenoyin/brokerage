from django.db import models
from django.conf import settings


class Portfolio(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="portfolio"
    )
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_profile.user.username}'s Portfolio"


class Holding(models.Model):
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, related_name="holdings"
    )
    instrument_symbol = models.CharField(
        max_length=10
    )  # Symbol of the instrument (e.g., AAPL)
    quantity = models.PositiveIntegerField()
    average_price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Average price per unit

    def __str__(self):
        return f"{self.instrument_symbol} - {self.quantity} @ {self.average_price}"
