import tkinter as tk
from tkinter import scrolledtext

class ChatApplication:

    def __init__(self):

        root = tk.Tk()
        root.title("Rede mit ihr")
        root.geometry("400x500")

        self.font = ("TkDefaultFont", 20)

        # Setup chat window
        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.chat_area.pack(pady=20, padx=20)
        self.chat_area.configure(state='disabled') 

        # Setup tags for left and right aligned messages
        self.chat_area.tag_configure('left', justify='left', background='lightblue', lmargin2=10, font=self.font)
        self.chat_area.tag_configure('right', justify='right', background='lightgreen', rmargin=10, font=self.font)

        # Send button
        send_button = tk.Button(root, text="Send", command=self.add_message)
        send_button.pack(pady=20)

        # Checking for new messages
        self.chat_area.after(5000, self.update_on_new_message)

        root.mainloop()

    def add_message(self):
        message = "Test message"

        print(f'Message: {message}')
        
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, f"DU: {message}\n", 'left')
        self.chat_area.insert(tk.END, f"SIE: {message}\n", 'right')
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)

    def update_on_new_message(self):
        print(f'Checking for a new message')
        return 



if __name__ == '__main__':
    ChatApplication()