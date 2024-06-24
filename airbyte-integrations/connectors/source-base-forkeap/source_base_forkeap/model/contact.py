from model.base import Base
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
            raise ValueError("Country code is required when region is specified")

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
            raise ValueError("Company ID is required")

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
            raise ValueError(f"Invalid fax number type")

        if not re.match(r"\+?[0-9]+", self.number):
            raise ValueError("Invalid fax number")

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
            raise ValueError("Email address is required")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValueError("Invalid email address")

        if self.field not in ["EMAIL1", "EMAIL2", "EMAIL3"]:
            raise ValueError(f"Invalid email field")

    def to_dict(self) -> dict:
        d = {"email": self.email, "field": self.field}
        if self.opt_in_reason:
            d["opt_in_reason"] = self.opt_in_reason
        return d

@dataclass
class OriginRequest(Base):
    ip_address: str

    def validate(self):
        if not re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", self.ip_address):
            raise ValueError("Invalid IP address")

    def to_dict(self) -> dict:
        return {"ip_address": self.ip_address}

@dataclass
class SocialAccount:

    name: str
    type: str

    def validate(self):
        if self.type not in ["SOCIAL_ACCOUNT_TYPE_UNSPECIFIED", "FACEBOOK", "LINKED_IN", "TWITTER", "INSTAGRAM", "SNAPCHAT", "YOUTUBE", "PINTEREST"]:
            raise ValueError("Invalid social account type")

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
    phone_numbers: Optional[List[str]] = None
    preffered_locale: Optional[str] = None
    preffered_name: Optional[str] = None
    prefix: Optional[str] = None
    referral_code: Optional[str] = None
    social_accounts: Optional[List[SocialAccount]] = None
    spouse_name: Optional[str] = None
    suffix: Optional[str] = None
    timezone: Optional[str] = None
    utm_parameters: Optional[List[UtmParameter]] = None
    website: Optional[str] = None

    # Data validations

    def validate(self): # Raises an exception if the object is invalid

        # At least one email address
        if not self.email_addresses:
            raise ValueError("At least one email address is required")

    def to_dict(self) -> dict:

        d = {}

        if self.email_addresses:
            d["email_addresses"] = [a.to_dict() for a in self.email_addresses]

        return d
