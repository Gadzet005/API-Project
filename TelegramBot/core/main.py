import asyncio

import config
from bots import TelegramBot


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    bot = TelegramBot(config.API_TOKEN)
    loop.create_task(bot.startWork())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Завершение работы")
    finally:
        stop_task = loop.create_task(bot.stopWork())
        loop.run_until_complete(stop_task)
