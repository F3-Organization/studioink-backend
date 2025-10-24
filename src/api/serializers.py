from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers

from api.models.appointment import Appointment
from api.models.client import Client
from api.models.invitation import Invitation
from api.models.portfolio_image import PortfolioImage
from api.models.time_block import TimeBlock


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


class InvitationInputArtistSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = "__all__"


class AppointmentSerializer(serializers.ModelSerializer):
    client_id = serializers.IntegerField(write_only=True)
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
            "client",
        )

    def validate(self, attrs):
        if attrs["start_time"] < timezone.now():
            raise serializers.ValidationError("Start time must be in the future.")
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
        if attrs["start_time"] < timezone.now():
            raise serializers.ValidationError("Start time must be in the future.")
        start, end = attrs["start_time"], attrs["end_time"]
        if start >= end:
            raise serializers.ValidationError("End time must be after start time.")
        return attrs


class AppointmentUpdateStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=Appointment.AppointmentStatus.choices, required=True
    )


class TimeBlockSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(
        format="%d/%m/%Y %H:%M",
        input_formats=["%d/%m/%Y %H:%M", "%Y-%m-%dT%H:%M:%S%z"],
    )
    end_time = serializers.DateTimeField(
        format="%d/%m/%Y %H:%M",
        input_formats=["%d/%m/%Y %H:%M", "%Y-%m-%dT%H:%M:%S%z"],
    )

    class Meta:
        model = TimeBlock
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


class ClientModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"
        read_only_fields = (
            "id",
            "studio",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        if "date_of_birth" in attrs and attrs["date_of_birth"] > timezone.now().date():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return attrs


class PortfolioImageSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True, allow_empty_file=False, use_url=True)
    title = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)


class PortfolioImageUpdateTitleSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, allow_blank=False)


class PortfolioImageUpdateDescriptionSerializer(serializers.Serializer):
    description = serializers.CharField(required=True, allow_blank=False)
