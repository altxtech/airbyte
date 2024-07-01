
import pytest
from source_base_forkeap.model.exceptions import ValidationError
from source_base_forkeap.model.contact import (
        SocialAccount
)

def test_valid_social_account():
    valid_types = [
            "FACEBOOK", "LINKED_IN", "TWITTER", "INSTAGRAM", "SNAPCHAT", "YOUTUBE", "PINTEREST"
    ]
    for t in valid_types:
        SocialAccount(type=t, name="http://example.com")

# Invalid type
def test_invalid_type1():
    with pytest.raises(ValidationError) as exc_info:
        SocialAccount(type="foo", name="http://example.com")
    assert exc_info.value.field == "type"

def test_invalid_type2():
    with pytest.raises(ValidationError) as exc_info:
        SocialAccount(type="SOCIAL_ACCOUNT_TYPE_UNSPECIFIED", name="http://example.com")
    assert exc_info.value.field == "type"

# Invalid name
def test_invalid_name1():
    with pytest.raises(ValidationError) as exc_info:
        SocialAccount(type="LINKED_IN", name="foo")
    assert exc_info.value.field == "type"

def test_invalid_name2():
    with pytest.raises(ValidationError) as exc_info:
        SocialAccount(type="LINKED_IN", name="example.com") # No protocol
    assert exc_info.value.field == "type"
