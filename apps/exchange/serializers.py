from rest_framework import serializers
from .models import Trade, Instrument, Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"


class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = "__all__"


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = "__all__"


class TradeCreateSerializer(serializers.Serializer):
    instrument_id = serializers.IntegerField()
    order_type = serializers.ChoiceField(choices=["buy", "sell"])
    quantity = serializers.DecimalField(max_digits=10, decimal_places=4)
    price = serializers.DecimalField(
        max_digits=12, decimal_places=2, required=False, allow_null=True
    )

    def validate(self, data):
        if (
            data["order_type"] == "sell"
            and not self.context["user"]
            .trade_set.filter(instrument_id=data["instrument_id"])
            .exists()
        ):
            raise serializers.ValidationError("You don't own this asset to sell.")
        return data
