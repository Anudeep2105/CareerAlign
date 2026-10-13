import pytest
from src.parser_manager import ParserFactory
from src.nlp.pii_filter import PIIFilter

def test_pii_filter():
    filter = PIIFilter(disabled_fields=["gender"])
    data = {"contact_details": {"name": "John Doe", "gender": "Male"}}
    result = filter.filter_data(data)
    assert result["contact_details"]["gender"] == "[REDACTED]"
    assert result["contact_details"]["name"] == "John Doe"

def test_parser_factory():
    # Mocking the parser calls for basic type check
    parser = ParserFactory.get_parser("test.txt")
    assert parser is not None
