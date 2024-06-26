from source_base_forkeap.model import contact
from test_utils.fake_data_generator import(
        fake_address
)

def test_fake_contact():
    f_address = fake_address()
    assert isinstance(f_address, contact.Address)
