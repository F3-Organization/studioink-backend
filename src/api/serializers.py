from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from api.models.appointment import Appointment
from api.services.invitation_service import InvitationService
from api.services.registration_service import RegistrationService


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
        service = InvitationService()
        return service.create_invitation(
            validated_data["email"], self.context["request"]
        )


class AppointmentSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(
        format="%d/%m/%Y %H:%M", input_formats=["%d/%m/%Y %H:%M", "%Y-%m-%dT%H:%M:%S%z"]
    )
    end_time = serializers.DateTimeField(
        format="%d/%m/%Y %H:%M", input_formats=["%d/%m/%Y %H:%M", "%Y-%m-%dT%H:%M:%S%z"]
    )

    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = (
            "id",
            "studio",
            "artist",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        if attrs["end_time"] <= attrs["start_time"]:
            raise serializers.ValidationError("End time must be after start time.")
        return attrs


class AppointmentRescheduleSerializer(serializers.Serializer):
    start_time = serializers.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M", "%Y-%m-%dT%H:%M:%S%z"],
        format="%d/%m/%Y %H:%M",
    )
    end_time = serializers.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M", "%Y-%m-%dT%H:%M:%S%z"],
        format="%d/%m/%Y %H:%M",
    )

    def validate(self, attrs):
        start, end = attrs["start_time"], attrs["end_time"]
        if start >= end:
            raise serializers.ValidationError("End time must be after start time.")
        return attrs


class AppointmentUpdateStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Appointment.Status.choices, required=True)
