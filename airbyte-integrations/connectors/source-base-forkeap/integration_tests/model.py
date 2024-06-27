from test_utils import fake_data_generator as gen
from source_base_forkeap.model.contact import *
import requests
import os

'''
Intensive test to check if the model classes are compatible with the Keap API

It is fine if our model is more strict than the Keap API
'''

KEAP_ACCESS_TOKEN = os.environ["KEAP_ACCESS_TOKEN"]

def test_contact_intensive():

    for _ in range(1):
        _test_contact()

def _test_contact():

    # Generate a fake contact
    contact = gen.fake_contact()
    
    # Try to create it against the Keap API
    _create_contact(contact)


def _create_contact(contact: Contact):

    payload = contact.to_dict()
    url = "https://api.infusionsoft.com/crm/rest/v2/contacts"
    head = {"Authorization": "Bearer " + KEAP_ACCESS_TOKEN}

    response = requests.post(url, headers = head, json = payload)

    if not response.ok:
        print(response.text)
        raise  Exception()
