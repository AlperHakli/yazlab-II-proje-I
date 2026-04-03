from fastapi import status






def test_login_success(authendpoint, authclient, mock_redis):
    mock_credentials = {
        "userName": "admin",
        "password": "admin123"
    }

    response = authclient.post("/login", json=mock_credentials)

    # KONTROLLER
    assert response.status_code == 200


    # mock_redis.setToken.assert_called_once()

    response_json = response.json()
    assert "access_token" in response_json


def test_login_failed_wrong_credentials(authendpoint , authclient , mock_redis):
    """
    Kullanıcı girişi başarısız olduğunda 401 (unauthorized) döndürüyomu kontrol eder

    :param authendpoint: otomatik olarak conftest den gelir auth mikroservisinin ana endpointi
    """

    mock_credentials = {
        "userName": "admin",
        "password": "wrongadmin123"
    }



    # istek atılır
    response = authclient.post("/login", json=mock_credentials)

    # doğru cevap kodu gelmesi gerekir
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, f"Login failed testinde status code 401 gelmesi gerekirdi yerine {response.status_code} geldi"





