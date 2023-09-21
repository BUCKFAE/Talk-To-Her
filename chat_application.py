import tkinter as tk
from tkinter import scrolledtext
import subprocess

from chat_handler import ChatHandler

import speech_recognition as sr




class ChatApplication:

    def __init__(self, send_queue, recieve_queue):

        super().__init__()
        self.send_queue = send_queue
        self.recieve_queue = recieve_queue
        self.root = tk.Tk()
        self.root.title("Rede mit ihr")
        self.root.geometry("400x500")

        self.font = ("TkDefaultFont", 20)

        # Setup chat window
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.chat_area.pack(pady=20, padx=20)
        self.chat_area.configure(state='disabled') 

        # Setup tags for left and right aligned messages
        self.chat_area.tag_configure('left', justify='left', background='lightblue', lmargin2=10, font=self.font)
        self.chat_area.tag_configure('right', justify='right', background='lightgreen', rmargin=10, font=self.font)

        # Send button
        send_button = tk.Button(self.root, text="Send", command=self.send_message)
        send_button.pack(pady=20)

        self.chat_handler = ChatHandler()
        self.shown_ids: list[int] = []

        #self.communicator = subprocess.Popen(['python', 'message_receiver.py'])
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.chat_area.after(1000, self.fetch_messages)

    def init(self):
        self.root.mainloop()
        

    def fetch_messages(self):
        self.chat_handler.update()

        for message in self.chat_handler.chat:
            if message.id not in self.shown_ids:
                self.add_message_to_area(message)

        self.chat_area.after(1000, self.fetch_messages)

    def on_close(self):
        #self.communicator.kill()
        self.root.destroy()

    def send_message(self):
        # Initialize recognizer
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('Speak now!')
            audio = r.listen(source)

        print(f'Finished listening!')
        text = r.recognize_google(audio, language='de-DE')
        print(text)
        self.send_queue.put(text)


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