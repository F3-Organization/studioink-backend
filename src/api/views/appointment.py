from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import AppointmentFilter
from api.models.appointment import Appointment
from api.permissions.is_artist_of_studio import IsArtistOfStudio
from api.serializers import AppointmentSerializer
from api.services.appointment import AppointmentService


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
        return Response(
            self.serializer_class(filtered_appointments, many=True).data,
            status=status.HTTP_200_OK,
        )

    def create(self, request):
        service = AppointmentService()
        appointment = service.create_appointment(request)
        return Response(
            self.serializer_class(appointment).data,
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk=None):
        pass
