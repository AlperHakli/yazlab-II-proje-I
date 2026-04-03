import pytest
from services.dispatcher.config import settings
import respx
import httpx

#TEST A
@pytest.mark.parametrize("endpoint", settings.PROTECTED_ENDPOINTS)
def test_endpoints_require_auth(client, endpoint):
    """
    bu test verilen listedeki tüm endpointler için daha dispatcher seviyesinde yetkisiz erişimmi kontrol eder auth testi yapar
    """
    # seneryo:


    response = client.get(endpoint)
    assert response.status_code == 401

    assert "yetkisiz erişim" in response.json()["detail"].lower()


#TEST B

@pytest.mark.parametrize("endpoint", settings.PROTECTED_ENDPOINTS)
@respx.mock
def test_valid_auth_success(client, endpoint):
    """
    dispatcher seviyesinde geçerli bir token varmı kontrol eder token geçerliyse başarılı 200 döndürmesi gerekir
    """
    # senaryo: Veritabanımızda olan geçerli bir token gönderiyoruz

    my_mock_route = respx.get(url__startswith="http://").mock(
        return_value=httpx.Response(200, json={"message": "Mocklanmış Veri"})
    )

    headers = {"Authorization": "Bearer gecerli_token_123"}
    response = client.get(endpoint, headers=headers)

    # Beklenti: 200 OK
    assert response.status_code == 200, f"{endpoint} yolu geçerli token ile 200 dönmedi!"
