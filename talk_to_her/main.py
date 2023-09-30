import multiprocessing
import time
from multiprocessing import Process

from talk_to_her.chat_application import ChatApplication
from talk_to_her.telegram_communicator import TelegramCommunicator

if __name__ == '__main__':

    # Allows communication between telegram and application
    conn_send, conn_rec = multiprocessing.Pipe()

    application = ChatApplication(conn_send)
    telegram = TelegramCommunicator(conn_rec)
    applicationProcess = Process(target=application.start_loop)
    telegramProcess = Process(target=telegram.start_loop)

    print(f'[MAIN] Starting chat application')
    applicationProcess.start()
    print(f'[MAIN]Starting telegram communicator')
    telegramProcess.start()

    while applicationProcess.is_alive() or telegramProcess.is_alive():
        time.sleep(1)
        # TODO: Kill processes
        if not applicationProcess.is_alive():
            print(f'[MAIN]: Application has stopped')
            print(f'[MAIN]: Shutting down telegram')
            telegramProcess.terminate()
