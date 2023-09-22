import time
from multiprocessing import Process, Queue

from talk_to_her.chat_application import ChatApplication
from talk_to_her.telegram_communicator import TelegramCommunicator


import speech_recognition as sr
def call_init(target):
    target.init()

if __name__ == '__main__':

    message_recieve_queue = Queue()
    message_send_queue = Queue()
    telegram = TelegramCommunicator(message_recieve_queue, message_send_queue)
    application = ChatApplication(message_send_queue, message_recieve_queue)
    telegramProcess = Process(target=call_init, args=(telegram,))
    applicationProcess = Process(target=call_init, args=(application,))
    telegramProcess.start()
    applicationProcess.start()

    while applicationProcess.is_alive() or telegramProcess.is_alive():
        if not message_recieve_queue.empty():
            msg = message_recieve_queue.get_nowait()
            print(f"received: {msg}")
        time.sleep(1)
        if not applicationProcess.is_alive():
            # Killing telegram
            message_send_queue.put("||killmenow||DOIT||JUSTDOITNOW||")

