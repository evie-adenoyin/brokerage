from collections import OrderedDict

from rest_framework import serializers

from apps.user.exceptions import UserAlreadyExistsException

from .models import Account, Transaction


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["user", "bank_name", "account_type", "account_number"]
        read_only_fields = ["user"]

    def create(self, validated_data: OrderedDict) -> Account:

        user = validated_data["user"]
        bank_name = validated_data["bank_name"]
        account_number = validated_data["account_number"]
        account_type = validated_data["account_type"]

        try:
            bank_account = Account.objects.get(
                user=user,
                bank_name=bank_name,
                account_number=account_number,
                account_type=account_type,
            )
            if bank_account:
                raise serializers.ValidationError(
                    {"bank_name": "This field is required."}
                )

        except Account.DoesNotExist:
            bank_account = Account.objects.create(**validated_data)

        return validated_data


class BankTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = [
            "user",
            "transaction_id",
            "amount",
            "currency",
            "status",
            "description",
        ]
