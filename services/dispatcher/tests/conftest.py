from unittest.mock import patch, AsyncMock

from services.dispatcher.app.main import app
import pytest
from fastapi.testclient import TestClient
from services.dispatcher.config import settings
from services.dispatcher.app.redis_client import redis_manager


@pytest.fixture
def client():
    """
    Dependency Injection denir amaç test fonksiyonlarında client i dışarıdan vererek fonksiyon bağımlılığını azaltmaktır
    """
    return TestClient(app=app)

@pytest.fixture
def bookendpoint():
    """
    Sabit olan book url sini döndürür
    """
    return  settings.BOOK_SERVICE_URL

@pytest.fixture
def borrowendpoint():
    """
    Sabit olan borrow url sini döndürür
    """
    return  settings.BORROW_SERVICE_URL

@pytest.fixture(autouse=True)
def mock_redis():
    """
    burada redis manageri mock ederek testte gerçekten redis kullanılması engellenir
    """
    mock = AsyncMock()

    mock.return_value = "1"

    redis_manager.getUserID = mock

    return redis_manager

@pytest.fixture(scope="session", autouse=True)
def prevent_redis_connect():
    with patch("services.dispatcher.app.redis_client.RedisManager.connect", new_callable=AsyncMock), \
         patch("services.dispatcher.app.redis_client.RedisManager.close", new_callable=AsyncMock):
        yield

