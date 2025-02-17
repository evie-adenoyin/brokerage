from rest_framework import status
from rest_framework.exceptions import APIException


class UserAlreadyExistsException(APIException):
    status_code = status.HTTP_201_CREATED
    default_detail = "User with this email already exists yo."
    default_code = "user_already_exists"
