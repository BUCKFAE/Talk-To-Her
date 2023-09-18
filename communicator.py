import os
import asyncio
import telegram


async def main():

    token = os.environ['TELEGRAM_TOKEN']
    print(token)

    bot = telegram.Bot(token)
    async with bot:
        print(await bot.get_me())

        updates = await bot.get_updates(limit=5)
        for update in updates:
            print(update.message.text)

        # Send a message
        # await bot.send_message(text='Hi, Buckfae!', chat_id=6298738395)


if __name__ == '__main__':
    asyncio.run(main())