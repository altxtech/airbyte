import pytest
from source_base_forkeap.model.exceptions import ValidationError
from source_base_forkeap.model.contact import (
        Company
)

def test_valid_company1():
    Company(id="1")

def test_valid_company2():
    Company(id="1", company_name="ACME")

def test_invalid_id():
    with pytest.raises(ValidationError) as exc_info:
        Company(id="foo")
    assert exc_info.value.field == "id"
