"""
Structify AI - Health Check Route

Provides a /health endpoint for:
  - Deployment platforms to verify the server is running
  - Frontend to check API connectivity
  - Developers to quickly test if the server is up
"""

from fastapi import APIRouter
from datetime import datetime, timezone

from app.config import settings

# Create a router for health-related endpoints
# "tags" groups this in the auto-generated docs
router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns the current status of the API server,
    including app name, version, and environment.
    """
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
