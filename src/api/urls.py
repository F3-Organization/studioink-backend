from django.urls import path
from rest_framework import routers

from api.views.invitations import InvitationArtistViewSet

router = routers.DefaultRouter()

router.register(
    r"invitations",
    InvitationArtistViewSet,
    basename="invitation",
)
urlpatterns: list[path] = []
urlpatterns += router.urls
