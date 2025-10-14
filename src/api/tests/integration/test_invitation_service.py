import pytest

from api.services.invitation_service import InvitationService


@pytest.mark.django_db
def test_create_invitation_successfully(email, registered_user):
    service = InvitationService()
    invitation = service.create_invitation(email, registered_user)
    assert invitation.email == email
