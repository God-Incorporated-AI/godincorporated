"""
API Routes package initialization.
"""
from app.api.inquiry import router as inquiry_router
from app.api.voice import router as voice_router
from app.api.value import router as value_router
from app.api.health import router as health_router

__all__ = [
    "inquiry_router",
    "voice_router",
    "value_router",
    "health_router"
]
