import respx
import httpx
from fastapi import status

def test_login_success(authendpoint):
    """
    Kullanıcı başarıyla giriş yaptığında 200 (başarılı işlem kodu) dönüyomu
    ve cevapta access token varmı kontrol eder

    :param authendpoint: otomatik olarak conftest den gelir auth mikroservisinin ana endpointi
    """

    mock_credentials = {
        "username":"admin",
        "password":"admin123"
    }

    #istek atılır
    response = httpx.post(authendpoint , json= mock_credentials)

    #kontroller

    responsejson = response.json()

    #doğru cevap kodu gelmesi gerekir
    assert response.status_code == status.HTTP_200_OK , f"Login success testinde status code 200 gelmesi gerekirdi yerine {response.status_code} geldi"
    assert "access_token" in responsejson
    assert responsejson["token_type"] == "bearer"


def test_login_failed_wrong_credentials(authendpoint):
    """
    Kullanıcı girişi başarısız olduğunda 401 (unauthorized) döndürüyomu kontrole eder

    :param authendpoint: otomatik olarak conftest den gelir auth mikroservisinin ana endpointi
    """

    mock_credentials = {
        "username": "admin",
        "password": "wrongadmin123"
    }

    # istek atılır
    response = httpx.post(authendpoint, json=mock_credentials)

    # kontroller

    responsejson = response.json()

    # doğru cevap kodu gelmesi gerekir
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, f"Login failed testinde status code 401 gelmesi gerekirdi yerine {response.status_code} geldi"





