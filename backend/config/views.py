"""Project-level DRF views (health check, etc.)."""
from __future__ import annotations

from django.db import DatabaseError, connection
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response


@api_view(["GET"])
def health(_request: Request) -> Response:
    """Report service health, including a database ping.

    Returns 200 with ``{"status": "ok", "db": "ok"}`` when the database is
    reachable, and 503 with ``{"status": "down", "db": "down"}`` otherwise.
    """
    try:
        connection.ensure_connection()
    except DatabaseError:
        return Response(
            {"status": "down", "db": "down"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    return Response({"status": "ok", "db": "ok"})
