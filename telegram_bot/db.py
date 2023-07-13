import redis.asyncio as redis
import config


class DB:
    def __init__(self):
        self.redis = redis.Redis(
            host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True
        )

    async def close(self):
        await self.redis.close()

    async def get_chat_context(self, chat_id):
        return await self.redis.hgetall(chat_id)

    async def set_chat_context(self, chat_id, context):
        return await self.redis.hset(chat_id, mapping=context)

    async def clear_chat_context(self, chat_id):
        return await self.redis.delete(chat_id)
