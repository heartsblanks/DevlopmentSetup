import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import hashlib
import logging

class PasswordUpdate:
    def __init__(self, master, system_options_window):
        self.master = master
        self.system_options_window = system_options_window

        # Create top level window for password update
        self.password_update_window = tk.Toplevel(self.master)
        self.password_update_window.title("Password Update")

        # Create and set custom styles for this window
        self.setup_password_update_styles()

        # Create password update form
        self.create_password_update_form()

    def setup_password_update_styles(self):
        self.password_update_window.option_add("*Label.Background", "#d9d9d9")
        self.password_update_window.option_add("*Label.Foreground", "#4d4d4d")
        self.password_update_window.option_add("*Entry.Background", "white")
        self.password_update_window.option_add("*Entry.Foreground", "#4d4d4d")
        self.password_update_window.option_add("*Entry.BorderWidth", 2)
        self.password_update_window.option_add("*Entry.Relief", "groove")
        self.password_update_window.option_add("*Button.Background", "#4d4d4d")
        self.password_update_window.option_add("*Button.Foreground", "white")
        self.password_update_window.option_add("*Button.activeBackground", "#808080")
        self.password_update_window.option_add("*Button.activeForeground", "white")
        self.password_update_window.option_add("*Button.highlightThickness", 0)

    def create_password_update_form(self):
        # Create HB Password form
        hb_password_label = ttk.Label(self.password_update_window, text="HB Password:")
        hb_password_label.pack(padx=10, pady=10)
        self.hb_password_entry = ttk.Entry(self.password_update_window, show="*")
        self.hb_password_entry.pack(padx=10, pady=5)

        # Create HO Password form
        ho_password_label = ttk.Label(self.password_update_window, text="HO Password:")
        ho_password_label.pack(padx=10, pady=10)
        self.ho_password_entry = ttk.Entry(self.password_update_window, show="*")
        self.ho_password_entry.pack(padx=10, pady=5)

        # Create update password button
        update_password_button = ttk.Button(self.password_update_window, text="Update Passwords", command=self.update_passwords)
        update_password_button.pack(padx=10, pady=10)

    def create_window(self):
        self.password_update_window.grab_set()
        self.password_update_window.transient(self.system_options_window)
        self.master.wait_window(self.password_update_window)

    def update_passwords(self):
        hb_password = self.hb_password_entry.get()
        ho_password = self.ho_password_entry.get()

        # Hash passwords
        hb_password_hash = hashlib.sha256(hb_password.encode()).hexdigest()
        ho_password_hash = hashlib.sha256(ho_password.encode()).hexdigest()

        # Update passwords
        try:
            logging.info("Updating passwords")
            # Code to update passwords goes here
        except Exception as e:
            logging.exception(f"Error updating passwords: {str(e)}")
            messagebox.showerror("Password Update", f"Error updating passwords: {str(e)}")
            return

        # Show success message
        messagebox.showinfo("Password Update", "Passwords updated successfully.")
        self.password_update_window.destroy()
