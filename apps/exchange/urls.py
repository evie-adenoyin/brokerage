from django.urls import path
from .views import (
    InstrumentListAPIView,
    WalletAPIView,
    TradeHistoryAPIView,
    TradeCreateAPIView,
)

urlpatterns = [
    path("instruments/", InstrumentListAPIView.as_view(), name="instruments"),
    path("wallet/", WalletAPIView.as_view(), name="wallet"),
    path("create/trade/", TradeCreateAPIView.as_view(), name="trade"),
    path("trade-history/", TradeHistoryAPIView.as_view(), name="trade_history"),
]
