from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegistrationAPIView

# app_name = "user"
urlpatterns = [
    path(
        "registration/",
        UserRegistrationAPIView.as_view(),
        name="user-registration",
    ),
    # Token endpoints
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
