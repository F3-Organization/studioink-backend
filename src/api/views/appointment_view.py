from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import AppointmentFilter
from api.models.appointment import Appointment
from api.permissions.is_artist_of_studio import IsArtistOfStudio
from api.serializers import (
    AppointmentRescheduleSerializer,
    AppointmentSerializer,
    AppointmentUpdateStatusSerializer,
)
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
        appointments = AppointmentService().get_appointments_for_artist(request)
        filtered_appointments = self.filter_queryset(appointments)
        page = self.paginate_queryset(filtered_appointments)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(
                serializer.data, status=status.HTTP_200_OK
            )

        serializer = self.get_serializer(filtered_appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        service = AppointmentService()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = service.create_appointment(
            request.user, serializer.validated_data
        )
        output_serializer = self.get_serializer(appointment)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["patch"], url_path="reschedule")
    def reschedule_appointment(self, request, pk=None):
        service = AppointmentService()
        serializer = AppointmentRescheduleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = service.reschedule_appointment(pk, serializer.validated_data)
        output_serializer = self.get_serializer(appointment)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"], url_path="update-status")
    def update_appointment_status(self, request, pk=None):
        serializer = AppointmentUpdateStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = AppointmentService().update_appointment_status(
            pk, serializer.validated_data["status"]
        )
        output_serializer = self.get_serializer(appointment)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path=r"studio/(?P<studio_id>[^/.]+)")
    def get_appointments_for_studio(self, request, studio_id):
        service = AppointmentService()
        appointments = service.get_appointments_for_studio(studio_id)
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path=r"client/(?P<client_id>[^/.]+)")
    def get_appointments_for_client(self, request, client_id):
        service = AppointmentService()
        appointments = service.get_appointments_for_client(client_id)
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="details")
    def get_appointment_details(self, request, pk=None):
        service = AppointmentService()
        appointment = service.get_appointment_details(pk)
        serializer = self.get_serializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)
