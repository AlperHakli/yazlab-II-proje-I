import pytest
from constants import PROTECTED_ENDPOINTS

@pytest.mark.parametrize("endpoint" , PROTECTED_ENDPOINTS)
def test_endpoints_require_auth(client, endpoint):
    """
    bu test verilen listedeki tüm endpointler için daha dispatcher seviyesinde yetkisiz erişimmi kontrol eder auth testi yapar
    """
    # seneryo:
    response = client.get(endpoint)
    assert response.status_code == 401

    assert "yetkisiz erişim" in response.json()["detail"].lower()


@pytest.mark.parametrize("endpoint" , PROTECTED_ENDPOINTS)
def test_valid_auth_success(client , endpoint):
    """
    dispatcher seviyesinde geçerli bir token varmı kontrol eder token geçerliyse başarılı 200 döndürmesi gerekir
    """
    # senaryo: Veritabanımızda olan geçerli bir token gönderiyoruz
    headers = {"Authorization": "Bearer gecerli_token_123"}
    response = client.get(endpoint, headers=headers)

    # Beklenti: 200 OK
    assert response.status_code == 200, f"{endpoint} yolu geçerli token ile 200 dönmedi!"