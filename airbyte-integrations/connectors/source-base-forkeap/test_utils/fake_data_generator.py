from source_base_forkeap.model import contact
from faker import Faker
from random import  random, choice
from typing import Optional

fake = Faker()

def fake_address(field: Optional[str] = None) -> contact.Address:

    if not field:
        field = choice(["ADDRESS_FIELD_UNSPECIFIED", "BILLING", "SHIPPING", "OTHER"])
    
    # Required fields
    address = contact.Address(
        country=fake.country(),
        field=field,
        line1=fake.street_address(),
        locality=fake.city(),
        postal_code=fake.postcode()
    )

    # Optional fields
    # Line 2
    if  random() > 0.5:
        address.line2 = fake.secondary_address()
    # Country code
    if random() > 0.5:
        address.country_code = fake.country_code()
        # Region

    # TODO: Region and region_code (ISO 3166-2)

    # Zip code
    if random() > 0.5:
        address.zip_code = fake.zipcode()
    # Zip four
    if random() > 0.5:
        address.zip_four = fake.zipcode_plus4()

    address.validate()

    return address

# Fake Company
def fake_company() -> contact.Company:
    company = contact.Company(
        id=fake.uuid4()
    )

    # Optional fields
    if random() > 0.5:
        company.company_name = fake.company()

    company.validate()
    
    return company

def fake_fax_number(field: Optional[str] = None) -> contact.FaxNumber:

    if not field:
        field = choice(["FAX_NUMBER_FIELD_UNSPECIFIED", "FAX1", "FAX2"])
    
    # Required fields
    fax_number = contact.FaxNumber(
        field=field,
        number=fake.msisdn(),
        type=fake.word()
    )

    fax_number.validate()

    return fax_number

def fake_custom_field_value() -> contact.CustomFieldValue:
    custom_field_value = contact.CustomFieldValue(
        id=fake.uuid4(),
        content=fake.word()
    )

    custom_field_value.validate()

    return custom_field_value

def fake_email_address(field: Optional[str] = None) -> contact.EmailAddress:

    if not field:
        field = choice(["EMAIL1", "EMAIL2", "EMAIL3"])
    
    # Required fields
    email_address = contact.EmailAddress(
        field=field,
        email=fake.email(),
    )

    if random() > 0.5:
        email_address.opt_in_reason = fake.sentence()

    email_address.validate()

    return email_address

def fake_origin_request() -> contact.OriginRequest:
    origin_request = contact.OriginRequest(
        ip_address=choice([fake.ipv4(), fake.ipv6()])
    )

    origin_request.validate()

    return origin_request

def fake_phone_number(field: Optional[str] = None) -> contact.PhoneNumber:

    if not field:
        field = choice(["PHONE_NUMBER_FIELD_UNSPECIFIED", "PHONE1", "PHONE2", "PHONE3", "PHONE4", "PHONE5"])
    
    # Required fields
    phone_number = contact.PhoneNumber(
        field=field,
        number=fake.msisdn(),
        type=fake.word()
    )

    phone_number.validate()

    return phone_number

def fake_social_account(type: Optional[str] = None) -> contact.SocialAccount:

    if not type:
        type = choice(["SOCIAL_ACCOUNT_TYPE_UNSPECIFIED", "FACEBOOK", "LINKED_IN", "TWITTER", "INSTAGRAM", "SNAPCHAT", "YOUTUBE",
                       "PINTEREST"])

    social_account = contact.SocialAccount(
            name = fake.word(),
            type = type
            )

    social_account.validate()

    return social_account

def fake_utm_parameter() -> contact.UtmParameter:
    
    utm_parameter = contact.UtmParameter()

    if random() > 0.5:
        utm_parameter.keap_source_id = fake.uuid4()

    if random() > 0.5:
        utm_parameter.utm_campaing = fake.word()

    if random() > 0.5:
        utm_parameter.utm_content = fake.word()

    if random() > 0.5:
        utm_parameter.utm_medium = fake.word()

    if random() > 0.5:
        utm_parameter.utm_source = fake.word()

    if random() > 0.5:
        utm_parameter.utm_term = fake.word()

    utm_parameter.validate()

    return utm_parameter

