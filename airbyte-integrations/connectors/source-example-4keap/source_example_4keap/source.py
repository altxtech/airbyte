#
# Copyright (c) 2024 Airbyte, Inc., all rights reserved.
#


from abc import ABC
from typing import Any, Iterable, List, Mapping, MutableMapping, Optional, Tuple, Union

from airbyte_cdk.models import SyncMode
from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.streams import Stream
from airbyte_cdk.sources.streams.core import StreamData

from faker import Faker
import random


# Contact Stream
class Contacts(Stream):

    def __init__(self, unique_contacts: int, contacts_events: int, **kwargs):
        super().__init__(**kwargs)

        self.unique_contacts = unique_contacts
        self.contacts_events = contacts_events

    @property
    def primary_key(self) -> Optional[Union[str, List[str], List[List[str]]]]:
        return "" 

    def read_records(
        self,
        sync_mode: SyncMode,
        cursor_field: Optional[List[str]] = None,
        stream_slice: Optional[Mapping[str, Any]] = None,
        stream_state: Optional[Mapping[str, Any]] = None,
    ) -> Iterable[StreamData]:

        # Gen emails
        fake = Faker()
        emails = [fake.email() for _ in range(self.unique_contacts)]

        for _ in range(self.contacts_events):
            # Choose an email
            email = random.choice(emails)
            yield {"resource": "contact", "payload": self._gen_contact(email)}

    def _gen_contact(self, email):

        fake = Faker()

        contact = {
                # TODO: Addresses
                "anniversary_date": fake.date(),
                "birth_date": fake.date(),
                # TODO: Company - Probably will need custom logic on how to identify companies
                "contact_type": random.choice(["Lead", "Customer", "Other"]),
                # TODO: Custom fields,
                # TODO: better email gen
                "email_addresses": [
                    {"email": email, "field": "EMAIL2", "opt_in_reason": fake.text()}
                ],
                "family_name": fake.last_name(),
                # TODO: Fax numbers
                "given_name": fake.first_name(),
                "job_title": fake.job(),
                # TODO: leadsource_id - I don't know what this is, so better not to mess with it for now
                "middle_name": fake.last_name(),
                "origin": {
                    "ip_address": fake.ipv4()
                },
                # TODO: Phone numbers
                # TODO: preferred_locale - don't know what the API accepts
                "preferred_name": fake.name(),
                # TODO: prefix - Not sure what the API accepts
                "referral_code": fake.pystr(),
                # TODO: Social Accounts
                "source_type": random.choice([
                    "SOURCE_TYPE_UNSPECIFIED",
                    "API",
                    "APPOINTMENT",
                    "FORM_API_HOSTED",
                    "FORM_API_INTERNAL",
                    "IMPORT",
                    "INTERNAL_FORM",
                    "LANDING_PAGE",
                    "MANUAL",
                    "OTHER",
                    # "UNKOWN", - invalid
                    "WEBFORM"
                ]),
                "spouse_name": fake.name(),
                # TODO: suffix - Don't know what the API will accept
                # TODO: time_zone - Need to figure out what is accepted by the API
                # TODO: Utm parameters
                "website": fake.url()
        }

        return contact

        

        


# Source
class SourceExample_4keap(AbstractSource):
    def check_connection(self, logger, config) -> Tuple[bool, any]:
        """
        TODO: Implement a connection check to validate that the user-provided config can be used to connect to the underlying API

        See https://github.com/airbytehq/airbyte/blob/master/airbyte-integrations/connectors/source-stripe/source_stripe/source.py#L232
        for an example.

        :param config:  the user-input config object conforming to the connector's spec.yaml
        :param logger:  logger object
        :return Tuple[bool, any]: (True, None) if the input config can be used to connect to the API successfully, (False, error) otherwise.
        """
        return True, None

    def streams(self, config: Mapping[str, Any]) -> List[Stream]:
        """
        TODO: Replace the streams below with your own streams.

        :param config: A Mapping of the user input configuration as defined in the connector spec.
        """
        # TODO remove the authenticator if not required.
        return [Contacts(config["unique_contacts"], config["contacts_events"])]
