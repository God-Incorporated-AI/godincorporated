"""
Inquiry Module - Handles question submission and processing.
"""
import uuid
from typing import Optional
from datetime import datetime
from app.models import InquiryRequest, InquiryResponse, InquiryType


class InquiryModule:
    """Module for handling inquiries and questions."""
    
    def __init__(self):
        """Initialize the inquiry module."""
        self.inquiries = {}
    
    async def submit_inquiry(self, inquiry: InquiryRequest) -> str:
        """
        Submit a new inquiry.
        
        Args:
            inquiry: The inquiry request
            
        Returns:
            Unique inquiry ID
        """
        inquiry_id = str(uuid.uuid4())
        self.inquiries[inquiry_id] = {
            "id": inquiry_id,
            "question": inquiry.question,
            "inquiry_type": inquiry.inquiry_type,
            "context": inquiry.context,
            "user_id": inquiry.user_id,
            "timestamp": datetime.utcnow(),
            "status": "submitted"
        }
        return inquiry_id
    
    async def get_inquiry(self, inquiry_id: str) -> Optional[dict]:
        """
        Retrieve an inquiry by ID.
        
        Args:
            inquiry_id: The inquiry ID
            
        Returns:
            Inquiry data or None
        """
        return self.inquiries.get(inquiry_id)
    
    def validate_inquiry(self, inquiry: InquiryRequest) -> bool:
        """
        Validate an inquiry request.
        
        Args:
            inquiry: The inquiry to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not inquiry.question or len(inquiry.question.strip()) == 0:
            return False
        return True


# Singleton instance
inquiry_module = InquiryModule()
