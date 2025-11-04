from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.filters import PortfolioImageFilter
from api.serializers import (
    PortfolioImageSerializer,
    PortfolioImageUpdateDescriptionSerializer,
    PortfolioImageUpdateTitleSerializer,
)
from api.services.portfolio_service import PortfolioService


class PortfolioViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = PortfolioImageSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = PortfolioImageFilter
    ordering_fields = ["title", "created_at"]
    search_fields = ["title", "description"]
    service = PortfolioService()

    @extend_schema(
        request=None,
        responses=PortfolioImageSerializer(many=True),
        tags=["Portfolio"],
    )
    def list(self, request, pk=None) -> Response:
        posts = PortfolioService().get_portfolio_from_artist(pk)
        filtered_posts = self.filter_queryset(posts)
        page = self.paginate_queryset(filtered_posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(filtered_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # TODO: Adicionar regra de validação onde só o dono do portfolio pode criar posts
    @extend_schema(
        request=PortfolioImageSerializer,
        responses=PortfolioImageSerializer,
        tags=["Portfolio"],
    )
    def create(self, request) -> Response:
        service = PortfolioService()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = service.create_portfolio_post(request.user, serializer.validated_data)
        return Response(data, status=status.HTTP_201_CREATED)

    @extend_schema(
        request=None,
        responses=PortfolioImageSerializer,
        tags=["Portfolio"],
    )
    def retrieve(self, request, pk=None) -> Response:
        data = self.service.get_portfolio_post_by_id(pk)
        serializer = self.get_serializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=PortfolioImageSerializer,
        responses=PortfolioImageSerializer,
        tags=["Portfolio"],
    )
    def update(self, request, pk=None) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = self.service.update_portfolio_post(pk, serializer.validated_data)
        return Response(post, status=status.HTTP_200_OK)

    @extend_schema(
        request=PortfolioImageUpdateTitleSerializer,
        responses=PortfolioImageSerializer,
        tags=["Portfolio"],
    )
    def update_title(self, request, pk=None) -> Response:
        pass

    @extend_schema(
        request=PortfolioImageUpdateDescriptionSerializer,
        responses=PortfolioImageSerializer,
        tags=["Portfolio"],
    )
    def update_description(self, request, pk=None) -> Response:
        pass

    @extend_schema(
        request=None,
        responses=None,
        tags=["Portfolio"],
    )
    def destroy(self, request, pk=None) -> Response:
        pass
