"""Keeps Track of messages sent"""
import json
import logging
import os.path
from collections import namedtuple


Message = namedtuple("Message", "id sender message")


class ChatHandler:

    CHAT_FILE: str = 'chat_history.json'

    def __init__(self):

        if os.path.isfile(self.CHAT_FILE):
            logging.info(f'Loading existing chat from file: {self.CHAT_FILE}')
            self.update()
            logging.info(f'Previous messages: {self.chat}')
        else:
            self.chat: list[Message] = []

    def add_message(self, message_id: int, sender: str, message: str):
        self.chat += [Message(message_id, sender, message)]
        with open(self.CHAT_FILE, 'w') as f:
            json.dump([m._asdict() for m in self.chat], f)
        self.update()

    def update(self):
        with open(self.CHAT_FILE, 'r') as f:
            messages = json.load(f)
            self.chat = [Message(message['id'], message['sender'], message['message']) for message in messages]


if __name__ == '__main__':
    chat_handler = ChatHandler()


