import pytest
from rest_framework.exceptions import APIException

from api.models.appointment import Appointment
from api.services.appointment_service import AppointmentService


@pytest.mark.django_db
class TestAppointmentService:

    def test_create_appointment_sucessfuly(
        self, user, create_appointment_validated_data
    ):
        service = AppointmentService()
        appointment = service.create_appointment(
            user, create_appointment_validated_data
        )
        assert appointment.id is not None
        assert appointment.client_id == create_appointment_validated_data["client_id"]
        assert appointment.start_time == create_appointment_validated_data["start_time"]
        assert appointment.end_time == create_appointment_validated_data["end_time"]
        assert (
            appointment.description == create_appointment_validated_data["description"]
        )
        assert appointment.status == Appointment.AppointmentStatus.PENDING
        assert (
            appointment.price_quoted
            == create_appointment_validated_data["price_quoted"]
        )
        assert (
            appointment.deposit_paid
            == create_appointment_validated_data["deposit_paid"]
        )

    def test_create_appointment_with_artist_unavailable(
        self, user, create_appointment_validated_data
    ):
        service = AppointmentService()
        service.create_appointment(user, create_appointment_validated_data)
        overlapping_data = create_appointment_validated_data.copy()
        with pytest.raises(APIException) as exc_info:
            service.create_appointment(user, overlapping_data)

        assert (
            str(exc_info.value) == "The artist is not available at the requested time."
        )

    def test_create_appointment_with_nonexistent_artist(
        self, user, create_appointment_validated_data, monkeypatch
    ):
        def mock_get_artist_profile(*args, **kwargs):
            raise APIException("Artist profile not found for the current user.")

        monkeypatch.setattr(
            AppointmentService,
            "_AppointmentService__get_artist_profile",
            mock_get_artist_profile,
        )
        service = AppointmentService()
        with pytest.raises(APIException) as exc_info:
            service.create_appointment(user, create_appointment_validated_data)
        assert str(exc_info.value) == "Artist profile not found for the current user."

    def test_reschedule_appointment_successfully(
        self,
        user,
        create_appointment_validated_data,
        reschedule_appointment_validated_data,
    ):
        service = AppointmentService()
        appointment = service.create_appointment(
            user, create_appointment_validated_data
        )
        updated_appointment = service.reschedule_appointment(
            appointment.id, reschedule_appointment_validated_data
        )
        assert (
            updated_appointment.start_time
            == reschedule_appointment_validated_data["start_time"]
        )
        assert (
            updated_appointment.end_time
            == reschedule_appointment_validated_data["end_time"]
        )

    def test_update_status_successfully(self, user, create_appointment_validated_data):
        service = AppointmentService()
        appointment = service.create_appointment(
            user, create_appointment_validated_data
        )
        updated_appointment = service.update_appointment_status(
            appointment.id, Appointment.AppointmentStatus.CONFIRMED
        )
        assert updated_appointment.status == Appointment.AppointmentStatus.CONFIRMED

    def test_delete_appointment_successfully(
        self, user, create_appointment_validated_data
    ):
        service = AppointmentService()
        appointment = service.create_appointment(
            user, create_appointment_validated_data
        )
        service.delete_appointment(user, appointment.id)
        with pytest.raises(APIException) as exc_info:
            service.get_appointment_details(appointment.id)
        assert str(exc_info.value) == "Appointment not found."

    def test_get_appointment_for_studio(self, user, create_appointment_validated_data):
        service = AppointmentService()
        appointment = service.create_appointment(
            user, create_appointment_validated_data
        )
        appointments = service.get_appointments_for_studio(appointment.studio_id)
        assert len(appointments) == 1
        assert appointments[0].id == appointment.id

    def test_get_appointment_for_artist(self, user, create_appointment_validated_data):
        service = AppointmentService()
        appointment = service.create_appointment(
            user, create_appointment_validated_data
        )
        request = type("Request", (object,), {"user": user})()
        appointments = service.get_appointments_for_artist(request)
        assert len(appointments) == 1
        assert appointments[0].id == appointment.id

    def test_get_appointment_for_client(
        self, user, client, create_appointment_validated_data
    ):
        service = AppointmentService()
        appointment = service.create_appointment(
            user, create_appointment_validated_data
        )
        appointments = service.get_appointments_for_client(client.id)
        assert len(appointments) == 1
        assert appointments[0].id == appointment.id

    def test_get_appointment_details(self, user, create_appointment_validated_data):
        service = AppointmentService()
        appointment = service.create_appointment(
            user, create_appointment_validated_data
        )
        fetched_appointment = service.get_appointment_details(appointment.id)
        assert fetched_appointment.id == appointment.id
        assert (
            fetched_appointment.client_id
            == create_appointment_validated_data["client_id"]
        )
        assert (
            fetched_appointment.start_time
            == create_appointment_validated_data["start_time"]
        )
        assert (
            fetched_appointment.end_time
            == create_appointment_validated_data["end_time"]
        )
        assert (
            fetched_appointment.description
            == create_appointment_validated_data["description"]
        )
        assert fetched_appointment.status == Appointment.AppointmentStatus.PENDING
        assert (
            fetched_appointment.price_quoted
            == create_appointment_validated_data["price_quoted"]
        )
        assert (
            fetched_appointment.deposit_paid
            == create_appointment_validated_data["deposit_paid"]
        )
