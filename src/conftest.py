import os
from pathlib import Path

import pytest
from django.conf import settings
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path, override=True)


@pytest.fixture(autouse=True)
def django_db_setup():
    """Override database settings for tests from environment variables"""
    settings.DATABASES["default"]["HOST"] = "localhost"
    settings.DATABASES["default"]["PORT"] = os.getenv("POSTGRES_PORT")
    settings.DATABASES["default"]["NAME"] = os.getenv("POSTGRES_NAME")
    settings.DATABASES["default"]["USER"] = os.getenv("POSTGRES_USER")
    settings.DATABASES["default"]["PASSWORD"] = os.getenv("POSTGRES_PASSWORD")
