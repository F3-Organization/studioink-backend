import pytest
from rest_framework.exceptions import APIException

from api.services.invitation_service import InvitationService


@pytest.mark.django_db
def test_create_invitation_successfully(email, registered_user):
    service = InvitationService()
    invitation = service.create_invitation(email, registered_user)
    assert invitation.email == email


@pytest.mark.django_db
def test_create_invitation_with_an_error(email, fake_user):
    service = InvitationService()
    with pytest.raises(APIException) as excinfo:
        service.create_invitation(email, fake_user)
    assert str(excinfo.value) == "Studio not found for the current user."
