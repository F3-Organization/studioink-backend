from django_filters import rest_framework as filters

from api.models.appointment import Appointment
from api.models.client import Client
from api.models.time_block import TimeBlock
from api.views.portfolio_view import PortfolioImage


class AppointmentFilter(filters.FilterSet):
    full_name = filters.CharFilter(
        field_name="client__full_name", lookup_expr="icontains"
    )
    description = filters.CharFilter(field_name="description", lookup_expr="icontains")
    status = filters.CharFilter(field_name="status", lookup_expr="icontains")
    start_time = filters.IsoDateTimeFilter(field_name="start_time", lookup_expr="gte")
    end_time = filters.IsoDateTimeFilter(field_name="end_time", lookup_expr="lte")

    class Meta:
        model = Appointment
        fields = [
            "full_name",
            "description",
            "status",
            "start_time",
            "end_time",
        ]


class TimeBlockFilter(filters.FilterSet):
    block_type = filters.CharFilter(field_name="block_type", lookup_expr="icontains")
    start_time = filters.IsoDateTimeFilter(field_name="start_time", lookup_expr="gte")
    end_time = filters.IsoDateTimeFilter(field_name="end_time", lookup_expr="lte")

    class Meta:
        model = TimeBlock
        fields = [
            "block_type",
            "start_time",
            "end_time",
        ]


class ClientFilter(filters.FilterSet):
    full_name = filters.CharFilter(field_name="full_name", lookup_expr="icontains")
    email = filters.CharFilter(field_name="email", lookup_expr="icontains")
    phone_number = filters.CharFilter(
        field_name="phone_number", lookup_expr="icontains"
    )

    class Meta:
        model = Client
        fields = [
            "full_name",
            "email",
            "phone_number",
        ]


class PortfolioImageFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    description = filters.CharFilter(field_name="description", lookup_expr="icontains")

    class Meta:
        model = PortfolioImage
        fields = [
            "title",
            "description",
        ]
