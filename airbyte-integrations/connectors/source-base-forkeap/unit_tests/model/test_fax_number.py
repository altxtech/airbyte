import pytest
from source_base_forkeap.model.exceptions import ValidationError
from source_base_forkeap.model.contact import (
        FaxNumber
)

def test_valid_fax_numbers():
    
    valid_fields = ["FAX1", "FAX2"]
    valid_types = [None, "Work", "Home", "Other"]

    for field in valid_fields:
        for type in valid_types:
            FaxNumber(field=field, type=type, number="(111) 111-1111")

def test_missing_field():
    with pytest.raises(TypeError):
        FaxNumber(number="(111) 111-1111")

def test_missing_number():
    with pytest.raises(TypeError):
        FaxNumber(field="FAX1")

def test_invalid_field1():
    with pytest.raises(ValidationError) as exc_info:
        FaxNumber(field="foo", number="(111) 111-1111")
    
    assert exc_info.value.field == "field"

def test_invalid_field2():
    with pytest.raises(ValidationError) as exc_info:
        FaxNumber(field="FAX_NUMBER_FIELD_UNSPECIFIED", number="(111) 111-1111")
    assert exc_info.value.field == "field"

def test_invalid_number():
    with pytest.raises(ValidationError) as exc_info:
        FaxNumber(field="FAX1", number="foo")
    assert exc_info.value.field == "number"
