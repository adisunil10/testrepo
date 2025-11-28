"""Tests for guardrails module"""
import pytest
from src.guardrails import Guardrails, QueryValidation


def test_query_validation():
    """Test query validation"""
    # Valid query
    valid_query = QueryValidation(query="What is the return policy?")
    assert valid_query.query == "What is the return policy?"
    
    # Empty query should fail
    with pytest.raises(ValueError):
        QueryValidation(query="")
    
    # Too long query should fail
    long_query = "a" * 1000
    with pytest.raises(ValueError):
        QueryValidation(query=long_query, max_length=500)


def test_unsafe_patterns():
    """Test unsafe pattern detection"""
    query = QueryValidation(query="How do I delete my account?")
    safety_check = query.check_unsafe_patterns()
    assert safety_check["is_safe"] == False
    assert "delete" in safety_check["found_patterns"]


def test_guardrails():
    """Test guardrails system"""
    guardrails = Guardrails(enable_guardrails=True)
    
    # Safe query
    result = guardrails.validate_query("What is the return policy?")
    assert result["is_valid"] == True
    assert result["is_safe"] == True
    
    # Unsafe query
    result = guardrails.validate_query("How do I delete everything?")
    assert result["is_safe"] == False

