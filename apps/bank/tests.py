from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from user.models import UserProfile
from .models import BankAccount, Transaction


class TransactionTestCase(APITestCase):
    def setUp(self):
        # Create a user and profile
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user, phone_number="1234567890"
        )

        # Create a bank account
        self.bank_account = BankAccount.objects.create(
            user_profile=self.user_profile,
            bank_name="Test Bank",
            account_number="123456789",
            routing_number="987654321",
        )

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

    def test_deposit(self):
        url = reverse("deposit")
        data = {"bank_account": self.bank_account.id, "amount": "1000.00"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["transaction_type"], "DEPOSIT")
        self.assertEqual(response.data["amount"], "1000.00")
        self.assertEqual(response.data["status"], "COMPLETED")

    def test_withdrawal(self):
        url = reverse("bank-withdrawal")
        data = {"bank_account": self.bank_account.id, "amount": "500.00"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["transaction_type"], "WITHDRAWAL")
        self.assertEqual(response.data["amount"], "500.00")
        self.assertEqual(response.data["status"], "COMPLETED")
