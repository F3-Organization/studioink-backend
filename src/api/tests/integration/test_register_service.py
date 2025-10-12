from types import SimpleNamespace as Simple

import pytest
from faker import Faker

from api.services.register_service import RegisterService


@pytest.fixture
def validated_data():
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


@pytest.mark.django_db
def test_register_user_and_studio(validated_data, fake_request):
    service = RegisterService()
    user, studio = service.register_user_and_studio(validated_data, fake_request)
    assert user.username == validated_data["username"]
    assert user.email == validated_data["email"]
    assert studio.name == validated_data["studio_name"]
    assert studio.owner == user
    assert user.check_password(validated_data["password"]) is True


@pytest.mark.django_db
def test_register_user_and_studio_existing_email(validated_data, fake_request):
    service = RegisterService()
    user1, studio1 = service.register_user_and_studio(validated_data, fake_request)
    assert user1.email == validated_data["email"]
    with pytest.raises(Exception) as exc_info:
        service.register_user_and_studio(validated_data, fake_request)
    assert "A user with this email already exists." in str(exc_info.value)


@pytest.mark.django_db
def test_register_user_and_studio_internal_error(
    validated_data, fake_request, monkeypatch
):
    def mock_create_user(*args, **kwargs):
        raise Exception("Database error")

    monkeypatch.setattr(
        RegisterService, "_RegisterService__create_user", mock_create_user
    )
    service = RegisterService()
    with pytest.raises(Exception) as exc_info:
        service.register_user_and_studio(validated_data, fake_request)
    assert "Registration failed: Database error" in str(exc_info.value)
