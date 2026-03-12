# gui.py — Optional live dashboard for Astra using Tkinter

import tkinter as tk
from tkinter import scrolledtext

class AstraGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Astra Assistant Console")
        self.root.geometry("600x400")

        self.log_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Consolas", 11))
        self.log_area.pack(expand=True, fill="both")
        self.log_area.insert(tk.END, "🚀 Astra Assistant GUI Started\n")
        self.log_area.configure(state='disabled')

    def add_log(self, message):
        self.log_area.configure(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.configure(state='disabled')

    def start(self):
        self.root.mainloop()

# Example usage (optional):
# if __name__ == '__main__':
#     gui = AstraGUI()
#     gui.add_log("Ready.")
#     gui.start()
