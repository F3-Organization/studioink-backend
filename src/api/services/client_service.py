import logging

from rest_framework import status
from rest_framework.exceptions import APIException

from api.models.artist import ArtistProfile
from api.models.client import Client

logger = logging.getLogger(__name__)


class ClientService:
    def __init__(self):
        self.model = Client

    def create_client(self, user, validate_data):
        studio = self.__get_studio_from_user(user)
        self.__verify_unique_constraints(
            studio,
            validate_data["email"],
            validate_data["phone_number"],
        )
        return self.__create(validate_data)

    def get_clients_for_studio(self, request):
        studio = self.__get_studio_from_user(request.user)
        return self.model.objects.filter(studio=studio)

    def get_client_details(self, user, client_id):
        studio = self.__get_studio_from_user(user)
        try:
            return self.model.objects.get(id=client_id, studio=studio)
        except self.model.DoesNotExist:
            return APIException("Client not found.", code=status.HTTP_404_NOT_FOUND)

    def __verify_unique_constraints(self, studio, email, phone_number):
        client = self.model.objects.filter(
            studio=studio, email=email, phone_number=phone_number
        ).exists()
        if client:
            logger.error(
                "Client with email %s and phone number %s already exists in studio %s",
                email,
                phone_number,
                studio.id,
            )
            raise APIException(
                "Client with this email and phone number already exists.",
                code=status.HTTP_400_BAD_REQUEST,
            )

    def __get_studio_from_user(self, user):
        try:
            artist_profile = ArtistProfile.objects.get(user=user)
            return artist_profile.studio
        except ArtistProfile.DoesNotExist:
            logger.error("ArtistProfile for user %s does not exist", user.id)
            raise APIException(
                "ArtistProfile not found.",
                code=status.HTTP_404_NOT_FOUND,
            )

    def __create(self, validated_data):
        return self.model.objects.create(
            studio_id=validated_data["studio_id"],
            full_name=validated_data["full_name"],
            email=validated_data["email"],
            phone_number=validated_data["phone_number"],
            date_of_birth=validated_data.get("date_of_birth"),
            notes=validated_data.get("notes"),
        )
