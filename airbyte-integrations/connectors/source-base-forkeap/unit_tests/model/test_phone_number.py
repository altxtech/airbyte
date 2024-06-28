import pytest
from source_base_forkeap.model.exceptions import ValidationError
from source_base_forkeap.model.contact import (
        PhoneNumber
)

def test_phone_missing_field():
    with pytest.raises(TypeError):
        PhoneNumber(number="123-456-7890", type="Home")

def test_phone_invalid_field():
    # Valid values for field are PHONE1...PHONE5
    with pytest.raises(ValidationError) as exc_info:
        PhoneNumber(field="INVALID", number="123-456-7890", type="Home")
    assert exc_info.value.field == "field"

def test_phone_invalid_field2():
    # PHONE_NUMBER_FIELD_UNSPECIFIED is invalid
    with pytest.raises(ValidationError) as exc_info:
        PhoneNumber(field="PHONE_NUMBER_FIELD_UNSPECIFIED", number="123-456-7890", type="Home")
    assert exc_info.value.field == "field"

def test_phone_valid_type():
    with pytest.raises(ValidationError) as exc_info:
        PhoneNumber(field="PHONE1", number="123-456-7890", type="invalid")
    assert exc_info.value.field == "type"

# The Keap API will literally accept any garbage for phone numbers and extensions
# But I decided to make this class more strict than the API in case they add validation in the future

def test_phone_invalid_number():
    # Phone number must be in the format XXX-XXX-XXXX
    with pytest.raises(ValidationError) as exc_info:
        PhoneNumber(field="PHONE1", number="invalid", type="Home")
    assert exc_info.value.field == "number"

def test_phone_invalid_extension():
    with pytest.raises(ValidationError) as exc_info:
        PhoneNumber(field="PHONE1", number="123-456-7890", type="Home", extension="invalid")
    assert exc_info.value.field == "extension"

def test_phone_valid():
    # Should not raise any exceptions
    PhoneNumber(field="PHONE1", number="123-456-7890", type="Home")

