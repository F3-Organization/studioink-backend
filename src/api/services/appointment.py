import logging

from rest_framework import status
from rest_framework.exceptions import APIException

from api.models.appointment import Appointment
from api.models.artist import ArtistProfile

logger = logging.getLogger(__name__)


class AppointmentService:

    def create_appointment(self, request):
        artist_profile = self.__get_artist_profile(request)
        self.__validate_appointment_availability(
            artist_profile,
            request.data.get("start_time"),
            request.data.get("end_time"),
        )
        return self.__create_appointment(request, artist_profile)

    def reschedule_appointment(self, appointment_id, new_start_time, new_end_time):
        pass

    def update_appointment_status(self, appointment_id, new_status):
        pass

    def get_appointments_for_studio(self, studio_id):
        pass

    def get_appointments_for_artist(self, request):
        artist_profile = self.__get_artist_profile(request)
        return Appointment.objects.filter(artist=artist_profile)

    def get_appointments_for_client(self, client_id):
        pass

    def __validate_appointment_availability(self, artist, start_time, end_time):
        overlap = Appointment.objects.is_artist_available(artist, start_time, end_time)
        if overlap:
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
