"""Keeps Track of messages sent"""
import json
import logging
import os.path
from collections import namedtuple


Message = namedtuple("Message", "id sender message")


class ChatHandler:

    CHAT_FILE: str = 'chat_history.json'

    def __init__(self,queue=None):
        self.queue = queue
        if os.path.isfile(self.CHAT_FILE):
            logging.info(f'Loading existing chat from file: {self.CHAT_FILE}')
            self.update()
            logging.info(f'Previous messages: {self.chat}')
        else:
            self.chat: list[Message] = []

    def add_message(self, message_id: int, sender: str, message: str):
        msg = Message(message_id, sender, message)
        self.chat += [msg]
        if self.queue:
            self.queue.put(msg)
        with open(self.CHAT_FILE, 'w') as f:
            json.dump([m._asdict() for m in self.chat], f)
        self.update()

    def update(self):

        if not os.path.isfile(self.CHAT_FILE):
            return

        with open(self.CHAT_FILE, 'r') as f:
            messages = json.load(f)
            self.chat = [Message(message['id'], message['sender'], message['message']) for message in messages]


if __name__ == '__main__':
    chat_handler = ChatHandler()


