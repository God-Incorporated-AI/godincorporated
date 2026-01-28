"""
Value-for-Value Module - Handles contributions and exchanges.
"""
import uuid
from typing import Optional
from datetime import datetime
from app.models import ValueExchangeRequest, ValueExchangeResponse
from app.config import settings


class ValueModule:
    """Module for value-for-value participation."""
    
    def __init__(self):
        """Initialize the value module."""
        self.enabled = settings.enable_payments
        self.transactions = {}
    
    async def process_contribution(self, request: ValueExchangeRequest) -> ValueExchangeResponse:
        """
        Process a value contribution.
        
        Args:
            request: Value exchange request
            
        Returns:
            ValueExchangeResponse
        """
        transaction_id = str(uuid.uuid4())
        
        if self.enabled:
            # In a real implementation, this would integrate with payment provider
            # For now, simulate successful transaction
            status = "completed"
        else:
            # When payments are disabled, acknowledge but don't process
            status = "acknowledged"
        
        transaction = {
            "id": transaction_id,
            "amount": request.amount,
            "currency": request.currency,
            "message": request.message,
            "status": status,
            "timestamp": datetime.utcnow()
        }
        
        self.transactions[transaction_id] = transaction
        
        return ValueExchangeResponse(
            transaction_id=transaction_id,
            status=status,
            amount=request.amount
        )
    
    async def get_transaction(self, transaction_id: str) -> Optional[dict]:
        """
        Get transaction details.
        
        Args:
            transaction_id: Transaction ID
            
        Returns:
            Transaction data or None
        """
        return self.transactions.get(transaction_id)
    
    def is_available(self) -> bool:
        """Check if value module is available."""
        return True  # Always available, even if payments are disabled


# Singleton instance
value_module = ValueModule()
