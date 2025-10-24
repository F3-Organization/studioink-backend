from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.exceptions import APIException

from api.models.artist import ArtistProfile
from api.models.portfolio_image import PortfolioImage


class PortfolioService:
    model = PortfolioImage

    def create_portfolio_post(
        self, user: User, validated_data: dict
    ) -> PortfolioImage | None:
        artist_profile = self.__get_artist_profile(user)
        return self.__create_portfolio_post(artist_profile, validated_data)

    def update_portfolio_post(
        self, portfolio_id: int, validated_data: dict
    ) -> PortfolioImage | None:
        post = self.__get_portfolio_post_by_id(portfolio_id)
        return self.__update_portfolio_post(post, validated_data)

    def get_portfolio_from_artist(self, artist_id: int) -> PortfolioImage | None:
        try:
            portfolio = self.model.objects.get_by_artist_id(artist_id)
            return portfolio
        except PortfolioImage.DoesNotExist:
            return APIException(
                "Artist portfolio not found.", code=status.HTTP_404_NOT_FOUND
            )

    def get_portfolio_post_by_id(self, post_id: int) -> PortfolioImage | None:
        try:
            return self.model.objects.get(id=post_id)
        except PortfolioImage.DoesNotExist:
            return APIException(
                "Portfolio post not found.", code=status.HTTP_404_NOT_FOUND
            )

    def __get_artist_profile(self, user):
        try:
            return ArtistProfile.objects.get(user=user)
        except ArtistProfile.DoesNotExist:
            raise APIException(
                "Artist profile not found.", code=status.HTTP_404_NOT_FOUND
            )

    def __create_portfolio_post(
        self, artist_profile: ArtistProfile, validated_data: dict
    ):
        try:
            return self.model.objects.create(
                artist_profile=artist_profile,
                image=validated_data["image"],
                title=validated_data.get("title", ""),
                description=validated_data.get("description", ""),
            )
        except Exception as e:
            raise APIException(
                f"Error creating portfolio post: {str(e)}",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def __get_portfolio_post_by_id(self, post_id: int) -> PortfolioImage:
        try:
            return self.model.objects.get(id=post_id)
        except PortfolioImage.DoesNotExist:
            raise APIException(
                "Portfolio post not found.", code=status.HTTP_404_NOT_FOUND
            )

    def __update_portfolio_post(self, post: PortfolioImage, validated_data: dict):
        try:
            post.title = validated_data.get("title", post.title)
            post.description = validated_data.get("description", post.description)
            post.image = validated_data.get("image", post.image)
            post.save()
            return post
        except Exception as e:
            raise APIException(
                f"Error updating portfolio post: {str(e)}",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
