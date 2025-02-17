"""
URL configuration for the brokerage project.

The `urlpatterns` list routes URLs to views. For more information, see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger Schema View
schema_view = get_schema_view(
    openapi.Info(
        title="Brokerage API",
        default_version="v1",
        description="API for Brokerage Application",
        # contact=openapi.Contact(email="support@brokerage.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

# URL Patterns
urlpatterns = [
    # Admin Panel
    path("admin/", admin.site.urls),
    # Swagger Documentation
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # API Endpoints
    path("api/user/", include("apps.user.urls")),  # user App URLs
    path("api/bank/", include("apps.bank.urls")),  # bank App URLs
]


# accounts – Manages user authentication (signup, login, profile).
# payments – Handles bank account linking, deposits, and withdrawals.
# trading – Manages buying and selling of stocks, bonds, and crypto.
# portfolio – Tracks user investments, historical performance.
# exchange – Integrates with third-party exchanges for prices & trades.
