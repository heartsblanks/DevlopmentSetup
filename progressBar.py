import tkinter as tk
from tkinter import ttk


class ProgressBar:
    def __init__(self, master, max_value):
        self.master = master
        self.progress_bar = None
        self.max_value = max_value

    def create_progress_bar(self):
        self.progress_bar = ttk.Progressbar(self.master, orient="horizontal", length=400, mode="determinate", maximum=self.max_value)
        self.progress_bar.pack(pady=10)

    def update_progress_bar(self, value):
        self.progress_bar["value"] = value
        self.master.update_idletasks()
