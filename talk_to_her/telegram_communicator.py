from __future__ import annotations

import os
from logging import Logger
from multiprocessing.connection import Connection

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, Job, Application

from talk_to_her.chat_handler import ChatHandler
from talk_to_her.her_logger import HerLogger


class TelegramCommunicator:
    """Handles the communication with telegram"""

    conn_send: Connection | None = None
    conn_rec: Connection | None = None

    # Will be set in the setup method
    chat_id: int
    check_new_messages_job: Job
    telegram: Application

    # Used for logging
    prefix = '[TELEGRAM] '
    logger: Logger

    def setup(self):
        self.logger = HerLogger().logger
        self.logger.info(self.prefix + 'Setup ...')

        # Load stuff from env vars
        load_dotenv()
        token = os.environ.get('TELEGRAM_TOKEN')
        assert token is not None, f'Did not find env var TELEGRAM_TOKEN'
        chat_env = os.environ.get('CHAT_ID')  # Bot only listens to this chat
        assert chat_env is not None, f'Did not find env var CHAT_ID'
        assert chat_env.isnumeric(), f'CHAT_ID is not numeric!'
        self.chat_id = int(chat_env)

        # Setup connection to telegram
        self.telegram = ApplicationBuilder().token(token).build()
        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_incoming_message)
        self.telegram.add_handler(echo_handler)

        # Check if there is a new message once every minute
        self.check_new_messages_job = self.telegram.job_queue.run_repeating(self.send_outgoing_messages, interval=1, first=1)

    def start_loop(self):
        self.setup()
        self.logger.info(self.prefix + 'Start polling')
        self.telegram.run_polling()

    async def send_outgoing_messages(self, _: ContextTypes.DEFAULT_TYPE):
        while self.conn_rec.poll():
            msg = self.conn_rec.recv()
            self.logger.info(self.prefix + f'Got message: {msg}')
            self.send_message(msg)

    async def _send_message(self, chat_id: int, msg: str):
        send_msg = await self.telegram.bot.send_message(chat_id=chat_id, text=msg)
        self.conn_send.send((send_msg.id, 'Opa', send_msg.text))

    def send_message(self, msg: str):
        self.logger.info(self.prefix + f'Sending message to chat {self.chat_id}')
        self.logger.info(self.prefix + f'Message: {msg}')
        if self.chat_id:
            self.telegram.create_task(self._send_message(self.chat_id, msg))

    async def handle_incoming_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_user.id == self.chat_id:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Sorry, not whitelisted!')
            self.logger.info(self.prefix + f'Got message from no-whitelisted user: {update.effective_user.id}')
            return
        self.conn_send.send((update.message.id, 'Oma', update.message.text))
        await context.bot.send_message(chat_id=update.effective_chat.id, text='[OPA] hat deine Nachricht erhalten!!')


if __name__ == '__main__':
    TelegramCommunicator()
