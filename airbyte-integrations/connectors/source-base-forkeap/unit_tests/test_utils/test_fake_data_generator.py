from source_base_forkeap.model import contact
import test_utils.fake_data_generator as gen 

def test_create_fake_address():
    fake_address = gen.fake_address()
    assert isinstance(fake_address, contact.Address)

def test_create_fake_address_with_field():
    fake_address = gen.fake_address("BILLING")
    assert isinstance(fake_address, contact.Address)
    assert fake_address.field == "BILLING"

def test_create_fake_company():
    fake_company = gen.fake_company()
    assert isinstance(fake_company, contact.Company)

def test_create_fake_fax_number():
    fake_fax_number = gen.fake_fax_number()
    assert isinstance(fake_fax_number, contact.FaxNumber)

def test_create_fake_fax_number_with_field():
    fake_fax_number = gen.fake_fax_number("FAX1")
    assert isinstance(fake_fax_number, contact.FaxNumber)
    assert fake_fax_number.field == "FAX1"

def test_create_fake_custom_field_value():
    fake_custom_field_value = gen.fake_custom_field_value()
    assert isinstance(fake_custom_field_value, contact.CustomFieldValue)

def test_create_fake_email_address():
    fake_email_address = gen.fake_email_address()
    assert isinstance(fake_email_address, contact.EmailAddress)

def test_create_fake_email_address_with_field():
    fake_email_address = gen.fake_email_address("EMAIL1")
    assert isinstance(fake_email_address, contact.EmailAddress)
    assert fake_email_address.field == "EMAIL1"

def test_create_fake_origin_request():
    fake_origin_request = gen.fake_origin_request()
    assert isinstance(fake_origin_request, contact.OriginRequest)

def test_create_fake_phone_number():
    fake_phone_number = gen.fake_phone_number()
    assert isinstance(fake_phone_number, contact.PhoneNumber)

def test_create_fake_phone_number_with_field():
    fake_phone_number = gen.fake_phone_number("PHONE1")
    assert isinstance(fake_phone_number, contact.PhoneNumber)
    assert fake_phone_number.field == "PHONE1"

def test_create_fake_social_account():
    fake_social_account = gen.fake_social_account()
    assert isinstance(fake_social_account, contact.SocialAccount)

def test_fake_social_account_with_type():
    fake_social_account = gen.fake_social_account("FACEBOOK")
    assert isinstance(fake_social_account, contact.SocialAccount)
    assert fake_social_account.type == "FACEBOOK"

def test_create_fake_utm_parameter():
    fake_utm_parameter = gen.fake_utm_parameter()
    assert isinstance(fake_utm_parameter, contact.UtmParameter)
