from source_base_forkeap.model import contact
from faker import Faker
from random import  random, choice, randint, sample
from typing import Optional, List
from datetime import date
import pycountry

fake = Faker()
MAX_ID = 2**64//2-1

def fake_address(field: Optional[str] = None) -> contact.Address:

    if not field:
        field = choice(["BILLING", "SHIPPING", "OTHER"])
    
    country = choice(list(pycountry.countries))

    address = contact.Address(
        field = field, 
        country_code = country.alpha_3
    )

    # Country
    if random() > 0.5:
        address.country = fake.country()

    # Line 1
    if random() > 0.5:
        address.line1 = fake.address()

    # city
    if random() > 0.5:
        address.locality = fake.city()

    # Postal code
    if random() > 0.5:
        address.postal_code = fake.postcode()

    # Line 2
    if  random() > 0.5:
        address.line2 = fake.secondary_address()

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
        id=str(randint(0,MAX_ID))
    )

    # Optional fields
    if random() > 0.5:
        company.company_name = fake.company()

    company.validate()
    
    return company

def fake_fax_number(field: Optional[str] = None) -> contact.FaxNumber:

    if not field:
        field = choice(["FAX1", "FAX2"])
    
    # Required fields
    fax_number = contact.FaxNumber(
        field=field,
        number=fake.phone_number(),
    )

    # Optional fields
    if random() > 0.5:
        fax_number.type = choice(["Work", "Home", "Other"])

    fax_number.validate()

    return fax_number

def fake_custom_field_value() -> contact.CustomFieldValue:
    custom_field_value = contact.CustomFieldValue(
        id=str(randint(0,MAX_ID)),
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
        field = choice(["PHONE1", "PHONE2", "PHONE3", "PHONE4", "PHONE5"])
    
    # Required fields
    phone_number = contact.PhoneNumber(
        field=field,
        number=fake.phone_number(),
    )
    
    # Optional fields
    if random() > 0.5:
        phone_number.type = choice(["Work", "Home", "Mobile", "Other"])

    phone_number.validate()

    return phone_number

def fake_social_account(type: Optional[str] = None) -> contact.SocialAccount:

    if not type:
        type = choice(["FACEBOOK", "LINKED_IN", "TWITTER", "INSTAGRAM", "SNAPCHAT", "YOUTUBE",
                       "PINTEREST"])

    social_account = contact.SocialAccount(
        name = fake.url() + fake.uri_path(),
        type = type
    )

    social_account.validate()

    return social_account

def fake_utm_parameter() -> contact.UtmParameter:
    
    utm_parameter = contact.UtmParameter(keap_source_id=fake.uuid4())

    if random() > 0.5:
        utm_parameter.utm_campaign = fake.word()

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

def fake_contact(with_company: Optional[bool] = False, with_custom_fields: Optional[bool] = False):

    # Contact needs at least one email address
    email_addresses: List[contact.EmailAddress] = []
    # Choose for which field to generate emails for (fields shouldn't be repeated)
    valid_fields = ["EMAIL1", "EMAIL2", "EMAIL3"]
    fields = sample(valid_fields, k=randint(1,3))
    for field in fields:
        email_addresses.append(fake_email_address(field))

    f_contact = contact.Contact(email_addresses = email_addresses)

    # Addresses
    valid_fields = ["BILLING", "SHIPPING", "OTHER"]
    fields = sample(valid_fields, randint(0,2))
    addresses: List[contact.Address] = []
    if fields:
        for field in fields:
            addresses.append(fake_address(field=field))
        f_contact.addresses = addresses

    if addresses:
        f_contact.addresses = addresses

    if random() > 0.5:
        f_contact.anniversary_date = date.fromisoformat(fake.date())

    if random() > 0.5:
        f_contact.birth_date = date.fromisoformat(fake.date())

    if random() > 0.5:
        f_contact.contact_type = choice(["Lead", "Customer", "Other"])

    if random() > 0.5:
        f_contact.family_name =  fake.last_name()

    valid_fields = ["FAX1", "FAX2"]
    fields = sample(valid_fields, randint(0,2))
    fax_numbers: List[contact.FaxNumber] = []
    if fields:
        for field in fields:
            fax_numbers.append(fake_fax_number(field=field))
        f_contact.fax_numbers = fax_numbers

    if fax_numbers:
        f_contact.fax_numbers = fax_numbers
    
    if random() > 0.5:
        f_contact.given_name = fake.first_name()

    if random() > 0.5:
        f_contact.job_title = fake.job()

    if random() > 0.5:
        f_contact.leadsource_id = str(randint(0, MAX_ID))

    if random() > 0.5:
        f_contact.middle_name = fake.last_name()

    if random() > 0.5:
        f_contact.origin = fake_origin_request()

    if random() > 0.5:
        f_contact.owner_id = str(randint(0, MAX_ID))

    valid_fields = ["PHONE1", "PHONE2", "PHONE3", "PHONE4", "PHONE5"]
    fields = sample(valid_fields, randint(0,5))
    phone_numbers: List[contact.PhoneNumber] = []
    if fields:
        for field in fields:
            phone_numbers.append(fake_phone_number(field=field))
        f_contact.phone_numbers = phone_numbers

    if random() > 0.5:
        f_contact.preferred_name = fake.name()

    if random() > 0.5:
        f_contact.prefix = choice(['Mr.', 'Mrs.', 'Ms.', "Dr."])

    if random() > 0.5:
        f_contact.referral_code = fake.uuid4()

    valid_types = ["FACEBOOK", "LINKED_IN", "TWITTER", "INSTAGRAM", "SNAPCHAT", "YOUTUBE", "PINTEREST"]
    types = sample(valid_types, randint(0,7))
    social_accounts: List[contact.SocialAccount] = []
    if types:
        for type in types:
            social_accounts.append(fake_social_account(type=type))
        f_contact.social_accounts = social_accounts

    if random() > 0.5:
        f_contact.spouse_name = fake.name()

    if random() > 0.5:
        f_contact.suffix = choice(["Jr", "PhD", "I", "II", "III", "IV", "V"])

    if random() > 0.5:
        f_contact.utm_parameters = fake_utm_parameter()

    if random() > 0.5:
        f_contact.website = fake.url()

    if with_company:
        f_contact.company = fake_company()

    if with_custom_fields:
        custom_fields: List[contact.CustomFieldValue] = []
        for _ in range(randint(1,2)):
            custom_fields.append(fake_custom_field_value())
        f_contact.custom_fields = custom_fields

    f_contact.validate()

    return f_contact
