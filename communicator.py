import asyncio
import os
import threading

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

from chat_application import ChatApplication
from queue import Queue


class Communicator(threading.Thread):
    """Handles the communication with telegram"""

    def __init__(self, chat_application_queue: Queue):
        super().__init__()
        load_dotenv()
        token = os.environ['TELEGRAM_TOKEN']

        self.application = ApplicationBuilder().token(token).build()
        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_incoming_message)
        self.application.add_handler(echo_handler)
        self.queue = chat_application_queue


    def run(self):
        t = threading.Thread(target=self.application.run_polling)
        loop=asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        # t.start()
        loop.run_until_complete(t.start())

    async def handle_incoming_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.name not in ['@buckfae']:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Sorry, not whitelisted!')
            return

        print('hi')
        # self.chat_handler.add_message(update.message.text, 'Oma')

        # await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


if __name__ == '__main__':
    message_queue = Queue()
    chat_app = ChatApplication(message_queue)
    communicator = Communicator(message_queue)
    communicator.start()
    chat_app.run()
