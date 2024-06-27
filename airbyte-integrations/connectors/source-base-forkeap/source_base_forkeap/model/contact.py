from .base import Base
from .exceptions import ValidationError
from dataclasses import dataclass
from typing import List, Optional, Any
from datetime import datetime, date, timezone
import re

'''
Note to self:

This right here is cool to do, but it's very easy to endup overegineering this
'''

@dataclass
class Address(Base):
    country: str
    field: str
    line1: str
    locality: str
    postal_code: str
    line2: Optional[str] = None
    country_code: Optional[str] = None
    region: Optional[str] = None
    region_code: Optional[str] = None
    zip_code: Optional[str] = None
    zip_four: Optional[str] = None

    def validate(self):
        # If region is specified, country_code is required
        if self.region and not self.country_code:
            raise ValidationError("Country code is required when region is specified", "contry_code")

@dataclass
class Company(Base):
    id: str
    company_name: Optional[str] = None

    def validate(self):
        if not self.id:
            raise ValidationError("Company ID is required", "id")

@dataclass
class FaxNumber(Base):
    field: str
    number: str
    type: str

    def validate(self):

        if self.field not in ["FAX1", "FAX2", "FAX_NUMBER_FIELD_UNSPECIFIED"]:
            raise ValidationError("Invalid fax number field", "field")

        if not re.match(r"\+?[0-9]+", self.number):
            raise ValidationError("Invalid fax number", "number")

@dataclass
class CustomFieldValue(Base):
    id: str
    content: Any 

    def validate(self):
        pass

@dataclass
class EmailAddress(Base):
    email: str
    field: str
    opt_in_reason: Optional[str] = None

    def validate(self):
        if not self.email:
            raise ValidationError("Email address is required", "email")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValidationError("Invalid email address", "email")

        if self.field not in ["EMAIL1", "EMAIL2", "EMAIL3"]:
            raise ValidationError(f"Invalid email field", "field")

@dataclass
class OriginRequest(Base):
    ip_address: str

    def validate(self):

        ipv4_re = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}" 
        ipv6_re = r"(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"

        if not re.match(ipv4_re, self.ip_address):
            if not re.match(ipv6_re, self.ip_address):
                raise ValidationError("Invalid IP address", "ip_address")

@dataclass
class PhoneNumber(Base):
    extension: Optional[str] = None
    field: Optional[str] = None
    number: Optional[str] = None
    type: Optional[str] = None
    
    def validate(self):

        if self.number:
            if not re.match(r"\+?[0-9]+", self.number):
                raise ValidationError("Invalid phone number", "number")

        if self.field not in ["PHONE_NUMBER_FIELD_UNSPECIFIED", "PHONE1", "PHONE2", "PHONE3", "PHONE4", "PHONE5"]:
            raise ValidationError("Invalid phone number field", "field")

@dataclass
class SocialAccount:

    name: str
    type: str

    def validate(self):
        if self.type not in ["SOCIAL_ACCOUNT_TYPE_UNSPECIFIED", "FACEBOOK", "LINKED_IN", "TWITTER", "INSTAGRAM", "SNAPCHAT", "YOUTUBE", "PINTEREST"]:
            raise ValidationError("Invalid social account type", "type")

@dataclass
class UtmParameter:
    keap_source_id: str
    utm_campaing: Optional[str] = None
    utm_content: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_source: Optional[str] = None
    utm_term: Optional[str] = None

    def validate(self):
        pass

@dataclass
class Contact(Base):
    addresses: Optional[List[Address]] = None
    anniversary_date: Optional[date] = None
    birth_date: Optional[date] = None
    company: Optional[Company] = None
    contact_type: Optional[str] = None
    custom_fields: Optional[List[CustomFieldValue]] = None
    email_addresses: Optional[List[EmailAddress]] = None
    family_name: Optional[str] = None
    fax_numbers: Optional[List[FaxNumber]] = None
    given_name : Optional[str] = None
    job_title: Optional[str] = None
    lead_source_id: Optional[str] = None
    middle_name: Optional[str] = None
    origin_request: Optional[OriginRequest] = None
    owner_id: Optional[str] = None
    phone_numbers: Optional[List[PhoneNumber]] = None
    preffered_locale: Optional[str] = None
    preffered_name: Optional[str] = None
    prefix: Optional[str] = None
    referral_code: Optional[str] = None
    social_accounts: Optional[List[SocialAccount]] = None
    spouse_name: Optional[str] = None
    suffix: Optional[str] = None
    timezone: Optional[str] = None
    utm_parameters: Optional[UtmParameter] = None
    website: Optional[str] = None

    # Data validations

    def validate(self): # Raises an exception if the object is invalid

        # At least one email address
        if not self.email_addresses:
            raise ValidationError("At least one email address is required", "email_addresses")

        # Email addresses fields should not be repeated
        fields = {}
        for email in self.email_addresses:
            if email.field in fields:
                raise ValidationError(f"Email field '{email.field}' is repeated", "email_addresses")
            fields[email.field] = True
