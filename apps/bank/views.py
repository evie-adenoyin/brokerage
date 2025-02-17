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
        data = self.request.data
        user_account_number = data["bank_account"]
        amount = data["amount"]
        user = self.request.user
        user_bank_account = Account.objects.filter(
            user=user, account_number=user_account_number
        ).first()

        if not user_bank_account:
            return Response(
                {"error": "Bank account not found or does not belong to the user"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create a deposit transaction

        deposit_to_account = deposit_funds(self.request.user, user_bank_account, amount)
        return Response({"message": deposit_to_account}, status=status.HTTP_201_CREATED)


class BankWithdrawalAPIView(generics.CreateAPIView):
    serializer_class = BankTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, *args, **kwargs):
        # Ensure the bank account belongs to the logged-in user
        data = self.request.data
        user_account_number = data["bank_account"]
        amount = data["amount"]
        user = self.request.user
        user_bank_account = Account.objects.filter(
            user=user, account_number=user_account_number
        ).first()

        if not user_bank_account:
            return Response(
                {"error": "Bank account not found or does not belong to the user"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create a deposit transaction

        withdraw_from_account = withdraw_funds(
            self.request.user, user_bank_account, amount
        )
        return Response(
            {"message": withdraw_from_account}, status=status.HTTP_201_CREATED
        )
