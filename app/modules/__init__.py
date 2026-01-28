"""
Modules package initialization.
"""
from app.modules.inquiry import inquiry_module
from app.modules.wisdom import wisdom_module
from app.modules.voice import voice_module
from app.modules.value import value_module

__all__ = [
    "inquiry_module",
    "wisdom_module", 
    "voice_module",
    "value_module"
]
