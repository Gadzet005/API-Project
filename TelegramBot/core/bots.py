import math
import asyncio
import json
from datetime import datetime

import aiohttp
from db import DB
import config


class BaseTelegramBot:
    def __init__(self, token):
        self.token = token
        self.current_update_id = 0
        self.commands = {}
        self.db = DB(cleaner_delete_event=self.cleaner_delete_event)

    async def _useMethod(self, method_name, request_method_name="GET", **kwargs):
        async with aiohttp.ClientSession() as session:
            if request_method_name == "GET":
                request_method = session.get
            else:
                request_method = session.post

            async with request_method(
                f"https://api.telegram.org/bot{self.token}/{method_name}",
                data=kwargs
            ) as response:
                return await response.json()

    def useGetMethod(self, method_name, **kwargs):
        return asyncio.create_task(self._useMethod(method_name, "GET", **kwargs))

    def usePostMethod(self, method_name, **kwargs):
        return asyncio.create_task(self._useMethod(method_name, "POST", **kwargs))

    def sendMessage(self, chat_id, text):
        return self.usePostMethod("sendMessage", chat_id=chat_id, text=text)

    async def sendBigMessage(self, chat_id, text):
        for i in range(math.ceil(len(text) / 4000)):
            text_fragment = text[4000 * i:4000 * (i + 1)]
            await self.sendMessage(chat_id, text_fragment)

    def editMessage(self, chat_id, message_id, text):
        return self.usePostMethod(
            "editMessageText", chat_id=chat_id, message_id=message_id, text=text
        )

    def deleteMessage(self, chat_id, message_id):
        return self.usePostMethod("deleteMessage", chat_id=chat_id, message_id=message_id)

    async def setBotCommands(self):
        bot_commands = [
            {"command": command, "description": command_info.get("description")}
            for command, command_info in self.commands.items()
        ]
        await self.usePostMethod("setMyCommands", commands=json.dumps(bot_commands))

    async def updatesReceiver(self):
        while True:
            response = await self.useGetMethod("getUpdates", offset=self.current_update_id + 1)
            updates = response.get("result")

            for update in updates:
                self.current_update_id = update.get("update_id")
                asyncio.create_task(self.receiveMessage(update.get("message")))
                await asyncio.sleep(0)

    async def receiveMessage(self, message):
        chat_id = message.get("chat").pop("id")
        text = message.get("text")

        context = await self.db.getChatContext(chat_id)
        _ = context.pop("update_time", None)
        command_name = context.get("command_name") if context else text
        command = self.commands.get(command_name)

        if command:
            func = command.get("func")
            asyncio.create_task(func(chat_id, message, context))
        else:
            self.sendMessage(chat_id, "Даже не знаю, что вам ответить...")

    async def startWork(self):
        await self.setBotCommands()
        asyncio.create_task(self.updatesReceiver())
        self.db.startCleaner(12 * 60 * 60)
        print("Бот успешно запущен")

    async def stopWork(self):
        await self.db.close()

    def cleaner_delete_event(self, chat_id):
        self.sendMessage(chat_id, "Вы слишком долго не отвечали. Ввод данных сброшен")


class TelegramBot(BaseTelegramBot):
    def __init__(self, token):
        super().__init__(token)
        self.commands = {
            "/start": {
                "func": self.start, "description": "Приветствие"
            },
            "/show_all_posts": {
                "func": self.showPosts, "description": "Показать все посты"
            },
            "/show_post": {
                "func": self.showPost, "description": "Показать пост"
            },
            "/get_auth_token": {
                "func": self.getAuthToken, "description": "Получить токен"
            },
        }

    def postToText(self, post):
        title, text, creation_date = post.get('title'), post.get("text"), post.get('creation_date')
        author = post.get("author_info").get("name")

        creation_date_object = datetime.strptime(creation_date, "%Y-%m-%dT%H:%M:%S.%f%z")
        creation_date_text = creation_date_object.strftime("%H:%M %d-%m-%Y")

        return title + f"\nАвтор {author}\nДата и время создания: {creation_date_text}\n" + text

    async def getBackendData(self, path):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{config.BACKEND_DOMEN}/api/v1/{path}",) as response:
                result = await response.json()
                status_code = response.status
        return status_code, result

    async def start(self, chat_id, message, context):
        first_name = message.get("chat").get("first_name")

        self.sendMessage(
            chat_id, f"Привет, {first_name}. Я не очень умный бот, но постараюсь тебе помочь"
        )

    async def showPosts(self, chat_id, message, context):
        send_message_task = self.sendMessage(chat_id, "Получаю информацию...")

        status_code, posts = await self.getBackendData("posts/")
        posts_info = [
            f"[{idx}] " + self.postToText(post)
            for idx, post in enumerate(posts, start=1)
        ]
        message_text = ("\n" + "-" * 50 + "\n").join(posts_info)
        sended_message_response = await send_message_task
        sended_message_id = sended_message_response.get("result").get("message_id")

        self.deleteMessage(chat_id, sended_message_id)
        asyncio.create_task(self.sendBigMessage(chat_id, message_text))

    async def showPost(self, chat_id, message, context):
        step = len(context.keys())

        if step == 0:
            await self.db.setChatContext(chat_id, {
                "command_name": "/show_post",
                "update_time": datetime.now().strftime("%H:%M %d-%m-%Y")
            })
            self.sendMessage(chat_id=chat_id, text="Укажите id поста")
        else:
            try:
                post_id = int(message.get("text"))
            except ValueError:
                self.sendMessage(chat_id, "Введите число")
                return

            status_code, post = await self.getBackendData(f"posts/{post_id}")
            message_text = self.postToText(post) if status_code == 200 else "Такого поста нет..."

            await self.db.clearChatContext(chat_id)
            asyncio.create_task(self.sendBigMessage(chat_id, message_text))

    async def getAuthToken(self, chat_id, message, context):
        step = len(context.keys())

        if step == 0:
            await self.db.setChatContext(chat_id, {
                "command_name": "/get_auth_token",
                "update_time": datetime.now().strftime("%H:%M %d-%m-%Y")
            })
            self.sendMessage(chat_id, "Укажите имя пользователя")
        elif step == 1:
            await self.db.setChatContext(chat_id, {
                **context, "username": message.get("text"),

                })
            self.sendMessage(chat_id, "Укажите пароль")
        else:
            data = {"username": context.get("username"), "password": message.get("text")}
            async with aiohttp.ClientSession() as session:
                async with session.post(f"http://{config.BACKEND_DOMEN}/api/v1/oauth/", data=data) as response:
                    result = await response.json()
                    status_code = response.status

            if status_code == 200:
                message_text = f"Ваш токен: {result.get('token')}"
            else:
                message_text = "Неправильное имя пользователя или пароль"
            await self.db.clearChatContext(chat_id)
            self.sendMessage(chat_id, message_text)
