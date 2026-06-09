"""
Structify AI - Main Application Entry Point

Responsibilities:
1. Create FastAPI application
2. Configure CORS
3. Register API routers
4. Expose root endpoint
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import (
    health,
    ocr,
    structure,
    export,
    text,
)

# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "Turn messy OCR text into perfectly structured documents. "
        "AI-powered structure recovery, document intelligence, "
        "and smart formatting profiles."
    ),
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ============================================================
# CORS Configuration
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# Route Registration
# ============================================================

app.include_router(health.router)
app.include_router(ocr.router)
app.include_router(structure.router)
app.include_router(export.router)
app.include_router(text.router)

# ============================================================
# Root Endpoint
# ============================================================

@app.get("/", tags=["Root"])
async def root():
    """
    API homepage.
    """

    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "tagline": (
            "Turn messy OCR text into perfectly structured documents."
        ),
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
    }