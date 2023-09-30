from __future__ import annotations

import os
import sys
from multiprocessing.connection import Connection

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

from talk_to_her.chat_handler import ChatHandler

class TelegramCommunicator:
    """Handles the communication with telegram"""


    def init(self):
        load_dotenv()
        token = os.environ['TELEGRAM_TOKEN']

        # Setup connection to telegram
        self.application = ApplicationBuilder().token(token).build()
        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_incoming_message)
        self.application.add_handler(echo_handler)

        self.conn_rec: Connection | None = None
        self.chat_handler = ChatHandler()

        # Bot only listens to this one chat
        self.chat_id = os.environ.get('CHAT_ID')
        assert self.chat_id is not None, f'Did not find env var CHAT_ID. '

        # Check if there is a new message once every minute
        self.job_minute = self.application.job_queue.run_repeating(self.check_for_message, interval=2, first=1)

    def start_loop(self):
        self.init()
        print(f'[TELEGRAM]: Start polling')
        self.application.run_polling()

    async def check_for_message(self, _: ContextTypes.DEFAULT_TYPE):
        """Checks if there are pending messages in the chat_handler, sends all pending messages"""

        if self.conn_rec.poll():
            msg = self.conn_rec.recv()
            print(f'[TELEGRAM]: Got message: {msg}')
            self.send_message(msg)

    def send_message(self, msg: str):
        print(f"trying to send to {self.chat_id}")
        if self.chat_id:
            self.application.create_task(self._send_message(self.chat_id, msg))

    async def _send_message(self, chat_id: int, msg: str):
        print("Sending Now")
        send_msg = await self.application.bot.send_message(chat_id=chat_id, text=msg)
        self.chat_handler.add_message_to_log(send_msg.id, 'Opa', send_msg.text)

    async def handle_incoming_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.name not in ['@buckfae']:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Sorry, not whitelisted!')
            return
        print(f"{self.chat_id} vs {update.effective_chat.id} {not self.chat_id}")
        if not self.chat_id:
            self.chat_id = update.effective_chat.id
            print(self.chat_id)
        self.chat_handler.add_message_to_log(update.message.id, 'Oma', update.message.text)


        await context.bot.send_message(chat_id=update.effective_chat.id, text='[OPA] hat deine Nachricht erhalten!!')

if __name__ == '__main__':
    TelegramCommunicator()

