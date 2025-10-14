import pytest

from api.services.time_block_service import TimeBlockService


@pytest.mark.django_db
class TestTimeBlockService:

    def test_create_time_block_successfully(
        self, registered_user, create_time_block_validated_data
    ):
        service = TimeBlockService()
        time_block = service.create_time_block(
            registered_user, create_time_block_validated_data
        )
        assert time_block.id is not None
        assert time_block.start_time == create_time_block_validated_data["start_time"]
        assert time_block.end_time == create_time_block_validated_data["end_time"]
        assert time_block.block_type == create_time_block_validated_data["block_type"]
        assert time_block.reason == create_time_block_validated_data["reason"]

    def test_create_time_block_with_unexisting_artist_profile(
        self, fake_user, create_time_block_validated_data
    ):
        service = TimeBlockService()
        with pytest.raises(Exception) as exc_info:
            service.create_time_block(fake_user, create_time_block_validated_data)
        assert "Artist profile not found for the current user" in str(exc_info.value)
