from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.utils import jwt_encode
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.serializers import CustomRegisterSerializer


class CustomRegisterView(RegisterView):
    """
    Custom user registration view.
    """

    serializer_class = CustomRegisterSerializer
    permission_classes = [AllowAny]
    queryset = get_user_model().objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        data = self.get_response_data(user)

        if data:
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer: CustomRegisterSerializer):
        user, studio = serializer.save()
        if api_settings.USE_JWT:
            self.access_token, self.refresh_token = jwt_encode(user)
        elif api_settings.TOKEN_MODEL:
            api_settings.TOKEN_CREATOR(api_settings.TOKEN_MODEL, user, serializer)
        return user
