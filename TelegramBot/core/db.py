from datetime import datetime, timedelta
import asyncio

import redis.asyncio as redis
import config


class DB:
    def __init__(self, cleaner_delete_event=None):
        self.redis = redis.Redis(
            host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True
        )
        self.cleaner_task = None
        self.cleaner_delete_event = cleaner_delete_event

    async def close(self):
        await self.redis.close()

    async def getChatContext(self, chat_id):
        return await self.redis.hgetall(chat_id)

    async def setChatContext(self, chat_id, context):
        return await self.redis.hset(chat_id, mapping=context)

    async def clearChatContext(self, chat_id):
        return await self.redis.delete(chat_id)

    async def clearOld(self, chat_id):
        return await self.redis.keys()

    def startCleaner(self, cicle_update_time):
        self.cleaner_task = asyncio.create_task(self.cleaner(cicle_update_time))

    async def cleaner(self, cicle_update_time):
        while True:
            tasks = {}
            keys = await self.redis.keys()

            for key in keys:
                tasks[key] = asyncio.create_task(
                    self.redis.hget(key, "update_time")
                )
                await asyncio.sleep(0)

            for key, task in tasks.items():
                update_time_text = await task
                if update_time_text:
                    update_time = datetime.strptime(update_time_text, "%H:%M %d-%m-%Y")
                    passed_time = datetime.now() - update_time
                    if passed_time > timedelta(seconds=cicle_update_time):
                        self.cleaner_delete_event(key)
                        asyncio.create_task(self.redis.delete(key))
                await asyncio.sleep(0)

            await asyncio.sleep(cicle_update_time)
