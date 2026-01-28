"""
Data models for God Incorporated API.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone
from enum import Enum


class InquiryType(str, Enum):
    """Types of inquiries."""
    WISDOM = "wisdom"
    GUIDANCE = "guidance"
    INSIGHT = "insight"
    GENERAL = "general"


class InquiryRequest(BaseModel):
    """Request model for submitting an inquiry."""
    question: str = Field(..., description="The inquiry or question to ask", min_length=1, max_length=5000)
    inquiry_type: InquiryType = Field(default=InquiryType.GENERAL, description="Type of inquiry")
    context: Optional[str] = Field(None, description="Additional context for the inquiry", max_length=2000)
    user_id: Optional[str] = Field(None, description="Optional user identifier")


class WisdomResponse(BaseModel):
    """Response model for wisdom queries."""
    answer: str = Field(..., description="The wisdom or answer provided")
    confidence: float = Field(..., description="Confidence level of the response (0-1)", ge=0, le=1)
    sources: Optional[List[str]] = Field(default=None, description="Sources or references")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class InquiryResponse(BaseModel):
    """Response model for inquiries."""
    inquiry_id: str = Field(..., description="Unique identifier for the inquiry")
    question: str = Field(..., description="The original question")
    wisdom: WisdomResponse = Field(..., description="The wisdom response")
    inquiry_type: InquiryType = Field(..., description="Type of inquiry")


class VoiceRequest(BaseModel):
    """Request model for voice interaction."""
    audio_format: str = Field(default="wav", description="Audio format")
    language: str = Field(default="en-US", description="Language code")


class VoiceResponse(BaseModel):
    """Response model for voice interaction."""
    text: str = Field(..., description="Transcribed or generated text")
    audio_url: Optional[str] = Field(None, description="URL to audio file if generated")


class ValueExchangeRequest(BaseModel):
    """Request model for value-for-value participation."""
    amount: float = Field(..., description="Amount to contribute", gt=0, le=1000000)
    currency: str = Field(default="USD", description="Currency code")
    message: Optional[str] = Field(None, description="Optional message with contribution")


class ValueExchangeResponse(BaseModel):
    """Response model for value exchange."""
    transaction_id: str = Field(..., description="Transaction identifier")
    status: str = Field(..., description="Transaction status")
    amount: float = Field(..., description="Amount exchanged")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    modules: dict = Field(default_factory=dict, description="Status of individual modules")
