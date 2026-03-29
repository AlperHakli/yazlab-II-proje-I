from dispatcher.app.logic import forward_request
from fastapi import HTTPException , status


class DispatcherProxyService():
    """
    dispatcher e ait mikroservislere routing yapan ana class
    """
    def __init__(self , service_name: str):
        self.service_name = service_name

    async def forward(self , base_url: str , rest_of_path: str ,  user: dict):
        """
           Dispatcher den gelen endpointti book mikroservisindeki ilgili endpointe yollar
           :param base_url: ilgili endpointin ana url si
           :param rest_of_path: ulaşılcak olan endpoint
           :param user: endpointe erişen kullanıcı
           :return:
           """

        full_url = f"{base_url}/{rest_of_path}/"

        try:
            data = await forward_request(target_url=full_url, user=user)
            return data



        except HTTPException as h:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Mikroservis {self.service_name} htttpexception verdi detaylar: {h}")

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"{self.service_name} sistem hatası: {str(e)}"
            )

book_service_proxy = DispatcherProxyService("Books")
borrow_service_proxy = DispatcherProxyService("Borrow")






