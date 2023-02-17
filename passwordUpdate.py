import tkinter as tk
from tkinter import ttk
import logging


class PasswordUpdate:
    def __init__(self, root, parent):
        self.root = root
        self.parent = parent
        self.logger = logging.getLogger(__name__)

    def create_window(self):
        self.password_update_window = tk.Toplevel(self.root)
        self.password_update_window.title("Password Update")

        # Create username and password labels
        self.username_label = ttk.Label(self.password_update_window, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")
        self.password_label = ttk.Label(self.password_update_window, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")

        # Create username and password entry fields
        self.username_entry = ttk.Entry(self.password_update_window, width=30)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.password_entry = ttk.Entry(self.password_update_window, width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Create update button
        self.update_button = ttk.Button(self.password_update_window, text="Update Password", command=self.update_password)
        self.update_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def update_password(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.logger.info(f"Username and password updated: {username} / {password}")
        self.password_update_window.destroy()
        self.parent.destroy()
