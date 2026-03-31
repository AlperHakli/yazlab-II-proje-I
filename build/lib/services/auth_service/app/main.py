from contextlib import asynccontextmanager

from fastapi import FastAPI
from services.auth_service.app.pydantic_models import LoginRequest , SignUpRequest
from services.auth_service.app.logic import login_logic , signup_logic
from services.auth_service.app.redis_client import redis_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Uygulama başlarken bağlantıyı kur
    await redis_manager.connect()
    yield
    # Uygulama kapanırken bağlantıyı kes
    await redis_manager.close()

app = FastAPI(lifespan=lifespan)


@app.post("/login")
async def login(request: LoginRequest):
    return await login_logic(request=request)

@app.post("/signup")
async def signup(request: SignUpRequest):
    return await signup_logic(request=request)
