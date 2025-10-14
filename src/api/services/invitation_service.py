from django.forms import ValidationError
from rest_framework import status
from rest_framework.exceptions import APIException

from api.models.artist import ArtistProfile
from api.models.invitation import Invitation
from api.models.studio import Studio
from api.tasks.send_email import send_invitation_email_task


class InvitationService:
    def create_invitation(self, email, user):
        try:
            studio = self.__get_studio(user)
            self.__verify_invitation_exists(studio, email)
            self.__verify_not_owner_other_studio(studio, email)
            self.__verify_if_available_to_invite(studio, email)
            invitation = Invitation.create_invitation(studio, email)
            send_invitation_email_task.delay(invitation.id)
            return invitation

        except APIException as e:
            raise APIException(
                f"Failed to create invitation: {e}",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    def __get_studio(self, user):
        try:
            studio = Studio.objects.get(owner=user)
            return studio
        except Studio.DoesNotExist:
            raise APIException(
                "Studio not found for the current user.",
                code=status.HTTP_404_NOT_FOUND,
            )

    def __verify_invitation_exists(self, studio, email):
        if Invitation.objects.filter(
            studio=studio, email=email, status=Invitation.Status.PENDING
        ).exists():
            raise ValidationError("An active invitation for this email already exists.")

    def __verify_if_available_to_invite(self, studio, email):
        if not ArtistProfile.objects.is_available_to_invite(studio, email):
            raise ValidationError("This user is already an artist in the studio.")

    def __verify_not_owner_other_studio(self, current_studio, email):
        if ArtistProfile.objects.is_owner_other_studio(email, current_studio):
            raise ValidationError("The user is already an owner of another studio.")
