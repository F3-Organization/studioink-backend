from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.filters import ClientFilter
from api.permissions.is_artist_of_studio import IsArtistOfStudio
from api.serializers import ClientModelSerializer
from api.services.client_service import ClientService


class ClientViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = ClientModelSerializer
    permission_classes = [IsAuthenticated, IsArtistOfStudio]
    filterset_class = ClientFilter
    ordering_fields = ["full_name", "email", "phone_number"]
    search_fields = ["full_name", "email", "phone_number"]
    service = ClientService()

    @extend_schema(
        request=None,
        responses=ClientModelSerializer(many=True),
        tags=["Clients"],
    )
    def list(self, request) -> Response:
        clients = ClientService().get_clients_for_studio(request)
        filtered_clients = self.filter_queryset(clients)
        page = self.paginate_queryset(filtered_clients)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=ClientModelSerializer,
        responses=ClientModelSerializer,
        tags=["Clients"],
    )
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client = ClientService().create_client(
            request.user,
            serializer.validated_data,
        )
        return Response(
            self.get_serializer(client).data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        request=None,
        responses=ClientModelSerializer,
        tags=["Clients"],
    )
    def retrieve(self, request, pk=None):
        client = self.service.get_client_details(request.user, pk)
        return Response(
            self.get_serializer(client).data,
            status=status.HTTP_200_OK,
        )
