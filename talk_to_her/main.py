import multiprocessing
import os
import time

from talk_to_her.chat_application import ChatApplication
from talk_to_her.her_logger import HerLogger
from talk_to_her.telegram_communicator import TelegramCommunicator


def start_application_loop(application):
    application.start_loop()


def start_telegram_loop(telegram):
    telegram.start_loop()


if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')

    logger = HerLogger().logger

    # https://stackoverflow.com/a/27215461
    os.system('xset r off')

    # Allows communication between telegram and application
    conn_send_a, conn_rec_t = multiprocessing.Pipe()
    conn_send_t, conn_rec_a = multiprocessing.Pipe()

    application = ChatApplication()
    telegram = TelegramCommunicator()

    application.conn_send = conn_send_a
    application.conn_rec = conn_rec_a

    telegram.conn_rec = conn_rec_t
    telegram.conn_send = conn_send_t

    applicationProcess = multiprocessing.Process(target=start_application_loop, args=(application,))
    telegramProcess = multiprocessing.Process(target=start_telegram_loop, args=(telegram,))

    telegramProcess.start()
    applicationProcess.start()

    while applicationProcess.is_alive() or telegramProcess.is_alive():
        time.sleep(1)
        if not applicationProcess.is_alive():
            logger.info(f'[MAIN]: Application has stopped')
            logger.info(f'[MAIN]: Shutting down telegram')
            telegramProcess.terminate()
