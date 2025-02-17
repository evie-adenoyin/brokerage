from django.urls import path
from .views import (
    BankAccountCreateAPIView,
    BankAccountListAPIView,
    BankTransactionAPIView,
    BankDepositAPIView,
    BankWithdrawalAPIView,
)

urlpatterns = [
    path(
        "bank-account/create",
        BankAccountCreateAPIView.as_view(),
        name="bank-account-creation",
    ),
    path("bank-accounts/", BankAccountListAPIView.as_view(), name="bank-account-list"),
    path(
        "bank-transactions/",
        BankTransactionAPIView.as_view(),
        name="transaction-create",
    ),
    path("bank-deposit/", BankDepositAPIView.as_view(), name="bank-deposit"),
    path("bank-withdrawal/", BankWithdrawalAPIView.as_view(), name="bank-withdrawal"),
]
