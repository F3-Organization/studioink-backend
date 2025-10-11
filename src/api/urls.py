from django.urls import path
from rest_framework import routers

from api.views.appointment_view import AppointmentByArtistViewSet
from api.views.invitations_view import InvitationArtistViewSet
from api.views.time_block_view import TimeBlockViewSet

router = routers.DefaultRouter()

router.register(
    r"invitations",
    InvitationArtistViewSet,
    basename="invitation",
)
router.register(
    r"appointments",
    AppointmentByArtistViewSet,
    basename="appointment",
)
router.register(
    r"time-blocks",
    TimeBlockViewSet,
    basename="time-block",
)
urlpatterns: list[path] = []
urlpatterns += router.urls
