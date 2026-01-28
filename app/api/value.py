"""
Value-for-Value API Routes.
"""
from fastapi import APIRouter, HTTPException, status
from app.models import ValueExchangeRequest, ValueExchangeResponse
from app.modules import value_module

router = APIRouter(prefix="/value", tags=["Value"])


@router.post("/contribute", response_model=ValueExchangeResponse, status_code=status.HTTP_201_CREATED)
async def contribute(request: ValueExchangeRequest):
    """
    Make a value contribution.
    
    Args:
        request: Value exchange request
        
    Returns:
        ValueExchangeResponse with transaction details
    """
    if not value_module.is_available():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Value module is not available"
        )
    
    response = await value_module.process_contribution(request)
    return response


@router.get("/transaction/{transaction_id}")
async def get_transaction(transaction_id: str):
    """
    Get transaction details.
    
    Args:
        transaction_id: Transaction ID
        
    Returns:
        Transaction details
    """
    transaction = await value_module.get_transaction(transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return transaction


@router.get("/status")
async def value_status():
    """
    Get value module status.
    
    Returns:
        Status information
    """
    from app.config import settings
    return {
        "available": value_module.is_available(),
        "payments_enabled": settings.enable_payments
    }
