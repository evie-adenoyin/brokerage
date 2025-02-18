from decimal import Decimal

from django.db import transaction

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.user.models import UserProfile

from .models import Wallet, Trade
from .serializers import TradeSerializer
from .utils import fecth_instruments, deposit_to_wallet, withdraw_from_wallet


class TradeCreateAPIView(generics.CreateAPIView):
    serializer_class = TradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Ensure the user profile exists
        user = request.user
        data = self.request.data
        instrument_symbol = data["instrument_symbol"]

        # Validate the instrument symbol
        instrument_data = fecth_instruments(
            instrument_symbol, Trade.USD_CURRENCY.lower()
        )

        if instrument_data["message"] == "success":
            # Get the current price from the API
            current_price = instrument_data["price"]
            print(current_price)

        # # Calculate the total cost of the trade
        instrument_quantity = Decimal(data["quantity"])
        instrument_total_cost = instrument_quantity * current_price
        # # Create the trade

        with transaction.atomic():

            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(
                user=user,
                price=current_price,
            )

            if data["trade_type"] == Trade.BUY_TRADE:
                withdraw_from_wallet(user, instrument_total_cost)
                return Response(
                    {
                        "message": f"{instrument_total_cost} has been withdrawn successfully from your wallet"
                    },
                    status=status.HTTP_201_CREATED,
                )

            if data["trade_type"] == Trade.SELL_TRADE:
                deposit_to_wallet(user, instrument_total_cost)
                return Response(
                    {
                        "message": f"{instrument_total_cost} has been deposited successfully into your wallet"
                    },
                    status=status.HTTP_201_CREATED,
                )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TradeListAPIView(generics.ListAPIView):
    serializer_class = TradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Trade.objects.filter(user=self.request.user)
