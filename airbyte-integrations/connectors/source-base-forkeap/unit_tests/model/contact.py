import pytest
from source_base_forkeap.model.exceptions import ValidationError
from source_base_forkeap.model.contact import (
        Contact,
        Company,
        CustomFieldValue,
        Address,
        EmailAddress,
        FaxNumber,
        OriginRequest
)
from datetime import date

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

def test_complete_contact_to_dict():

    # Tests the dict conversion of a complete contact object

    contact = Contact(
            addresses = [
                Address(
                    line1 = "123 Main St",
                    line2 = "Apt 1",
                    field = "BILLING",
                    locality = "Anytown",
                    postal_code = "12345",
                    country = "USA"
                )
            ],
            anniversary_date = date(2020, 1, 1),
            birth_date = date(1990, 1, 1),
            company = Company(
                company_name = "Test Company",
                id = "12345"
            ),
            contact_type = "lead",
            custom_fields = [
                CustomFieldValue(
                    id = "12345",
                    content = "test"
                )
            ],
            email_addresses = [
                EmailAddress(
                    field = "EMAIL1",
                    email = "john.doe@example.com"
                ),
                EmailAddress(
                    field = "EMAIL2",
                    email = "john.doe1@example.com"
                )
            ],
            family_name="Doe",
            fax_numbers = [
                FaxNumber(
                    field = "FAX1",
                    number = "123-456-7890",
                    type = "home"
                )
            ],
            given_name = "John",
            job_title = "CEO",
            lead_source_id = "12345",
            middle_name = "D",
            origin_request = OriginRequest(
                ip_address = "0.0.0.0",
            ),
            owner_id = "12345",
            preffered_locale = "en_US",
            preffered_name = "John Doe",
            prefix = "Mr.",
            referral_code = "12345",
            spouse_name = "Jane",
            suffix = "Jr.",
            timezone = "America/New_York",
            website = "https://example.com"
    )

    expect = {
            "addresses": [
                {
                    "line1": "123 Main St",
                    "line2": "Apt 1",
                    "field": "BILLING",
                    "locality": "Anytown",
                    "postal_code": "12345",
                    "country": "USA"
                }
            ],
            "anniversary_date": "2020-01-01",
            "birth_date": "1990-01-01",
            "company": {
                "company_name": "Test Company",
                "id": "12345"
            },
            "contact_type": "lead",
            "custom_fields": [
                {
                    "id": "12345",
                    "content": "test"
                }
            ],
            "email_addresses": [
                {
                    "field": "EMAIL1",
                    "email": "john.doe@example.com"
                },
                {
                    "field": "EMAIL2",
                    "email": "john.doe1@example.com"
                }
            ],
            "family_name": "Doe",
            "fax_numbers": [
                {
                    "field": "FAX1",
                    "number": "123-456-7890",
                    "type": "home"
                }
            ],
            "given_name": "John",
            "job_title": "CEO",
            "lead_source_id": "12345",
            "middle_name": "D",
            "origin_request": {
                "ip_address": "0.0.0.0"
            },
            "owner_id": "12345",
            "preffered_locale": "en_US",
            "preffered_name": "John Doe",
            "prefix": "Mr.",
            "referral_code": "12345",
            "spouse_name": "Jane",
            "suffix": "Jr.",
            "timezone": "America/New_York",
            "website": "https://example.com"
    }

    assert contact.to_dict() == expect
