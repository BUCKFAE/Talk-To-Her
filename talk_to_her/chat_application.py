import tkinter as tk
from tkinter import scrolledtext


import speech_recognition as sr

from talk_to_her.chat_handler import ChatHandler
from talk_to_her.talk_to_logs import logger


class ChatApplication:

    def __init__(self, send_queue, recieve_queue):

        super().__init__()
        self.send_queue = send_queue
        self.recieve_queue = recieve_queue
        self.root = tk.Tk()
        # self.root.attributes('-fullscreen', True)
        self.root.title("Rede mit ihr")
        self.root.geometry("1920x1080")

        self.font = ("TkDefaultFont", 50)

        chat_frame = tk.Frame(self.root)
        chat_frame.pack(fill=tk.BOTH, expand=True)
        chat_frame.grid_rowconfigure(0, weight=9)  # This will allow chat_area to occupy most of the vertical space
        chat_frame.grid_rowconfigure(1, weight=1)  # Space for the button
        chat_frame.grid_columnconfigure(0, weight=1)  # Single column which will occupy the entire width

        # Setup chat window
        self.chat_area = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD)
        self.chat_area.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.chat_area.configure(state='disabled')

        # Setup tags for left and right aligned messages
        self.chat_area.tag_configure('left', justify='left', background='lightblue', lmargin2=10, font=self.font)
        self.chat_area.tag_configure('right', justify='right', background='lightgreen', rmargin=10, font=self.font)

        self.chat_handler = ChatHandler()
        self.shown_ids: list[int] = []

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.recognizer = sr.Recognizer()
        self.root.bind("<KeyPress>", self.key_up)

        self.chat_area.after(1000, self.fetch_messages)

    def init(self):
        self.root.mainloop()

    def key_up(self, key):

        if not key.char == ' ':
            logger.info(f'Ignoring key: {key}')
            return

        with sr.Microphone() as source:
            print('Speak now!')
            audio = self.recognizer.listen(source)

        print(f'Finished listening!')
        text = self.recognizer.recognize_google(audio, language='de-DE')
        print(text)
        self.send_queue.put(text)

    def fetch_messages(self):
        self.chat_handler.update()

        for message in self.chat_handler.chat:
            if message.id not in self.shown_ids:
                self.add_message_to_area(message)

        self.chat_area.after(1000, self.fetch_messages)

    def on_close(self):
        self.root.destroy()

    def add_message_to_area(self, message):
        print(f'Adding message: {message}')
        if message.id not in self.shown_ids:
            self.chat_area.configure(state='normal')
            if message.sender == 'Oma':
                self.chat_area.insert(tk.END, f"SIE: {message.message}\n", 'left')
            elif message.sender == 'Opa':
                self.chat_area.insert(tk.END, f"DU: {message.message}\n", 'right')
            else:
                raise ValueError(f'Unknown sender: {message.sender}')
            self.chat_area.configure(state='disabled')
            self.chat_area.see(tk.END)

            self.shown_ids.append(message.id)





if __name__ == '__main__':
    # logging.basicConfig(
    #     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    #     level=logging.INFO
    # )

    ChatApplication()