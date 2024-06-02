import tkinter as tk
from tkinter import StringVar
import json

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My App")
        self.geometry("400x300")

        self.validate_command = (self.register(self.get_command), "%P")
        
        self.init_ui()
        self.load_data()

    def load_data(self):
        self.data = open("./codes.json", "r", encoding="utf-8")
        self.data = json.load(self.data)

    def get_command(self, inp):
        inp = self.entry.get()
        if inp:
            if inp in self.data:
                self.label.config(text=self.data[inp])
        
    def init_ui(self):
        self.entry = tk.Entry(self, 
                              validatecommand=self.validate_command, validate="key")
        self.entry.pack(pady=10)
        
        self.label = tk.Label(self, text="Hello, World!")
        self.label.pack(pady=10)
        

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()