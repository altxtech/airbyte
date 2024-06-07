#
# Copyright (c) 2024 Airbyte, Inc., all rights reserved.
#

import logging

from typing import Any, Iterable, Mapping
 
from airbyte_cdk.destinations import Destination
from airbyte_cdk.models import AirbyteConnectionStatus, AirbyteMessage, ConfiguredAirbyteCatalog, Status

import requests


class DestinationKeap(Destination):
    def write(
        self, config: Mapping[str, Any], configured_catalog: ConfiguredAirbyteCatalog, input_messages: Iterable[AirbyteMessage]
    ) -> Iterable[AirbyteMessage]:


        for message in input_messages:
            yield message


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
