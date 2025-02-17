from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Instrument, Trade, Wallet
from .serializers import (
    InstrumentSerializer,
    TradeSerializer,
    WalletSerializer,
    TradeCreateSerializer,
)
from django.db import transaction


class InstrumentListAPIView(ListAPIView):
    queryset = Instrument.objects.all()
    serializer_class = InstrumentSerializer


class WalletAPIView(RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Wallet.objects.get(user=self.request.user)


class TradeHistoryAPIView(ListAPIView):
    serializer_class = TradeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Trade.objects.filter(user=self.request.user)


class TradeCreateAPIView(CreateAPIView):
    serializer_class = TradeCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)

        instrument = Instrument.objects.get(
            id=serializer.validated_data["instrument_id"]
        )
        order_type = serializer.validated_data["order_type"]
        quantity = serializer.validated_data["quantity"]
        price = serializer.validated_data["price"] or instrument.price

        with transaction.atomic():
            wallet, _ = Wallet.objects.get_or_create(user=request.user)

            if order_type == "buy":
                total_cost = quantity * price
                if wallet.balance < total_cost:
                    return Response(
                        {"error": "Insufficient funds"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                wallet.balance -= total_cost
                wallet.save()
                Trade.objects.create(
                    user=request.user,
                    instrument=instrument,
                    trade_type="buy",
                    quantity=quantity,
                    price=price,
                )

            elif order_type == "sell":
                trade = Trade.objects.filter(
                    user=request.user, instrument=instrument
                ).first()
                if not trade or trade.quantity < quantity:
                    return Response(
                        {"error": "Not enough holdings to sell"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                wallet.balance += quantity * price
                wallet.save()
                Trade.objects.create(
                    user=request.user,
                    instrument=instrument,
                    trade_type="sell",
                    quantity=quantity,
                    price=price,
                )

        return Response(
            {"message": f"{order_type.capitalize()} order placed successfully"},
            status=status.HTTP_201_CREATED,
        )
