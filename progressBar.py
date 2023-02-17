import tkinter as tk
from tkinter import ttk


class ProgressBar:
    def __init__(self, master, max_value, message, size="400x75"):
        self.master = master
        self.max_value = max_value
        self.message = message

        self.top_level = tk.Toplevel(master)
        self.top_level.title("Installation Progress")
        self.top_level.geometry(size)
        self.top_level.protocol("WM_DELETE_WINDOW", self.disable_close_button)

        self.label = ttk.Label(self.top_level, text=self.message)
        self.label.pack(pady=10)

        self.progress = ttk.Progressbar(self.top_level, orient="horizontal", length=350, mode="determinate", maximum=self.max_value)
        self.progress.pack()

        self.top_level.grab_set()

    def disable_close_button(self):
        pass

    def update(self, current_value):
        self.progress["value"] = current_value
        self.progress.update()

    def destroy(self):
        self.top_level.destroy()
