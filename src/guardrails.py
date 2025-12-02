"""Guardrails for query validation and safety"""
import logging
from typing import Optional, Dict
from pydantic import BaseModel, ValidationError, field_validator
from src.config import settings

logger = logging.getLogger(__name__)


class QueryValidation(BaseModel):
    """Pydantic model for query validation"""
    query: str
    
    @field_validator('query')
    @classmethod
    def validate_query(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Query cannot be empty")
        max_length = settings.MAX_QUERY_LENGTH
        if len(v) > max_length:
            raise ValueError(f"Query exceeds maximum length of {max_length} characters")
        return v.strip()
    
    def check_unsafe_patterns(self) -> Dict[str, bool]:
        """Check for potentially unsafe query patterns"""
        unsafe_patterns = [
            "delete", "drop", "remove", "clear",
            "password", "secret", "api key",
            "hack", "exploit", "vulnerability"
        ]
        
        query_lower = self.query.lower()
        found_patterns = [pattern for pattern in unsafe_patterns if pattern in query_lower]
        
        return {
            "is_safe": len(found_patterns) == 0,
            "found_patterns": found_patterns
        }


class Guardrails:
    """Guardrails system for query safety and validation"""
    
    def __init__(self, enable_guardrails: bool = True):
        self.enable_guardrails = enable_guardrails
        self.rebuff_client = None
        
        # Initialize Rebuff if API key is provided
        if settings.REBUFF_API_KEY and enable_guardrails:
            try:
                import rebuff
                self.rebuff_client = rebuff.Rebuff(
                    api_key=settings.REBUFF_API_KEY
                )
                logger.info("Rebuff guardrails initialized")
            except Exception as e:
                logger.warning(f"Could not initialize Rebuff: {str(e)}")
    
    def validate_query(self, query: str) -> Dict:
        """Validate and check query safety"""
        result = {
            "is_valid": False,
            "is_safe": True,
            "error": None,
            "warnings": []
        }
        
        if not self.enable_guardrails:
            result["is_valid"] = True
            return result
        
        try:
            # Pydantic validation
            validated_query = QueryValidation(query=query)
            result["is_valid"] = True
            
            # Check unsafe patterns
            safety_check = validated_query.check_unsafe_patterns()
            result["is_safe"] = safety_check["is_safe"]
            
            if not result["is_safe"]:
                result["warnings"].append(f"Query contains potentially unsafe patterns: {safety_check['found_patterns']}")
            
            # Rebuff check if available
            if self.rebuff_client:
                try:
                    rebuff_result = self.rebuff_client.detect_injection(query)
                    if rebuff_result.injection_detected:
                        result["is_safe"] = False
                        result["warnings"].append("Potential injection attack detected by Rebuff")
                except Exception as e:
                    logger.warning(f"Rebuff check failed: {str(e)}")
            
        except ValidationError as e:
            result["is_valid"] = False
            result["error"] = str(e)
        except Exception as e:
            result["is_valid"] = False
            result["error"] = f"Validation error: {str(e)}"
        
        return result
    
    def should_refuse_query(self, query: str) -> bool:
        """Determine if a query should be refused"""
        validation = self.validate_query(query)
        return not validation["is_valid"] or not validation["is_safe"]

