from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from users.models import UserProfile
from banking.models import Wallet
from .models import Trade


class TradeTestCase(APITestCase):
    def setUp(self):
        # Create a user and profile
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user, phone_number="1234567890"
        )

        # Create a wallet for the user
        self.wallet = Wallet.objects.create(
            user_profile=self.user_profile, balance=1000.00
        )

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

    def test_buy_trade(self):
        url = reverse("trade-create")
        data = {
            "instrument_symbol": "AAPL",
            "trade_type": "BUY",
            "quantity": 5,
            "price": "150.00",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)

        # Verify the trade was created
        trade = Trade.objects.get(id=response.data["id"])
        self.assertEqual(trade.trade_type, "BUY")
        self.assertEqual(trade.quantity, 5)
        self.assertEqual(trade.price, "150.00")

        # Verify the wallet balance was updated
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 250.00)  # 1000 - (5 * 150)
