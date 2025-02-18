import requests
import json

from django.db import transaction

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from .models import Wallet


# https://api.coingecko.com/api/v3/coins/list


def fecth_instruments(
    instrument_symbol=None,
    currency=None,
):

    url = f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd,eur"

    if instrument_symbol:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={instrument_symbol}&vs_currencies={currency}"

    headers = {"accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        json_data = json.loads(response.text)
        data = {}

        if not response:
            data["response"] = {}
            data["message"] = "Instrument not found"

        if response:
            data["response"] = json_data
            data["message"] = "success"

        if response and instrument_symbol and currency:
            data["response"] = json_data[instrument_symbol]
            data["message"] = "success"
            data["price"] = json_data[instrument_symbol][currency]
    except:
        return Response(
            {"message": "An error occured, try again"}, status=status.HTTP_403_FORBIDDEN
        )

    return data


def deposit_to_wallet(
    user,
    amount,
):
    wallet, _ = Wallet.objects.get_or_create(user=user)
    if amount < 50:
        raise APIException(
            detail=f"{amount} is below minimum trade.",
            code=status.HTTP_400_BAD_REQUEST,
        )
    with transaction.atomic():
        wallet.balance += amount
        wallet.save()
    return wallet


def withdraw_from_wallet(user, amount):
    wallet, _ = Wallet.objects.get_or_create(user=user)
    if wallet.balance < amount:

        raise APIException(
            detail=f"Insufficient funds",
            code=status.HTTP_400_BAD_REQUEST,
        )
    with transaction.atomic():
        wallet.balance -= amount
        wallet.save()

    return wallet
