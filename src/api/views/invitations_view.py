from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.models.invitation import Invitation
from api.permissions.is_studio_owner import IsStudioOwnerOrReadOnly
from api.permissions.is_subscription_studio import IsStudioSubscription
from api.serializers import InvitationInputArtistSerializer, InvitationSerializer
from api.services.invitation_service import InvitationService
from api.tasks.send_email import send_invitation_email_task


class InvitationArtistViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = InvitationInputArtistSerializer
    permission_classes = [
        IsAuthenticated,
        IsStudioOwnerOrReadOnly,
        IsStudioSubscription,
    ]

    @extend_schema(
        request=None,
        responses=InvitationSerializer(many=True),
        tags=["Invitations"],
    )
    def list(self, request):
        queryset = Invitation.objects.filter(studio__owner=request.user)
        filtered_queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=InvitationInputArtistSerializer,
        responses=InvitationSerializer,
        tags=["Invitations"],
    )
    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        invitation = self.__perform_create(serializer)
        return Response(
            InvitationSerializer(invitation).data,
            status=status.HTTP_201_CREATED,
        )

    def __perform_create(self, serializer):
        invitation = InvitationService().create_invitation(
            serializer.validated_data["email"], self.context["request"]
        )
        send_invitation_email_task(invitation).delay()
        return invitation
