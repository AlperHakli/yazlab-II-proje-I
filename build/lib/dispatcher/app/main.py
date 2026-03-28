from logic import verify_token , forward_request

from fastapi import FastAPI , Depends

# app ana dispatcher (proxy de denir)

app = FastAPI()


app.get("/books/{rest_of_path}")
async def bookproxy(rest_of_path: str , user: dict = Depends(verify_token)):
    



