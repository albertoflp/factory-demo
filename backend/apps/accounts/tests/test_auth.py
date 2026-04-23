"""Tests for the session-auth login and whoami endpoints."""
from __future__ import annotations

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def user(db) -> User:
    return User.objects.create_user(
        username="alice",
        password="correct-horse-battery-staple",
    )


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
def test_login_happy_path(client: APIClient, user: User) -> None:
    response = client.post(
        reverse("auth-login"),
        {"username": "alice", "password": "correct-horse-battery-staple"},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"id": user.id, "username": "alice", "is_staff": False}
    assert "sessionid" in response.cookies


@pytest.mark.django_db
def test_login_bad_credentials(client: APIClient, user: User) -> None:
    response = client.post(
        reverse("auth-login"),
        {"username": "alice", "password": "wrong"},
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data == {"detail": "Invalid credentials."}


@pytest.mark.django_db
def test_login_missing_fields(client: APIClient) -> None:
    response = client.post(reverse("auth-login"), {}, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.data
    assert "password" in response.data


@pytest.mark.django_db
def test_me_authenticated(client: APIClient, user: User) -> None:
    client.force_login(user)

    response = client.get(reverse("auth-me"))

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"id": user.id, "username": "alice", "is_staff": False}


@pytest.mark.django_db
def test_me_unauthenticated(client: APIClient) -> None:
    response = client.get(reverse("auth-me"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
