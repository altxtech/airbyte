from os import kill
from .base import Base
from .exceptions import ValidationError
from dataclasses import dataclass
from typing import List, Optional, Any
from datetime import datetime, date, timezone
import re
import pycountry

'''
Note to self:

This right here is cool to do, but it's very easy to endup overegineering this
'''

@dataclass
class Address(Base):
    field: str
    country_code: str
    line1: Optional[str] = None
    locality: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    line2: Optional[str] = None
    region: Optional[str] = None
    region_code: Optional[str] = None
    zip_code: Optional[str] = None
    zip_four: Optional[str] = None

    def validate(self):
        
        valid_fields = ["BILLING", "SHIPPING", "OTHER"]
        if self.field not in valid_fields:
            raise ValidationError(f"Invalid field: {self.field}", "field")
        
        # Validate country and region
        country = pycountry.countries.get(alpha_3=self.country_code)
        if not country:
            raise ValidationError(f"Invalid country code: f{self.country_code}", "country_code")

        if self.region_code:
            region = pycountry.subdivisions.get(code=self.region_code)

            if not region:
                raise ValidationError(f"Invalid region code: {self.region_code}", "region_code")

            if region.country != country:
                raise ValidationError(f"Region {self.region_code} is not a subdivision of {self.country_code}", "region_code")

@dataclass
class Company(Base):

    # Decided to make id optional because we could potentially send just the company name and have the Keap destination figure out the id
    # downstream

    id: Optional[str]
    company_name: Optional[str] = None

    def validate(self):

        if not re.match(r"\d+", self.id):
            raise ValidationError("id should include only digits", "id") 

@dataclass
class FaxNumber(Base):
    field: str
    number: str
    type: Optional[str] = None

    def validate(self):

        if self.field not in ["FAX1", "FAX2"]:
            raise ValidationError("Invalid fax number field", "field")

        if not re.match(r"^(\+?\d{1,3}[\s-])?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}(x\d{1,5})?$", self.number):
            raise ValidationError("Invalid fax number", "number")
        
        if self.type:
            valid_types = ["Work", "Home", "Other"]
            if self.type not in valid_types:
                raise ValidationError(f"Valid types are {', '.join(valid_types)}", "type")

@dataclass
class CustomFieldValue(Base):

    # Differently from Company, custom field id should be required because:
    # 1 - Keap API requires it 
    # 2 - Would be 'hacky' for the Keap destination to figure out the id based on content only

    id: str
    content: Any 

    def validate(self):
        
        if not re.match(r"\d+", self.id):
            raise ValidationError("'id' should include only digits", "id")

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
    field: str
    number: str
    type: Optional[str] = None
    extension: Optional[str] = None
    
    def validate(self):

        if self.field not in ["PHONE1", "PHONE2", "PHONE3", "PHONE4", "PHONE5"]:
            raise ValidationError("Invalid phone number field", "field")

        if not re.match(r"^(\+?\d{1,3}[\s-])?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}(x\d{1,5})?$", self.number):
            raise ValidationError("Invalid phone number", "number")
        
        if self.type:
            valid_types = ["Work", "Home", "Mobile", "Other"]
            if self.type not in valid_types:
                raise ValidationError(f"Valid types are {', '.join(valid_types)}", "type")

        if self.extension:
            if not re.match(r"\d{1,5}", self.extension):
                raise ValidationError(f"Extension should be 1 to 5 digits", "extension")


@dataclass
class SocialAccount(Base):

    name: str
    type: str

    def validate(self):
        if self.type not in ["FACEBOOK", "LINKED_IN", "TWITTER", "INSTAGRAM", "SNAPCHAT", "YOUTUBE", "PINTEREST"]:
            raise ValidationError("Invalid social account type", "type")

        url_re = r"https?:\/\/\w+(\.\w+)+"
        if not re.match(url_re, self.name):
            raise ValidationError(f"{self.name} is not a valid url", "name")

@dataclass
class UtmParameter:
    keap_source_id: str
    utm_campaign: Optional[str] = None
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
    leadsource_id: Optional[str] = None
    middle_name: Optional[str] = None
    origin: Optional[OriginRequest] = None
    owner_id: Optional[str] = None
    phone_numbers: Optional[List[PhoneNumber]] = None

    # too hard to validate
    # preferred_locale: Optional[str] = None -> 

    preferred_name: Optional[str] = None
    prefix: Optional[str] = None
    referral_code: Optional[str] = None
    social_accounts: Optional[List[SocialAccount]] = None
    spouse_name: Optional[str] = None
    suffix: Optional[str] = None

    # too hard to validate
    # time_zone: Optional[str] = None

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

        # Phone numbers fiels should be not be repeated
        if self.phone_numbers:
            fields = {}
            for number in self.phone_numbers:
                if number.field in fields:
                    raise ValidationError(f"Phone field '{number.field}' is repeated", "phone_numbers")
                fields[number.field] = True

        if self.fax_numbers:
            fields = {}
            for number in self.fax_numbers:
                if number.field in fields:
                    raise ValidationError(f"Fax field '{number.field}' is repeated", "fax_numbers")
                fields[number.field] = True

        if self.social_accounts:
            fields = {}
            for acc in self.social_accounts:
                if acc.type in fields:
                    raise ValidationError(f"Fax field '{acc.type}' is repeated", "social_accounts")
                fields[acc.type] = True

        # Prefixes
        if self.prefix:
            valid_prefixes = ['Mr.', 'Mrs.', 'Ms.', "Dr."]
            if self.prefix not in valid_prefixes:
                raise ValidationError(f"Valid prefixes are {', '.join(valid_prefixes)}", "prefix")

        # Suffixes
        if self.suffix:
            valid_suffixes = ["Jr", "PhD", "I", "II", "III", "IV", "V"]
            if self.suffix not in valid_suffixes:
                raise ValidationError(f"Valid suffixes are {', '.join(valid_suffixes)}", "suffix")
        
        if self.contact_type:
            valid_contact_types = ["Lead", "Customer", "Other"]
            if self.contact_type not in valid_contact_types:
                raise ValidationError(f"Valid types are {', '.join(valid_contact_types)}", "contact_type")

        # Website
        if self.website:
            url_re = r"https?:\/\/\w+(\.\w+)+"
            if not re.match(url_re, self.website):
                raise ValidationError(f"{self.website} is not a valid url", "website")

