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

    def to_dict(self) -> dict:

        d = {
            "country": self.country,
            "field": self.field,
            "line1": self.line1,
"locality": self.locality,
            "postal_code": self.postal_code
        }

        if self.line2:
            d["line2"] = self.line2

        if self.country_code:
            d["country_code"] = self.country_code

        if self.region:
            d["region"] = self.region

        if self.region_code:
            d["region_code"] = self.region_code

        if self.zip_code:
            d["zip_code"] = self.zip_code

        if self.zip_four:
            d["zip_four"] = self.zip_four

        return d

@dataclass
class Company(Base):
    id: str
    company_name: Optional[str] = None

    def validate(self):
        if not self.id:
            raise ValidationError("Company ID is required", "id")

    def to_dict(self) -> dict:
        d = {"id": self.id}
        if self.company_name:
            d["company_name"] = self.company_name
        return d
    
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

    def to_dict(self) -> dict:
        return {"field": self.field, "number": self.number, "type": self.type}

@dataclass
class CustomFieldValue(Base):
    id: str
    content: Any 

    def validate(self):
        pass

    def to_dict(self) -> dict:
        return {"id": self.id, "content": self.content}

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

    def to_dict(self) -> dict:
        d = {"email": self.email, "field": self.field}
        if self.opt_in_reason:
            d["opt_in_reason"] = self.opt_in_reason
        return d

@dataclass
class OriginRequest(Base):
    ip_address: str

    def validate(self):

        ipv4_re = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}" 
        ipv6_re = r"(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"

        if not re.match(ipv4_re, self.ip_address):
            if not re.match(ipv6_re, self.ip_address):
                raise ValidationError("Invalid IP address", "ip_address")

    def to_dict(self) -> dict:
        return {"ip_address": self.ip_address}

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

    def to_dict(self) -> dict:
        return {
                "extension": self.extension,
                "field": self.field,
                "number": self.number,
                "type": self.type
        }

@dataclass
class SocialAccount:

    name: str
    type: str

    def validate(self):
        if self.type not in ["SOCIAL_ACCOUNT_TYPE_UNSPECIFIED", "FACEBOOK", "LINKED_IN", "TWITTER", "INSTAGRAM", "SNAPCHAT", "YOUTUBE", "PINTEREST"]:
            raise ValidationError("Invalid social account type", "type")

    def to_dict(self) -> dict:
        return {"name": self.name, "type": self.type}

class UtmParameter:
    keap_source_id: str
    utm_campaing: Optional[str] = None
    utm_content: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_source: Optional[str] = None
    utm_term: Optional[str] = None

    def validate(self):
        pass

    def to_dict(self) -> dict:
        d = {"keap_source_id": self.keap_source_id}
        if self.utm_campaing:
            d["utm_campaing"] = self.utm_campaing
        if self.utm_content:
            d["utm_content"] = self.utm_content
        if self.utm_medium:
            d["utm_medium"] = self.utm_medium
        if self.utm_source:
            d["utm_source"] = self.utm_source
        if self.utm_term:
            d["utm_term"] = self.utm_term

        return d

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

    def to_dict(self) -> dict:

        d = {
                "addresses": [addr.to_dict() for addr in self.addresses] if self.addresses else [],
                "anniversary_date": self.anniversary_date.isoformat() if self.anniversary_date else None,
                "birth_date": self.birth_date.isoformat() if self.birth_date else None,
                "company": self.company.to_dict() if self.company else None,
                "contact_type": self.contact_type,
                "custom_fields": [cf.to_dict() for cf in self.custom_fields] if self.custom_fields else [],
                "email_addresses": [ea.to_dict() for ea in self.email_addresses] if self.email_addresses else [],
                "family_name": self.family_name,
                "fax_numbers": [fn.to_dict() for fn in self.fax_numbers] if self.fax_numbers else [],
                "given_name": self.given_name,
                "job_title": self.job_title,
                "lead_source_id": self.lead_source_id,
                "middle_name": self.middle_name,
                "origin_request": self.origin_request.to_dict() if self.origin_request else None,
                "owner_id": self.owner_id,
                "phone_numbers": [pn.to_dict() for pn in self.phone_numbers] if self.phone_numbers else [],
                "preffered_locale": self.preffered_locale,
                "preffered_name": self.preffered_name,
                "prefix": self.prefix,
                "referral_code": self.referral_code,
                "social_accounts": [sa.to_dict() for sa in self.social_accounts] if self.social_accounts else [],
                "spouse_name": self.spouse_name,
                "suffix": self.suffix,
                "timezone": self.timezone,
                "utm_parameters": self.utm_parameters.to_dict() if self.utm_parameters else None,
                "website": self.website
        }

        # Remove None values
        d = {k: v for k, v in d.items() if v}

        return d
