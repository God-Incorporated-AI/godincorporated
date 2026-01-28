"""
Voice API Routes.
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, status
from app.models import VoiceRequest, VoiceResponse
from app.modules import voice_module
from typing import Optional

router = APIRouter(prefix="/voice", tags=["Voice"])


@router.post("/process", response_model=VoiceResponse)
async def process_voice(
    audio_file: Optional[UploadFile] = File(None),
    language: str = "en-US"
):
    """
    Process voice input.
    
    Args:
        audio_file: Optional audio file
        language: Language code
        
    Returns:
        VoiceResponse with transcribed text
    """
    if not voice_module.is_available():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Voice module is not available"
        )
    
    audio_data = None
    if audio_file:
        audio_data = await audio_file.read()
    
    request = VoiceRequest(language=language)
    response = await voice_module.process_voice_request(request, audio_data)
    
    return response


@router.get("/status")
async def voice_status():
    """
    Get voice module status.
    
    Returns:
        Status information
    """
    return {
        "available": voice_module.is_available(),
        "tts_available": voice_module.tts_available,
        "stt_available": voice_module.stt_available
    }
