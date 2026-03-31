import httpx

from fastapi import HTTPException, status


class DispatcherProxyService():
    """
    dispatcher e ait mikroservislere routing yapan ana class
    """

    def __init__(self, service_name: str):
        self.service_name = service_name

    async def forward(
            self,
            base_url: str,
            rest_of_path: str,
            method: str,
            body,
            headers: dict,
            request_data: dict = None,
            user: dict = None

    ):
        """
           Dispatcher den gelen endpointti book mikroservisindeki ilgili endpointe yollar
           :param base_url: ilgili endpointin ana url si
           :param rest_of_path: ulaşılcak olan endpoint
           :param user: endpointe erişen kullanıcı
           :return:
           """

        base = base_url.rstrip("/")
        path = rest_of_path.strip("/")

        if path:
            full_url = f"{base}/{path}"
        else:
            full_url = base

        try:

            #mikroservise istek atılır (burada isteği dispatcher atıyo ondan client dispatcher)
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=method,
                    url=full_url,
                    content=body,
                    headers=headers,
                    timeout=10.0
                )

                # mikroservis in hata kodu yansılılır
                if response.status_code >= 400:
                    raise HTTPException(status_code=response.status_code, detail=response.json())

                response_data = response.json()

            if user and isinstance(response_data, dict):
                response_data["id"] = user.get("id")

                return response_data




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
auth_service_proxy = DispatcherProxyService("Auth")






