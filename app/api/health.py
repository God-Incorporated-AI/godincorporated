"""
Health Check API Routes.
"""
from fastapi import APIRouter
from app.models import HealthResponse
from app.config import settings
from app.modules import inquiry_module, wisdom_module, voice_module, value_module

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        HealthResponse with service status
    """
    modules_status = {
        "inquiry": "available",
        "wisdom": "available" if wisdom_module.is_available() else "limited",
        "voice": "available" if voice_module.is_available() else "unavailable",
        "value": "available"
    }
    
    return HealthResponse(
        status="healthy",
        version=settings.api_version,
        modules=modules_status
    )


@router.get("/")
async def root():
    """
    Root endpoint.
    
    Returns:
        Welcome message
    """
    return {
        "message": "Welcome to God Incorporated Oracle API",
        "version": settings.api_version,
        "description": settings.api_description,
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "inquiry": "/inquiry/submit",
            "voice": "/voice/process",
            "value": "/value/contribute"
        }
    }
