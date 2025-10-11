from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api.models.invitation import Invitation
from api.permissions.is_studio_owner import IsStudioOwnerOrReadOnly
from api.permissions.is_subscription_studio import IsStudioSubscription
from api.serializers import InvitationInputArtistSerializer, InvitationSerializer
from api.services.invitation_service import InvitationService
from api.tasks.send_email import send_invitation_email_task


class InvitationArtistViewSet(ViewSet):
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
    def list(self, request, *args, **kwargs):
        queryset = Invitation.objects.filter(studio__owner=request.user)
        serializer = InvitationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=InvitationInputArtistSerializer,
        responses=InvitationSerializer,
        tags=["Invitations"],
    )
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        invitation = self.perform_create(serializer)
        return Response(
            InvitationSerializer(invitation).data,
            status=status.HTTP_201_CREATED,
        )

    def perform_create(self, serializer):
        invitation = InvitationService().create_invitation(
            serializer.validated_data["email"], self.context["request"]
        )
        send_invitation_email_task(invitation).delay()
        return invitation
