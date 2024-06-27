import pytest
from source_base_forkeap.model.exceptions import ValidationError
from source_base_forkeap.model.contact import (
        Contact,
        EmailAddress
)

def test_email_address_repeated_field():
    
    # Emails should have unique "field" 
    emails = [
            EmailAddress(field="EMAIL1", email="test1@example.com"),
            EmailAddress(field="EMAIL1", email="test2@example.com")
    ]

    # Should fail
    with pytest.raises(ValidationError) as exc_info:
        Contact(email_addresses=emails)

    assert exc_info.value.message == "Email field 'EMAIL1' is repeated"
    assert exc_info.value.field == "email_addresses"
