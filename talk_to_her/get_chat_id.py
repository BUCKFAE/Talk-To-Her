import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

from talk_to_her.talk_to_logs import logger


def main():
    load_dotenv()
    token = os.environ['TELEGRAM_TOKEN']

    application = ApplicationBuilder().token(token).build()
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), _handle_incoming_message)
    application.add_handler(echo_handler)
    logger.info(f'Listening for incoming messages')
    application.run_polling()


async def _handle_incoming_message(update: Update, _: ContextTypes.DEFAULT_TYPE):
    logger.info(f'Got message from {update.message.from_user.name} with id {update.message.from_user.id}')


if __name__ == '__main__':
    main()
