from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import TimeBlockFilter
from api.permissions.is_artist_of_studio import IsArtistOfStudio
from api.serializers import TimeBlockSerializer
from api.services.time_block_service import TimeBlockService


class TimeBlockViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = TimeBlockSerializer
    permission_classes = [IsAuthenticated, IsArtistOfStudio]
    filterset_class = TimeBlockFilter
    ordering_fields = ["start_time", "end_time", "block_type"]
    search_fields = ["reason", "block_type"]

    @extend_schema(
        request=None,
        responses=TimeBlockSerializer(many=True),
        tags=["Time Blocks"],
    )
    def list(self, request, *args, **kwargs):
        service = TimeBlockService()
        queryset = service.list_time_blocks_for_artist(request.user)
        filtered_queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=TimeBlockSerializer,
        responses=TimeBlockSerializer,
        tags=["Time Blocks"],
    )
    def create(self, request, *args, **kwargs):
        service = TimeBlockService()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        time_block = service.create_time_block(request.user, serializer.validated_data)
        output_serializer = self.get_serializer(time_block)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        request=None,
        responses=TimeBlockSerializer(many=True),
        tags=["Time Blocks"],
    )
    @action(detail=False, methods=["get"], url_path=r"studio/(?P<studio_id>[^/.]+)")
    def list_for_studio(self, request, studio_id=None):
        service = TimeBlockService()
        queryset = service.list_time_blocks_for_studio(studio_id)
        filtered_queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=None,
        responses=None,
        tags=["Time Blocks"],
    )
    def destroy(self, request, *args, **kwargs):
        service = TimeBlockService()
        service.delete_time_block(request.user, kwargs.get("pk"))
        return Response(status=status.HTTP_204_NO_CONTENT)
