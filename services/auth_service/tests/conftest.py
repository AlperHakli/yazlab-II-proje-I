from unittest.mock import AsyncMock, patch

import pytest
from envconfig_and_settings import Settings
from services.auth_service.app.main import app
from fastapi.testclient import TestClient

from services.auth_service.app.redis_client import redis_manager


@pytest.fixture
def authendpoint():
    """
    Sabit olan ana auth url sini döndürür
    """
    return Settings.AUTH_SERCICE_URL

@pytest.fixture
def authclient():
    """
    Auth service test clienti döndürür
    """
    with TestClient(app) as client:
        yield client

@pytest.fixture(autouse=True)
def mock_redis():
    """
    burada redis manageri mock ederek testte gerçekten redis kullanılması engellenir
    """
    redis_manager.setToken = AsyncMock()
    return redis_manager

@pytest.fixture(scope="session", autouse=True)
def prevent_redis_connect():
    with patch("services.auth_service.app.redis_client.RedisManager.connect", new_callable=AsyncMock), \
         patch("services.auth_service.app.redis_client.RedisManager.close", new_callable=AsyncMock):
        yield
