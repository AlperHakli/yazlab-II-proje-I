import redis.asyncio as redis
from services.dispatcher.config import settings


class RedisManager():
    def __init__(self, redis_port: int, redis_host: str):
        self.redis_port = redis_port
        self.redis_host = redis_host
        self.redis_client= None

    async def connect(self):
        self.redis_client = redis.Redis(
            host=self.redis_host,
            port=self.redis_port,
            decode_responses=True
        )

    async def getUserID(self, token: str):
        """Token karşılığındaki userID'yi getirir (Dispatcher kullanacak)."""
        return await self.redis_client.get(token)

    async def close(self):
        """Bağlantıyı güvenli kapatır."""
        if self.redis_client:
            await self.redis_client.aclose()


redis_manager = RedisManager(redis_port=settings.REDIS_PORT, redis_host=settings.REDIS_HOST)
