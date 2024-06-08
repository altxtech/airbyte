#
# Copyright (c) 2024 Airbyte, Inc., all rights reserved.
#

import logging

from typing import Any, Iterable, Mapping
 
from airbyte_cdk.destinations import Destination
from airbyte_cdk.models import AirbyteConnectionStatus, AirbyteMessage, ConfiguredAirbyteCatalog, Status, Type
from airbyte_cdk.models.airbyte_protocol import AirbyteControlMessage, AirbyteControlConnectorConfigMessage

import requests
from time import time
from datetime import datetime, timedelta
import os
import json

'''
Things to worry about at some point (not today):
    - idempotency
    - Error handling
    - Rate limiting
    - Data validation
    - Async requests
    - Retry / Exponential backoff
    - Code reorganization and unit tests
'''

class DestinationKeap(Destination):
    def write(
        self, config: Mapping[str, Any], configured_catalog: ConfiguredAirbyteCatalog, input_messages: Iterable[AirbyteMessage]
    ) -> Iterable[AirbyteMessage]:

        # Logger
        logger = logging.getLogger("airbyte")


        # Refresh Auth
        logger.info("Refreshing access token...")
        form = {"grant_type": "refresh_token", "refresh_token": config["refresh_token"]}
        auth = (config["client_id"], config["client_secret"])
        r = requests.post("https://api.infusionsoft.com/token", auth = auth, data = form)
        r.raise_for_status()

        # Update and store configuration
        logger.info("Token refresh successfull. Updating connector config.")
        config["access_token"] = r.json()["access_token"]
        config["refresh_token"] = r.json()["refresh_token"]
        config["expires_at"] = (datetime.utcnow() + timedelta(seconds=r.json()["expires_in"])).isoformat() + "Z" 

        # Update the configuration with a control message
        control_message = AirbyteMessage(
                type = "CONTROL",
                control = AirbyteControlMessage(
                    type = "CONNECTOR_CONFIG",
                    emitted_at = time(),
                    connectorConfig = AirbyteControlConnectorConfigMessage(
                        config = config
                    )
                )
        )

        if os.environ.get("ENV") == "dev":
            with open("secrets/config.json", "w") as f:
                json.dump(config, f)

        yield control_message


        for message in input_messages:

            logger.info(f"Received {message.type} message")
            
            if message.type == Type.STATE:
                logger.info("STATE message received. Confirming.")
                yield message

            elif message.type == Type.RECORD:

                logger.info("RECORD message received. Validating data.")
                data = message.record.data

                # TODO - Here we should do some data validation.
                # - The data should match the schema expected by this destination
                # - Should specify a supported action / resource
                # - The payload should match the specified resource
                
                if data["resource"] == "contact":

                    payload = data["payload"]

                    logger.info("Sync contact identified")
                    
                    logger.info("Identifying deduplication email")

                    # Identify the priority email to search the user by
                    email_dict = {email["field"]: email["email"] for email in payload["email_addresses"]}

                    # Default priority is personal_email > work_email > other_email
                    email_priority = ["EMAIL2", "EMAIL1", "EMAIL3"]

                    # Email specified in the configuration overrides default priority
                    dedup_key = config.get("contact_deduplication_key")
                    if dedup_key in ["work_email", "personal_email", "other_email"]:
                        email_field_map = {"work_email": "EMAIL1", "personal_email": "EMAIL2", "other_email": "EMAIL3"}
                        email_priority.insert(0, email_field_map["dedup_key"])

                    email = None
                    for field in email_priority:
                        email = email_dict.get(field)
                        if email != None:
                            break

                    # Search for existing contacts
                    logger.info("Searching for existing contacts")
                    header = {"Authorization": "Bearer " + config["access_token"]}
                    query = {"filter": f"email=={email}"}
                    r = requests.get("https://api.infusionsoft.com/crm/rest/v2/contacts", headers=header, params=query)
                    r.raise_for_status()

                    found_contacts = r.json()["contacts"]
                    if len(found_contacts) == 0:
                        logger.info("Contact does not exist. Creating.")
                        r = requests.post("https://api.infusionsoft.com/crm/rest/v2/contacts", headers=header, json=payload)
                        r.raise_for_status()
                        logger.info(f"Created contact with id: {r.json()['id']}")

                    else:

                        id = found_contacts[0]["id"]
                        logger.info("Found existing contact. Updating.")

                        # Raise a warning if there are more than one contacts were found
                        if len(found_contacts) > 1:
                            logger.warning(f"Multiple contacts were found with the email {email}. The connector will default to updating the first one found, but errors may occur")

                        r = requests.patch(f"https://api.infusionsoft.com/crm/rest/v2/contacts/{id}", headers=header, json=payload)
                        r.raise_for_status()


                            

                elif data["resource"] == "api_goal":
                    pass
                    
                


        




    def check(self, logger: logging.Logger, config: Mapping[str, Any]) -> AirbyteConnectionStatus:

        '''
        Ideally, we would want to refresh the access token to make sure all credentials are valid and fresh.

        However, we can't update the destination configuration from the check method.

        So, the best we can do is to make an API call to at least make sure the access token is valid.
        '''
        try:

            r = requests.get("https://api.infusionsoft.com/crm/rest/v2/businessProfile", headers = {"Authorization": "Bearer " + config["access_token"]})
            r.raise_for_status()


            if r.headers['x-keap-tenant-id'].split(".")[0] != config["keap_app_id"]:
                raise Exception("Provided Keap App ID does not match with tenant ID")
            
            return AirbyteConnectionStatus(status=Status.SUCCEEDED)

        except Exception as e:
            return AirbyteConnectionStatus(status=Status.FAILED, message=f"An exception occurred: {repr(e)}")
