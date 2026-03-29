import pytest

from envconfig_and_settings import Settings


@pytest.fixture
def authendpoint():
    """
    Sabit olan ana auth url sini döndürür
    """
    return Settings.BOOK_SERVICE_URL