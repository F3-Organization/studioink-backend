from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, status

from api.models import Studio
from api.models.invitation import Invitation
from api.services.registration_service import RegistrationService
from api.utils import get_current_user


class CustomRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )
    studio_name = serializers.CharField(required=True, allow_blank=True)
    terms_accepted = serializers.BooleanField(required=True)

    def create(self, validated_data):
        service = RegistrationService()
        return service.register_user_and_studio(validated_data, self.context["request"])

    def validate(self, attrs):
        attrs = super().validate(attrs)
        self.__verify_terms_accepted(attrs["terms_accepted"])
        validate_password(attrs["password"])
        return attrs

    def __verify_terms_accepted(self, value):
        if not value:
            raise serializers.ValidationError(
                "You must accept the terms of service to register.",
            )
        return value


class InvitationArtistSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        studio = self.get_studio()
        invitation = Invitation.objects.create(
            studio=studio,
            email=validated_data["email"],
            status=Invitation.Status.PENDING,
        )
        return invitation

    def validate(self, attrs):
        attrs = super().validate(attrs)
        self.__validate_email(attrs["email"])
        return attrs

    def __validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        if Invitation.objects.filter(
            studio=self.get_studio(), email=email, status=Invitation.Status.PENDING
        ).exists():
            raise serializers.ValidationError(
                "An invitation has already been sent to this email.",
                code=status.HTTP_409_CONFLICT,
            )
        return email

    def get_studio(self):
        current_user = get_current_user(self.context["request"])
        if not current_user:
            raise serializers.ValidationError("Authentication required.")
        try:
            return Studio.objects.get(owner=current_user)
        except Studio.DoesNotExist:
            raise serializers.ValidationError("Current user does not own a studio.")
