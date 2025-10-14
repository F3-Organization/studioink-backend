from datetime import timedelta
from decimal import ROUND_HALF_EVEN, Decimal
from types import SimpleNamespace as Simple

import pytest
from django.utils import timezone
from faker import Faker

from api.services.client_service import ClientService
from api.services.register_service import RegisterService


@pytest.fixture
def email():
    return Faker().email()


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
def register_client_validated_data():
    return {
        "full_name": Faker().name(),
        "email": Faker().email(),
        "phone_number": Faker().basic_phone_number(),
        "notes": Faker().sentence(),
    }


@pytest.fixture
def fake_request():
    return Simple(META={"REMOTE_ADDR": "127.0.0.1"})


@pytest.fixture
def registered_user(register_user_validated_data, fake_request):
    service = RegisterService()
    user, studio = service.register_user_and_studio(
        register_user_validated_data,
        fake_request,
    )
    return user


@pytest.fixture
def client(registered_user, register_client_validated_data):
    service = ClientService()
    return service.create_client(
        registered_user,
        register_client_validated_data,
    )


@pytest.fixture
def create_appointment_validated_data(client):
    start_time = timezone.now() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=1)
    price_quoted = Faker().pydecimal(left_digits=3, right_digits=2, positive=True)
    deposit_paid = (price_quoted / Decimal("2")).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_EVEN
    )
    return {
        "start_time": start_time,
        "end_time": end_time,
        "description": Faker().sentence(),
        "price_quoted": price_quoted,
        "deposit_paid": deposit_paid,
        "client_id": client.id,
    }


@pytest.fixture
def reschedule_appointment_validated_data(client):
    start_time = timezone.now() + timedelta(days=1, hours=1)
    end_time = start_time + timedelta(hours=1)
    return {
        "start_time": start_time,
        "end_time": end_time,
    }
