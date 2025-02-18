from django.urls import path
from .views import TradeCreateAPIView, TradeListAPIView

app_name = "Trade"
urlpatterns = [
    path("", TradeCreateAPIView.as_view(), name="trade"),
    path("trades/", TradeListAPIView.as_view(), name="trades"),
]
