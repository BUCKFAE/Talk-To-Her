from __future__ import annotations

import tkinter as tk
from multiprocessing.connection import Connection
from tkinter import scrolledtext

import speech_recognition as sr

from talk_to_her.chat_handler import ChatHandler


class ChatApplication:
    conn_send: Connection | None = None
    conn_rec: Connection | None = None

    def init(self):

        """TODO: Load old messages on init"""

        # Setup Window
        self.root = tk.Tk()
        # self.root.attributes('-fullscreen', True)
        self.root.title("Rede mit ihr")
        self.root.geometry("1920x1080")

        self.font = ("TkDefaultFont", 50)

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

        self.shown_ids: list[int] = []

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.recognizer = sr.Recognizer()
        self.root.bind("<KeyPress>", self.key_up)

        self.chat_area.after(1000, self.fetch_messages)

    def start_loop(self):
        self.init()
        print(f'[CHAT-APP]: Start main loop')
        self.root.mainloop()

    def key_up(self, key):

        # Prevent multiple key-presses
        self.root.unbind("<KeyPress>")

        if not key.char == ' ':
            print(f'Ignoring key: {key}')
            self.root.bind("<KeyPress>", self.key_up)
            return

        # with sr.Microphone() as source:
        #     print('Speak now!')
        #     audio = self.recognizer.listen(source)
        #
        # print(f'Finished listening!')
        # text = self.recognizer.recognize_google(audio, language='de-DE')
        text = 'test'
        print(f'[APP]: Text: {text}')

        self.conn_send.send(text)

        # Listen for keys again
        self.root.bind("<KeyPress>", self.key_up)

    def fetch_messages(self):

        if self.conn_rec.poll():
            msg_id, msg_sender, msg_text = self.conn_rec.recv()
            print(f'[APP] Got message: ({msg_id}) - {msg_sender}: {msg_text}')
            self.add_message_to_area(msg_id, msg_sender, msg_text)

        self.chat_area.after(1000, self.fetch_messages)

    def on_close(self):
        self.root.destroy()

    def add_message_to_area(self, msg_id, msg_sender, msg_text):
        print(f'Add msg e')
        if msg_id not in self.shown_ids:
            self.chat_area.configure(state='normal')
            if msg_sender == 'Oma':
                self.chat_area.insert(tk.END, f"SIE: {msg_text}\n", 'left')
            elif msg_sender == 'Opa':
                self.chat_area.insert(tk.END, f"DU: {msg_text}\n", 'right')
            else:
                raise ValueError(f'Unknown sender: {msg_sender}')
            self.chat_area.configure(state='disabled')
            self.chat_area.see(tk.END)

            self.shown_ids.append(msg_id)


if __name__ == '__main__':
    ChatApplication()
