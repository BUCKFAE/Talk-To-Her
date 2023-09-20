import logging
import tkinter as tk
from tkinter import scrolledtext
from queue import Queue



class ChatApplication:

    def __init__(self, queue: Queue):

        super().__init__()
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

        self.queue = queue

    def run(self):
        self.check_queue()
        self.root.mainloop()

    def check_queue(self):
        while not self.queue.empty():
            message, sender = self.queue.get()
            print('New stuff')
            # self.add_message(message, sender)
        # Check the queue again in 100ms
        self.root.after(100, self.check_queue)

    def send_message(self):
        message = "Test message"

        logging.info(f'Message: {message}')
        
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, f"DU: {message}\n", 'left')
        self.chat_area.insert(tk.END, f"SIE: {message}\n", 'right')
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)




if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    ChatApplication()