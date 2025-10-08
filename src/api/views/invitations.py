from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api.models.invitation import Invitation
from api.permissions.isStudioOwner import IsStudioOwnerOrReadOnly
from api.permissions.isSubscriptionStudio import IsStudioSubscription
from api.serializers import InvitationArtistSerializer
from api.tasks.sendEmail import send_invitation_email_task


class InvitationArtistViewSet(ViewSet):
    serializer_class = InvitationArtistSerializer
    permission_classes = [
        IsAuthenticated,
        IsStudioOwnerOrReadOnly,
        IsStudioSubscription,
    ]

    def list(self, request, *args, **kwargs):
        queryset = Invitation.objects.filter(studio__owner=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invitation = self.perform_create(serializer)
        return Response(
            InvitationArtistSerializer(invitation).data,
            status=status.HTTP_201_CREATED,
        )

    def perform_create(self, serializer):
        invitation = serializer.save()
        send_invitation_email_task(invitation).delay()
        return invitation
