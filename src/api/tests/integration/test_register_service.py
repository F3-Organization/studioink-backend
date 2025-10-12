import pytest

from api.services.register_service import RegisterService


@pytest.mark.django_db
def test_register_user_and_studio(register_user_validated_data, fake_request):
    service = RegisterService()
    user, studio = service.register_user_and_studio(
        register_user_validated_data, fake_request
    )
    assert user.username == register_user_validated_data["username"]
    assert user.email == register_user_validated_data["email"]
    assert studio.name == register_user_validated_data["studio_name"]
    assert studio.owner == user
    assert user.check_password(register_user_validated_data["password"]) is True


@pytest.mark.django_db
def test_register_user_and_studio_existing_email(
    register_user_validated_data, fake_request
):
    service = RegisterService()
    user1, studio1 = service.register_user_and_studio(
        register_user_validated_data, fake_request
    )
    assert user1.email == register_user_validated_data["email"]
    with pytest.raises(Exception) as exc_info:
        service.register_user_and_studio(register_user_validated_data, fake_request)
    assert "A user with this email already exists." in str(exc_info.value)


@pytest.mark.django_db
def test_register_user_and_studio_internal_error(
    register_user_validated_data, fake_request, monkeypatch
):
    def mock_create_user(*args, **kwargs):
        raise Exception("Database error")

    monkeypatch.setattr(
        RegisterService, "_RegisterService__create_user", mock_create_user
    )
    service = RegisterService()
    with pytest.raises(Exception) as exc_info:
        service.register_user_and_studio(register_user_validated_data, fake_request)
    assert "Registration failed: Database error" in str(exc_info.value)
