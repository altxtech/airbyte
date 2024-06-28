import pytest
from source_base_forkeap.model.exceptions import ValidationError
from source_base_forkeap.model.contact import (
        EmailAddress
)

def test_field_is_required():
    with pytest.raises(TypeError):
        EmailAddress()

def test_invalid_field():
    with pytest.raises(ValidationError) as exc_info:
        EmailAddress(field="INVALID", email="test@example.com")

    assert exc_info.value.field == "field"

def test_invalid_field2():
    # EMAIL_FIELD_UNSPECIFIED is not valid, despite being in the docs
    with pytest.raises(ValidationError) as exc_info:
        EmailAddress(field="EMAIL_FIELD_UNSPECIFIED", email="test@example.com")

    assert exc_info.value.field == "field"

def test_invalid_email():
    with pytest.raises(ValidationError) as exc_info:
        EmailAddress(field="EMAIL1", email="invalid")
    assert exc_info.value.field == "email"

def test_valid_email():
    # Should not raise any exceptions
    EmailAddress(field="EMAIL1", email="test@example.com", opt_in_reason="Test")
