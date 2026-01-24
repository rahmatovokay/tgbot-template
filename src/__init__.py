from .dependencies import check_dependencies

from .settings import get_redis
from .core import bot_core
# from .sdk import SDK

# sdk = SDK()

_redis_instance = None

async def get_redis_client():
    global _redis_instance
    if _redis_instance is None:
        _redis_instance = await get_redis()
    return _redis_instance

async def close_redis():
    global _redis_instance
    if _redis_instance is not None:
        await _redis_instance.close()
        _redis_instance = None

class RedisClient:
    def __getattr__(self, name):
        import asyncio
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
        
        if loop is not None:
            async def _wrapper(*args, **kwargs):
                client = await get_redis_client()
                method = getattr(client, name)
                return await method(*args, **kwargs)
            return _wrapper
        else:
            raise RuntimeError("Redis client must be accessed from async context")

redis = RedisClient()

bot_manager = bot_core.BotManager()
bot_manager.initialize()

bot = bot_manager.bot
dp = bot_manager.dp