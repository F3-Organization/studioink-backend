from django.urls import path
from rest_framework import routers

from api.views.appointment_view import AppointmentByArtistViewSet
from api.views.client_view import ClientViewSet
from api.views.invitations_view import InvitationArtistViewSet
from api.views.portfolio_view import PortfolioViewSet
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
router.register(
    r"clients",
    ClientViewSet,
    basename="client",
)
router.register(
    r"portfolio",
    PortfolioViewSet,
    basename="portfolio",
)
urlpatterns: list[path] = []
urlpatterns += router.urls
