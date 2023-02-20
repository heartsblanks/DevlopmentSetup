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
        # Create new top level window
        self.system_setup_options_window = tk.Toplevel(self.master)
        self.system_setup_options_window.title(f"{system_type} {install_type} Setup")

        # Set up custom styles for this window
        self.setup_system_setup_options_styles()

        # Create labels and options
        self.installation_type_var = self.create_label_and_options("Unattended installation", ["Yes", "No"])
        self.repo_update_var = self.create_label_and_options("Repository", ["Update", "Replace"])
        self.hb_password_entry = self.create_label_and_entry("HB Password")
        if install_type in ["IIB10", "ACE12"]:
            self.ho_password_entry = self.create_label_and_entry("HO Password")
            self.auto_reboot_var = self.create_label_and_options("Reboot Automatically", ["Yes", "No"])

        # Create submit button
        submit_button = ttk.Button(self.system_setup_options_window, text="Submit", command=lambda: self.submit_options, style="SubmitButton.TButton")
        submit_button.pack(pady=10)

        # Create quit button
        quit_button = ttk.Button(self.system_setup_options_window, text="Quit", command=self.system_setup_options_window.destroy, style="QuitButton.TButton")
        quit_button.pack(pady=10)
        self.system_options_window.destroy()

    def setup_system_setup_options_styles(self):
        self.system_setup_options_window.option_add("*Button.Background", "#4d4d4d")
        self.system_setup_options_window.option_add("*Button.Foreground", "white")
        self.system_setup_options_window.option_add("*Button.activeBackground", "#808080")
        self.system_setup_options_window.option_add("*Button.activeForeground", "white")
        self.system_setup_options_window.option_add("*Button.highlightThickness", 0)
        self.system_setup_options_window.option_add("*Label.Background", "#d9d9d9")
        self.system_setup_options_window.option_add("*Label.Foreground", "#4d4d4d")

    def create_label_and_options(self, label_text, option_values):
        label = ttk.Label(self.system_setup_options_window, text=label_text, style="OptionLabel.TLabel")
        label.pack(pady=5)
        var = tk.StringVar(value=option_values[0])
        for option_value in option_values:
            radio = ttk.Radiobutton(self.system_setup_options_window, text=option_value, variable=var, value=option_value, style="Option.TRadiobutton")
            radio.pack()
        return var

    def create_label_and_entry(self, label_text):
        label = ttk.Label(self.system_setup_options_window, text=label_text, style="OptionLabel.TLabel")
        label.pack(pady=5)
        entry = ttk.Entry(self.system_setup_options_window, show="*", style="Option.TEntry")
        entry.pack()
        return entry

    def submit_options(self):
        # get the values of the options
        installation_type = self.installation_type_var.get()
        repo_update = self.repo_update_var.get()
        hb_password = self.hb_password_entry.get()

        if self.install_type in ["IIB10", "ACE12"]:
            ho_password = self.ho_password_entry.get()
            auto_reboot = self.auto_reboot_var.get()
        else:
            ho_password = None
            auto_reboot = None

        # instantiate the Installation class
        installation = Installation(self.system_type, self.install_type, self.options['systemPath'])

