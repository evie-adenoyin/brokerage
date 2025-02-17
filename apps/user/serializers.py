from collections import OrderedDict

from django.contrib import auth
from django.db.transaction import atomic


from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers

from .models import User, UserProfile
from .exceptions import UserAlreadyExistsException


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 6}}

    @atomic
    def create(self, validated_data: OrderedDict) -> User:
        """This method creates a new user."""

        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        user_profile = UserProfile(user=user)
        user_profile.save()

        return user
