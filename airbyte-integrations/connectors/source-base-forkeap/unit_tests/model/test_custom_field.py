import pytest
from source_base_forkeap.model.exceptions import ValidationError
from source_base_forkeap.model.contact import (
        CustomFieldValue
)

def test_valid_custom_field():
    CustomFieldValue(id="1", content="foo")

def test_invalid_id():
    with pytest.raises(ValidationError) as exc_info:
        CustomFieldValue(id="foo", content="foo")
    assert exc_info.value.field == "id"
