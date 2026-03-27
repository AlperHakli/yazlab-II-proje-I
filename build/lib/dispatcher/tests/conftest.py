from dispatcher.app.main import app
import pytest
from fastapi.testclient import TestClient
from constants import PROTECTED_ENDPOINTS

@pytest.fixture
def client():
    """
    Dependency Injection denir amaç test fonksiyonlarında client i dışarıdan vererek fonksiyon bağımlılığını azaltmaktır
    """
    return TestClient(app=app)

@pytest.fixture
def secured_endpoint_list():
    """
    :return: constants dosyasından projected endpoints listesini döndürür amaç burada dependency injection yapmaktır yine
    """
    return PROTECTED_ENDPOINTS

