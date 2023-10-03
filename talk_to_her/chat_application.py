from __future__ import annotations

import tkinter as tk
from logging import Logger
from multiprocessing.connection import Connection
from tkinter import scrolledtext

import speech_recognition as sr

from talk_to_her.chat_handler import ChatHandler
from talk_to_her.her_logger import HerLogger


class ChatApplication:
    conn_send: Connection | None = None
    conn_rec: Connection | None = None

    prefix = "[CHAT-APP] "
    logger: Logger

    # Window
    font = ("TkDefaultFont", 50)
    root: tk.Tk
    chat_area: scrolledtext.ScrolledText
    shown_msg_ids: list[int] = []

    chat_handler: ChatHandler
    recognizer = sr.Recognizer

    def init(self):

        self.logger = HerLogger().logger
        self.logger.info(self.prefix + 'Setup ...')

        # Setup Window
        self.root = tk.Tk()
        # self.root.attributes('-fullscreen', True)
        self.root.title("Rede mit ihr")
        self.root.geometry("1920x1080")

        # Setup chat frame
        chat_frame = tk.Frame(self.root)
        chat_frame.pack(fill=tk.BOTH, expand=True)
        chat_frame.grid_rowconfigure(0, weight=9)  # This will allow chat_area to occupy most of the vertical space
        chat_frame.grid_columnconfigure(0, weight=1)  # Single column which will occupy the entire width

        # Setup chat area
        self.chat_area = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD)
        self.chat_area.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.chat_area.configure(state='disabled')

        # Setup tags for left and right aligned messages
        self.chat_area.tag_configure('left', justify='left', background='lightblue', lmargin2=10, font=self.font)
        self.chat_area.tag_configure('right', justify='right', background='lightgreen', rmargin=10, font=self.font)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.chat_handler = ChatHandler()
        for previous_message in self.chat_handler.chat:
            self.add_message_to_area(*previous_message)

        self.recognizer = sr.Recognizer()
        self.root.bind("<KeyPress>", self.key_up)
        self.chat_area.after(1000, self.fetch_messages)

    def start_loop(self):
        self.init()
        self.logger.info(self.prefix + 'Start main loop')
        self.root.mainloop()

    def key_up(self, key):

        # Prevent multiple key-presses
        self.root.unbind("<KeyPress>")

        # Ignore all keys but space
        if not key.char == ' ':
            self.logger.info(f'Ignoring key: {key}')
            self.root.bind("<KeyPress>", self.key_up)
            return

        # Listen to user speakV
        with sr.Microphone() as source:
            self.logger.info(self.prefix + 'Speak now!')
            # audio = self.recognizer.listen(source)
            while not keyboard.is_pressed('space'):
                pass
            audio = self.recognizer.listen(source)

        self.logger.info(self.prefix + 'Finished listening!')
        text = self.recognizer.recognize_google(audio, language='de-DE')
        # text = 'Sample text'
        self.logger.info(self.prefix + f'Text: {text}')

        # Schedule message to be sent via telegram
        self.conn_send.send(text)

        # Listen for keys again
        self.root.bind("<KeyPress>", self.key_up)

    def fetch_messages(self):
        # CHeck if there are new messages from telegram
        if self.conn_rec.poll():
            msg_id, msg_sender, msg_text = self.conn_rec.recv()
            self.logger.info(self.prefix + f'Got message: ({msg_id}) - {msg_sender}: {msg_text}')
            self.chat_handler.add_message_to_log(msg_id, msg_sender, msg_text)
            self.add_message_to_area(msg_id, msg_sender, msg_text)
        self.chat_area.after(1000, self.fetch_messages)

    def on_close(self):
        self.root.destroy()

    def add_message_to_area(self, msg_id, msg_sender, msg_text):
        self.logger.info(self.prefix + f'Adding message to chat area: ({msg_sender}) - {msg_sender}: {msg_text}')
        if msg_id not in self.shown_msg_ids:
            self.chat_area.configure(state='normal')
            if msg_sender == 'Oma':
                self.chat_area.insert(tk.END, f"SIE: {msg_text}\n", 'left')
            elif msg_sender == 'Opa':
                self.chat_area.insert(tk.END, f"DU: {msg_text}\n", 'right')
            else:
                raise ValueError(f'Unknown sender: {msg_sender}')
            self.chat_area.configure(state='disabled')
            self.chat_area.see(tk.END)
            self.shown_msg_ids.append(msg_id)


if __name__ == '__main__':
    ChatApplication()
