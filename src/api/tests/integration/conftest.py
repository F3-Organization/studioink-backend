from types import SimpleNamespace as Simple

import pytest
from faker import Faker


@pytest.fixture
def register_user_validated_data():
    return {
        "username": Faker().user_name(),
        "email": Faker().email(),
        "password": Faker().password(),
        "studio_name": Faker().company(),
        "terms_accepted": True,
    }


@pytest.fixture
def fake_request():
    return Simple(META={"REMOTE_ADDR": "127.0.0.1"})
