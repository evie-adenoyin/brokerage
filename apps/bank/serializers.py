from collections import OrderedDict

from rest_framework import serializers

from apps.user.exceptions import UserAlreadyExistsException

from .models import Account, Transaction


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "user",
            "bank_name",
            "account_balance",
            "account_type",
            "account_number",
        ]
        read_only_fields = ["id", "user"]

    def create(self, validated_data: OrderedDict) -> Account:
        bank_account = Account(**validated_data)
        bank_account.save()
        return validated_data


class BankTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = [
            "user",
        ]
