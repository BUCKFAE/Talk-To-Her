"""Keeps Track of messages sent"""
import json
import os.path
from collections import namedtuple

from talk_to_her.her_logger import HerLogger

Message = namedtuple("Message", "id sender message")


class ChatHandler:
    CHAT_FILE: str = 'chat_history.json'
    prefix = '[CHAT-HANDLER] '

    def __init__(self):
        self.logger = HerLogger().logger

        self.logger.info(self.prefix + 'Created new chat handler!')
        # Loading chat history
        if os.path.isfile(self.CHAT_FILE):
            self.logger.info(self.prefix + f'Loading existing chat from file: {self.CHAT_FILE}')
            self.update()
            self.logger.info(self.prefix + f'Finished loading {len(self.chat)} previous messages')
        else:
            self.chat: list[Message] = []

    def add_message_to_log(self, message_id: int, sender: str, message: str):
        """Add a message that was successfully sent by the telegramm_communicator to the chat history"""
        msg = Message(message_id, sender, message)
        self.chat += [msg]
        with open(self.CHAT_FILE, 'w') as f:
            json.dump([{'id': m.id, 'sender': m.sender, 'message': m.message} for m in self.chat], f)
        self.update()

    def update(self):
        """Ensures self.chat is on the latest state"""

        if not os.path.isfile(self.CHAT_FILE):
            return

        with open(self.CHAT_FILE, 'r') as f:
            messages = json.load(f)
            self.chat = [Message(message['id'], message['sender'], message['message']) for message in messages]
