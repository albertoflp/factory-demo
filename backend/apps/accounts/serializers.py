"""Serializers for the accounts app."""
from __future__ import annotations

from django.contrib.auth.models import User
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """Validates the login request payload."""

    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})


class UserSerializer(serializers.ModelSerializer):
    """Public representation of an authenticated user."""

    class Meta:
        model = User
        fields = ["id", "username", "is_staff"]
        read_only_fields = fields
