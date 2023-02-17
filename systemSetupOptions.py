import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import logging


class SystemSetupOptions:
    def __init__(self, master, system_options_window, system_type, install_type):
        self.master = master
        self.system_options_window = system_options_window
        self.system_type = system_type
        self.install_type = install_type
        self.logger = logging.getLogger(__name__)

    def create_window(self):
        self.system_options_window.withdraw()

        # Create new top level window
        self.setup_options_window = tk.Toplevel(self.master)
        self.setup_options_window.title(f"{self.install_type} Setup Options")

        # Create submit button
        submit_button = ttk.Button(self.setup_options_window, text="Submit", command=self.submit_options, style="SystemButton.TButton")
        submit_button.pack(pady=10)

        # Create quit button
        quit_button = ttk.Button(self.setup_options_window, text="Quit", command=self.quit_options, style="SystemButton.TButton")
        quit_button.pack(pady=10)

        # Create options
        self.create_options()

    def create_options(self):
        self.options = {}
        try:
            with open(f"config/{self.system_type}_{self.install_type}.txt", "r") as f:
                for line in f:
                    key, value = line.split("=")
                    self.options[key.strip()] = value.strip()
        except FileNotFoundError:
            self.logger.warning(f"No configuration file found for {self.system_type} - {self.install_type}.")

        for key, value in self.options.items():
            label = ttk.Label(self.setup_options_window, text=key, font="Helvetica 10 bold")
            label.pack(pady=5)

            entry = ttk.Entry(self.setup_options_window)
            entry.insert(0, value)
            entry.pack(pady=5)

            browse_button = ttk.Button(self.setup_options_window, text="Browse", command=lambda entry=entry: self.browse_for_file(entry))
            browse_button.pack(pady=5)

    def browse_for_file(self, entry):
        file_path = filedialog.askopenfilename()
        entry.delete(0, "end")
        entry.insert(0, file_path)

    def quit_options(self):
        self.setup_options_window.destroy()
        self.system_options_window.deiconify()

    def submit_options(self):
        for key, value in self.options.items():
            if key in ["keystore", "truststore"]:
                if not os.path.exists(self.options[key]):
                    self.logger.warning(f"{self.options[key]} not found for {self.install_type}.")
            elif key == "sslProfile" and value != "":
                if not os.path.exists(self.options[key]):
                    self.logger.warning(f"{self.options[key]} not found for {self.install_type}.")
            self.options[key] = self.setup_options_window.children[key + "!entry"].get()

        with open(f"config/{self.system_type}_{self.install_type}.txt", "w") as f:
            for key, value in self.options.items():
                f.write(f"{key}={value}\n")

        self.setup_options_window.destroy()
        self.system_options_window.deiconify()
