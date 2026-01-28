"""
Inquiry API Routes.
"""
from fastapi import APIRouter, HTTPException, status
from app.models import InquiryRequest, InquiryResponse
from app.modules import inquiry_module, wisdom_module

router = APIRouter(prefix="/inquiry", tags=["Inquiry"])


@router.post("/submit", response_model=InquiryResponse, status_code=status.HTTP_201_CREATED)
async def submit_inquiry(inquiry: InquiryRequest):
    """
    Submit a new inquiry and receive wisdom in response.
    
    Args:
        inquiry: The inquiry request
        
    Returns:
        InquiryResponse with the wisdom answer
    """
    # Validate inquiry
    if not inquiry_module.validate_inquiry(inquiry):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid inquiry: question cannot be empty"
        )
    
    # Submit inquiry
    inquiry_id = await inquiry_module.submit_inquiry(inquiry)
    
    # Generate wisdom response
    wisdom = await wisdom_module.generate_wisdom(
        question=inquiry.question,
        inquiry_type=inquiry.inquiry_type,
        context=inquiry.context
    )
    
    return InquiryResponse(
        inquiry_id=inquiry_id,
        question=inquiry.question,
        wisdom=wisdom,
        inquiry_type=inquiry.inquiry_type
    )


@router.get("/history/{inquiry_id}")
async def get_inquiry_history(inquiry_id: str):
    """
    Retrieve an inquiry by ID.
    
    Args:
        inquiry_id: The inquiry ID
        
    Returns:
        Inquiry details
    """
    inquiry = await inquiry_module.get_inquiry(inquiry_id)
    if not inquiry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inquiry not found"
        )
    return inquiry
