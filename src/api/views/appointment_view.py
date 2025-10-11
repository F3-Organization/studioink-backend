from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import AppointmentFilter
from api.models.appointment import Appointment
from api.permissions.is_artist_of_studio import IsArtistOfStudio
from api.serializers import AppointmentSerializer
from api.services.appointment_service import AppointmentService


class AppointmentByArtistViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsArtistOfStudio]
    filterset_class = AppointmentFilter
    ordering_fields = ["start_time", "end_time", "status"]
    search_fields = [
        "client__full_name",
        "description",
        "status",
        "start_time",
        "end_time",
    ]

    def list(self, request) -> Response:
        service = AppointmentService()
        appointments = service.get_appointments_for_artist(request)
        filtered_appointments = self.filter_queryset(appointments)
        paginated_appointments = self.paginate_queryset(filtered_appointments)
        return Response(
            self.serializer_class(paginated_appointments, many=True).data,
            status=status.HTTP_200_OK,
        )

    def create(self, request):
        service = AppointmentService()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = service.create_appointment(
            request.user, serializer.validated_data
        )
        return Response(
            self.serializer_class(appointment).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["patch"], url_path="reschedule")
    def reschedule_appointment(self, request, pk=None):
        service = AppointmentService()
        service.reschedule_appointment(pk, request)
        return Response(
            {"detail": "Appointment rescheduled successfully."},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["patch"], url_path="update-status")
    def update_appointment_status(self, request, pk=None):
        appointment = AppointmentService().update_appointment_status(
            pk, request.data.get("status")
        )
        return Response(
            self.serializer_class(appointment).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"], url_path="studio/(studio_id)")
    def get_appointments_for_studio(self, request, studio_id):
        appointment = AppointmentService().get_appointments_for_studio(studio_id)
        return Response(
            self.serializer_class(appointment, many=True).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"], url_path="client/(client_id)")
    def get_appointments_for_client(self, request, client_id):
        appointment = AppointmentService().get_appointments_for_client(client_id)
        return Response(
            self.serializer_class(appointment, many=True).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["get"], url_path="details")
    def get_appointment_details(self, request, pk=None):
        service = AppointmentService()
        appointment = service.__get_appointment_by_id(pk)
        return Response(
            self.serializer_class(appointment).data,
            status=status.HTTP_200_OK,
        )
