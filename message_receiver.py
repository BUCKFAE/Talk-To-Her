import asyncio
import os
import threading

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

from chat_handler import ChatHandler


class MessageReceiver:
    """Handles the communication with telegram"""

    def __init__(self):
        super().__init__()
        load_dotenv()
        token = os.environ['TELEGRAM_TOKEN']

        self.application = ApplicationBuilder().token(token).build()
        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_incoming_message)
        self.application.add_handler(echo_handler)
        self.chat_handler = ChatHandler()
        self.application.run_polling()

    async def handle_incoming_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.name not in ['@buckfae']:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Sorry, not whitelisted!')
            return
        self.chat_handler.add_message(update.message.id, 'Oma', update.message.text)


        await context.bot.send_message(chat_id=update.effective_chat.id, text='Got it!')

if __name__ == '__main__':
    MessageReceiver()

