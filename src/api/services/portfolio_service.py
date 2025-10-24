from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.exceptions import APIException

from api.models.portfolio_image import PortfolioImage


class PortfolioService:
    model = PortfolioImage

    def create_portfolio_post(
        self, user: User, validated_data: dict
    ) -> PortfolioImage | None:
        pass

    def get_portfolio_from_artist(self, artist_id: int) -> PortfolioImage | None:
        pass

    def get_portfolio_post_by_id(self, post_id: int) -> PortfolioImage | None:
        try:
            return self.model.objects.get(id=post_id)
        except PortfolioImage.DoesNotExist:
            return APIException(
                "Portfolio post not found.", code=status.HTTP_404_NOT_FOUND
            )
