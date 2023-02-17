import tkinter as tk
from tkinter import ttk

class ProgressBar:
    def __init__(self, master, title, progress_title, progress_var):
        self.master = master
        self.title = title
        self.progress_title = progress_title
        self.progress_var = progress_var

        self.create_window()

    def create_window(self):
        # Create window
        self.window = tk.Toplevel(self.master)
        self.window.title(self.title)
        self.window.geometry("300x100")

        # Create progress bar
        self.progress_label = ttk.Label(self.window, text=self.progress_title)
        self.progress_bar = ttk.Progressbar(self.window, variable=self.progress_var, maximum=100)
        self.progress_label.pack(pady=10)
        self.progress_bar.pack(pady=5)

    def start(self):
        self.window.grab_set()
        self.progress_var.set(0)

    def update(self, progress):
        self.progress_var.set(progress)
        self.window.update()

    def end(self):
        self.progress_var.set(100)
        self.window.after(500, self.window.destroy)
