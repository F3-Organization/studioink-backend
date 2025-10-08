from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers, status

from api.models import Studio
from api.models.artist import ArtistProfile
from api.models.invitation import Invitation
from api.models.termsAcceptance import TermsAcceptance
from api.utils import get_client_ip, get_current_user
from app import settings


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

    def save(self):
        user, studio = self.create(self.validated_data)
        return user, studio

    @transaction.atomic
    def create(self, validated_data):
        ip = get_client_ip(self.context["request"])
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        studio = Studio.objects.create(
            name=validated_data["studio_name"],
            owner=user,
            subscription_plan=Studio.SubscriptionPlan.SOLO,
            subscription_status=Studio.SubscriptionStatus.TRIALING,
        )
        ArtistProfile.objects.create(user=user, studio=studio)
        TermsAcceptance.objects.create(
            user=user,
            terms_version=settings.TERMS_OF_SERVICE_VERSION,
            ip_address=ip,
        )
        return user, studio

    def validate(self, attrs):
        attrs = super().validate(attrs)
        self.verify_unique_email(attrs["email"])
        self.verify_terms_accepted(attrs["terms_accepted"])
        validate_password(attrs["password"])
        return attrs

    def verify_unique_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return email

    def verify_terms_accepted(self, value):
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
            raise serializers.ValidationError("Current user does not own a studio.")
