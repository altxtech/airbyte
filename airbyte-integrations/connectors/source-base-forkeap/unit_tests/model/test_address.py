import pytest
from source_base_forkeap.model.exceptions import ValidationError
from source_base_forkeap.model.contact import (
        Address
)
import pycountry

def test_valid_address_field():
    valid_fields = ["BILLING", "SHIPPING", "OTHER"]
    for f in valid_fields:
        Address(field = f, country_code="USA")

def test_invalid_field1():
    with pytest.raises(ValidationError) as exc_info:
        Address(field = "foo", country_code="USA")
    assert exc_info.value.field == "field"


def test_invalid_field2():
    with pytest.raises(ValidationError) as exc_info:
        Address(field = "ADDRESS_FIELD_UNSPECIFIED", country_code="USA")
    assert exc_info.value.field == "field"

def test_valid_country_codes():
    for country in pycountry.countries:
        Address(field = "BILLING", country_code=country.alpha_3)

def test_valid_region_codes():
    for region in pycountry.subdivisions:
        Address(field = "BILLING", country_code=region.country.alpha_3, region_code=region.code)

def test_invalid_country_code():
    with pytest.raises(ValidationError) as exc_info:
        Address(field = "BILLING", country_code="foo")
    assert exc_info.value.field == "country_code"

def test_invalid_region_code():
    with pytest.raises(ValidationError) as exc_info:
        # There are both valid ISO country and region codes, but US-AZ is not a region of BRA
        Address(field = "BILLING", country_code="BRA", region_code="US-AZ")
    assert exc_info.value.field == "country_code"

# There is a lot of crazy validation I could do on address, but I'll keep things simple for now
