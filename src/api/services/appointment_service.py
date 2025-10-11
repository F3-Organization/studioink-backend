import logging

from rest_framework import status
from rest_framework.exceptions import APIException

from api.models.appointment import Appointment
from api.models.artist import ArtistProfile

logger = logging.getLogger(__name__)


class AppointmentService:

    def create_appointment(self, user, validated_data):
        artist_profile = self.__get_artist_profile()
        self.__validate_appointment_availability(
            artist_profile,
            validated_data.get("start_time"),
            validated_data.get("end_time"),
        )
        return self.__create_appointment(validated_data, artist_profile)

    def reschedule_appointment(self, appointment_id, request):
        appointment = self.__get_appointment_by_id(appointment_id)
        self.__validate_appointment_availability(
            appointment.artist,
            request.data.get("start_time"),
            request.data.get("end_time"),
        )
        return Appointment.reschedule_appointment(
            appointment,
            request.data.get("start_time"),
            request.data.get("end_time"),
        )

    def update_appointment_status(self, appointment_id, new_status):
        appointment = self.__get_appointment_by_id(appointment_id)
        self.__validate_new_status(appointment, new_status)
        appointment.status = new_status
        appointment.save()
        return appointment

    def get_appointments_for_studio(self, studio_id):
        return Appointment.objects.filter(studio_id=studio_id)

    def get_appointments_for_artist(self, request):
        artist_profile = self.__get_artist_profile(request)
        return Appointment.objects.filter(artist=artist_profile)

    def get_appointments_for_client(self, client_id):
        pass

    def __validate_appointment_availability(self, artist, start_time, end_time):
        is_available = Appointment.objects.is_artist_available(
            artist, start_time, end_time
        )
        if not is_available:
            raise APIException(
                "The artist is not available at the requested time.",
                code=status.HTTP_400_BAD_REQUEST,
            )

    def __get_artist_profile(self, request):
        try:
            return ArtistProfile.objects.get(user=request.user)
        except ArtistProfile.DoesNotExist:
            logger.error("Artist profile not found for user: %s", request.user)
            raise APIException(
                "Artist profile not found for the current user.",
                code=status.HTTP_404_NOT_FOUND,
            )

    def __create_appointment(self, request, artist_profile):
        return Appointment.objects.create(
            studio_id=artist_profile.studio_id,
            artist=artist_profile,
            client_id=request.data.get("client"),
            start_time=request.data.get("start_time"),
            end_time=request.data.get("end_time"),
            description=request.data.get("description", ""),
            status=request.data.get("status", Appointment.AppointmentStatus.PENDING),
        )

    def __get_appointment_by_id(self, appointment_id):
        try:
            return Appointment.objects.get_appointment_by_id(appointment_id)
        except Appointment.DoesNotExist:
            logger.error("Appointment not found with ID: %s", appointment_id)
            raise APIException(
                "Appointment not found.",
                code=status.HTTP_404_NOT_FOUND,
            )

    def __validate_new_status(self, appointment, new_status):
        valid_transitions = {
            Appointment.AppointmentStatus.PENDING: [
                Appointment.AppointmentStatus.CONFIRMED,
                Appointment.AppointmentStatus.CANCELED,
            ],
            Appointment.AppointmentStatus.CONFIRMED: [
                Appointment.AppointmentStatus.COMPLETED,
                Appointment.AppointmentStatus.CANCELED,
            ],
            Appointment.AppointmentStatus.COMPLETED: [],
            Appointment.AppointmentStatus.CANCELED: [],
        }

        if new_status not in valid_transitions.get(appointment.status, []):
            raise APIException(
                f"Invalid status transition from {appointment.status} to {new_status}.",
                code=status.HTTP_400_BAD_REQUEST,
            )
        appointment.status = new_status
        appointment.save()
