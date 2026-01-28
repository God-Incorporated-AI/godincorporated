"""
Wisdom Module - Provides AI-powered responses using OpenAI.
"""
import logging
from typing import Optional, List
from app.models import WisdomResponse, InquiryType
from app.config import settings

# Configure logging
logger = logging.getLogger(__name__)


class WisdomModule:
    """Module for generating wisdom and AI-powered responses."""
    
    def __init__(self):
        """Initialize the wisdom module."""
        self.openai_available = bool(settings.openai_api_key)
        if self.openai_available:
            try:
                import openai
                self.client = openai.OpenAI(api_key=settings.openai_api_key)
            except (ImportError, Exception) as e:
                logger.warning(f"OpenAI initialization failed: {e}")
                self.openai_available = False
                self.client = None
        else:
            self.client = None
    
    async def generate_wisdom(
        self, 
        question: str, 
        inquiry_type: InquiryType = InquiryType.GENERAL,
        context: Optional[str] = None
    ) -> WisdomResponse:
        """
        Generate a wisdom response for a question.
        
        Args:
            question: The question to answer
            inquiry_type: Type of inquiry
            context: Additional context
            
        Returns:
            WisdomResponse with the answer
        """
        if self.openai_available and self.client:
            try:
                # Build the prompt based on inquiry type
                system_prompt = self._build_system_prompt(inquiry_type)
                user_message = question
                if context:
                    user_message = f"Context: {context}\n\nQuestion: {question}"
                
                # Call OpenAI API
                response = self.client.chat.completions.create(
                    model=settings.openai_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=0.7,  # Balance between creativity and consistency
                    max_tokens=1000  # Reasonable limit for wisdom responses
                )
                
                answer = response.choices[0].message.content
                confidence = 0.85  # High confidence for AI-generated responses
                
                return WisdomResponse(
                    answer=answer,
                    confidence=confidence,
                    sources=["OpenAI GPT"]
                )
            except Exception as e:
                # Log error and fallback to default response
                logger.error(f"OpenAI API call failed: {e}")
                return self._generate_fallback_response(question, inquiry_type)
        else:
            # Use fallback when OpenAI is not available
            return self._generate_fallback_response(question, inquiry_type)
    
    def _build_system_prompt(self, inquiry_type: InquiryType) -> str:
        """
        Build system prompt based on inquiry type.
        
        Args:
            inquiry_type: Type of inquiry
            
        Returns:
            System prompt string
        """
        prompts = {
            InquiryType.WISDOM: "You are a wise oracle providing thoughtful, philosophical insights and wisdom. Draw from various philosophical traditions and offer deep, meaningful perspectives.",
            InquiryType.GUIDANCE: "You are a helpful guide providing practical advice and direction. Focus on actionable steps and clear guidance.",
            InquiryType.INSIGHT: "You are an insightful analyst providing deep understanding and clarity. Help uncover hidden patterns and meanings.",
            InquiryType.GENERAL: "You are a knowledgeable assistant providing helpful, accurate, and thoughtful responses."
        }
        return prompts.get(inquiry_type, prompts[InquiryType.GENERAL])
    
    def _generate_fallback_response(self, question: str, inquiry_type: InquiryType) -> WisdomResponse:
        """
        Generate a fallback response when AI is not available.
        
        Args:
            question: The question
            inquiry_type: Type of inquiry
            
        Returns:
            WisdomResponse with fallback answer
        """
        fallback_responses = {
            InquiryType.WISDOM: f"Thank you for your inquiry about: '{question}'. In wisdom, we find that understanding comes from contemplation and reflection. Consider what this question means to you personally.",
            InquiryType.GUIDANCE: f"Thank you for seeking guidance on: '{question}'. The path forward often reveals itself through careful consideration of your goals and values.",
            InquiryType.INSIGHT: f"Your inquiry about '{question}' invites deeper examination. Look beneath the surface to find the patterns and connections.",
            InquiryType.GENERAL: f"Thank you for your question about: '{question}'. This is an interesting inquiry that deserves thoughtful consideration."
        }
        
        answer = fallback_responses.get(inquiry_type, fallback_responses[InquiryType.GENERAL])
        
        return WisdomResponse(
            answer=answer,
            confidence=0.5,  # Lower confidence for fallback responses
            sources=["Built-in responses"]
        )
    
    def is_available(self) -> bool:
        """Check if the wisdom module is available."""
        return self.openai_available


# Singleton instance
wisdom_module = WisdomModule()
