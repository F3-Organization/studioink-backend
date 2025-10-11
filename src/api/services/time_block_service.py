import logging

from rest_framework import status
from rest_framework.exceptions import APIException

from api.models.appointment import Appointment
from api.models.artist import ArtistProfile
from api.models.time_block import TimeBlock

logger = logging.getLogger(__name__)


class TimeBlockService:

    def create_time_block(self, user, validated_data):
        artist_profile = self.__get_artist_profile(user)
        self.__ensure_no_conflicts(
            artist_profile,
            validated_data["start_time"],
            validated_data["end_time"],
        )
        return self.__create_time_block(validated_data, artist_profile)

    def list_time_blocks_for_artist(self, user):
        artist_profile = self.__get_artist_profile(user)
        return TimeBlock.objects.filter(artist=artist_profile)

    def list_time_blocks_for_studio(self, studio_id):
        return TimeBlock.objects.filter(studio_id=studio_id)

    def delete_time_block(self, user, time_block_id):
        time_block = self.__get_time_block_by_id(time_block_id)
        if time_block.artist.user != user and not user.is_staff:
            logger.warning(
                "User %s attempted to delete time block %s without permission",
                user,
                time_block_id,
            )
            raise APIException(
                "You do not have permission to delete this time block.",
                code=status.HTTP_403_FORBIDDEN,
            )
        time_block.delete()

    def __ensure_no_conflicts(
        self,
        artist,
        start_time,
        end_time,
        exclude_timeblock_id: int | None = None,
    ) -> None:
        has_time_block_conflict = TimeBlock.objects.has_conflict(
            artist,
            start_time,
            end_time,
            exclude_timeblock_id=exclude_timeblock_id,
        )
        has_appointment_conflict = not Appointment.objects.is_artist_available(
            artist,
            start_time,
            end_time,
        )
        if has_time_block_conflict or has_appointment_conflict:
            raise APIException(
                "The artist is not available for this time block.",
                code=status.HTTP_400_BAD_REQUEST,
            )

    def __get_artist_profile(self, user):
        try:
            return ArtistProfile.objects.get(user=user)
        except ArtistProfile.DoesNotExist:
            logger.error("Artist profile not found for user: %s", user)
            raise APIException(
                "Artist profile not found for the current user.",
                code=status.HTTP_404_NOT_FOUND,
            )

    def __create_time_block(self, validated_data, artist_profile):
        return TimeBlock.objects.create(
            studio_id=artist_profile.studio_id,
            artist=artist_profile,
            start_time=validated_data["start_time"],
            end_time=validated_data["end_time"],
            block_type=validated_data.get("block_type", TimeBlock.BlockType.OTHER),
            reason=validated_data.get("reason"),
        )

    def __get_time_block_by_id(self, time_block_id):
        try:
            return TimeBlock.objects.get_time_block_by_id(time_block_id)
        except TimeBlock.DoesNotExist:
            logger.error("Time block not found with ID: %s", time_block_id)
            raise APIException(
                "Time block not found.",
                code=status.HTTP_404_NOT_FOUND,
            )
