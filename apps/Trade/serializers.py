from rest_framework import serializers
from .models import Trade


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = [
            "instrument_symbol",
            "trade_type",
            "quantity",
        ]

        read_only_fields = [
            "id",
            "user",
            "timestamp",
        ]  # These fields are auto-populated
