"""URL routes for the accounts app, mounted at /api/auth/."""
from __future__ import annotations

from django.urls import path

from .views import login_view, me_view

urlpatterns = [
    path("login/", login_view, name="auth-login"),
    path("me/", me_view, name="auth-me"),
]
