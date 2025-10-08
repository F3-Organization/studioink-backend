from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.exceptions import ValidationError

from api.models.artist import ArtistProfile
from api.models.studio import Studio
from api.models.terms_acceptance import TermsAcceptance
from api.utils import get_client_ip
from app import settings


class RegistrationService:
    @transaction.atomic
    def register_user_and_studio(self, validated_data, request):
        self.validate(validated_data)
        try:
            ip_address = get_client_ip(request)
            user = self.__create_user(validated_data)
            studio = self.__create_studio(validated_data, user)
            self.__create_artist_profile(user, studio)
            self.__record_terms_acceptance(user, ip_address)
            return user, studio
        except Exception as e:
            raise ValidationError(f"Registration failed: {e}")

    def validate(self, data):
        self.__validate_unique_email(data["email"])

    def __create_user(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user

    def __create_studio(self, validated_data, user):
        studio = Studio.create_studio_trial(
            name=validated_data["studio_name"], owner=user
        )
        return studio

    def __create_artist_profile(self, user, studio):
        ArtistProfile.objects.create(user=user, studio=studio)

    def __record_terms_acceptance(self, user, ip_address):
        TermsAcceptance.create_terms_acceptance(
            user=user,
            terms_version=settings.TERMS_OF_SERVICE_VERSION,
            ip_address=ip_address,
        )

    def __validate_unique_email(self, email):
        if User.objects.filter(email=email).exists():
            raise ValidationError("User with this email already exists.")
