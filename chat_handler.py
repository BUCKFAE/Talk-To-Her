"""Keeps Track of messages sent"""
import json
import logging
import os.path
from collections import namedtuple


Message = namedtuple("Message", "sender message")


class ChatHandler:

    CHAT_FILE: str = 'chat_history.json'
    has_new_message: bool = False

    def __init__(self):

        if os.path.isfile(self.CHAT_FILE):
            logging.info(f'Loading existing chat from file: {self.CHAT_FILE}')
            with open(self.CHAT_FILE, 'r') as f:
                messages = json.load(f)
                self.chat = [Message(message['sender'], message['message']) for message in messages]

            logging.info(f'Previous messages: {self.chat}')
        else:
            self.chat: list[Message] = []

    def add_message(self, sender: str, message: str):
        self.chat += [Message(sender, message)]

        with open(self.CHAT_FILE, 'w') as f:
            json.dump([m._asdict() for m in self.chat], f)


if __name__ == '__main__':
    chat_handler = ChatHandler()
    chat_handler.add_message(Message('oma', 'hallo opa'))


