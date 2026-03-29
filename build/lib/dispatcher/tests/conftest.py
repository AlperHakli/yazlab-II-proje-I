from dispatcher.app.main import app
import pytest
from fastapi.testclient import TestClient
from constants import PROTECTED_ENDPOINTS , BOOK_SERVICE_URL , BORROW_SERVICE_URL

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
    return  BOOK_SERVICE_URL

@pytest.fixture
def borrowendpoint():
    """
    Sabit olan borrow url sini döndürür
    """
    return  BORROW_SERVICE_URL

def returnservicesdict():
    """
    tüm servislerin içerdiği dict i döndürür
    """




@pytest.fixture
def secured_endpoint_list():
    """
    :return: constants dosyasından projected endpoints listesini döndürür amaç burada dependency injection yapmaktır yine
    """
    return PROTECTED_ENDPOINTS

