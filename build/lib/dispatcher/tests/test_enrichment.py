import respx
import httpx
from constants import SERVICES
import pytest

@pytest.mark.parametrize("endpoint" , "target_url" , SERVICES)
@respx.mock
def test_dispatcher_enriches_with_user_id(client , endpoint , target_url):
        """
        seneryo: kullanıcı geçerli token ile /books yada /borrow endpointlerine istek atar
        hedef: amaçlanan şey burada dispatcher in cevaba userID yide eklemesi
        ek not: burada amaç dispatcher ile mikroservis arasındaki bir olayı kontrol etmek
        """

        # Dispatcher mikroservis e gittiğinde sanki mikroservis doğru çalışıyomuş gibi davranılır
        # Aslında dispatcher hiç mikroservis e gitmez sadece gidiyomuş gibi yapılıp belirlediğimiz cevap dönülür
        # Bu sayede zaten bizim yazdığımız cevaptan farklı bişey dönerse dispatcher de hata var demektir
        # Yani kısaca dispatcher e ilgili url geldiğinde hiç gitmeden hazır cevap döndürür
        respx.get(target_url).mock(return_value=httpx.Response(200 , json={"data" : "original data"}))

        headers = {"Authorization": "Bearer gecerli_token_123"}
        response = client.get(endpoint , headers=headers)

        #kontroller

        # burada tekrardan 200 beklememizin sebebi dispatcher in kendisinde bir hata oluşursa hiç mikroservise gitmeden
        # bozulabilir bu sebeple bunu önleriz
        assert response.status_code == 200
        data = response.json()



        # dispatcher kodunda dönen mock dataya bir "id" parametresi eklenmesi gerekir normalde
        # eğerki bir sorun olurda eklenmezse bu kısım bozulur ve sorun anlaşılır
        assert "id" in data










