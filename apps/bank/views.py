from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Account, Transaction
from .serializers import BankAccountSerializer, BankTransactionSerializer
from .utils import withdraw_funds, deposit_funds


class BankAccountCreateAPIView(generics.CreateAPIView):
    """View for listing and adding user bank accounts."""

    serializer_class = BankAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)


class BankAccountListAPIView(generics.ListAPIView):
    """View for listing and adding user bank accounts."""

    serializer_class = BankAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class BankTransactionAPIView(generics.ListAPIView):
    """View for initiating deposits and withdrawals."""

    serializer_class = BankTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class BankDepositAPIView(generics.CreateAPIView):
    serializer_class = BankTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, *args, **kwargs):
        # Ensure the bank account belongs to the logged-in user
        user = self.request.user
        bank_account = Account.objects.filter(
            user=user, bank_account=self.request.data["bank_account"]
        ).first()

        if not bank_account:
            return Response(
                {"error": "Bank account not found or does not belong to the user"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create a deposit transaction
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        deposit_to_account = deposit_funds(
            self.request.user,
            bank_account.pk,
        )
        serializer.save(
            bank_account=bank_account, transaction_type="DEPOSIT", status="COMPLETED"
        )

        return deposit_to_account


class BankWithdrawalAPIView(generics.CreateAPIView):
    serializer_class = BankTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, *args, **kwargs):
        # Ensure the bank account belongs to the logged-in user
        user = self.request.user
        bank_account = Account.objects.filter(
            user=user, bank_account=self.request.data["bank_account"]
        ).first()

        if not bank_account:
            return Response(
                {"error": "Bank account not found or does not belong to the user"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the account has sufficient balance (optional, if you track balance)
        # For now, we assume the bank handles balance checks

        # Create a withdrawal transaction
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        withdraw_from_account = withdraw_funds(
            request.user,
            bank_account.pk,
        )
        serializer.save(
            bank_account=bank_account, transaction_type="WITHDRAWAL", status="COMPLETED"
        )

        return withdraw_from_account
