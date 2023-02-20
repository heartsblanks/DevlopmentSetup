import tkinter as tk
from tkinter import ttk
import logging
from passwordUpdate import PasswordUpdate
from systemSetupOptions import SystemSetupOptions

# Set up logging
logging.basicConfig(filename='install_orchestration.log', level=logging.ERROR)

class InstallOrchestrationGUI:
    def __init__(self, master):
        self.master = master
        master.title("Install Orchestration")

        # Create EAI button
        self.create_system_button("EAI", ["IIB10", "ACE12"])

        # Create ETL button
        self.create_system_button("ETL", ["DS"])

    def create_system_button(self, system_name, options):
        try:
            # Create button
            button = ttk.Button(self.master, text=system_name, command=lambda: self.displaySystemOptions(system_name, options), style="SystemButton.TButton")
            button.pack(fill="x", padx=10, pady=10)
        except Exception as e:
            logging.error(f"An error occurred while creating the {system_name} button: {e}")

    def displaySystemOptions(self, system_type, options):
        try:
            # Create new top level window
            self.system_options_window = tk.Toplevel(self.master)
            self.system_options_window.title(f"{system_type} Options")

            # Set up custom styles for this window
            self.setup_system_options_styles()

            # Create buttons
            for option in options:
                button = ttk.Button(self.system_options_window, text=option, command=lambda option=option: self.displaySystemSetupOptions(system_type, option), style="SystemButton.TButton")
                button.pack(fill="x", padx=10, pady=5)

            # Create Password update button
            password_update_button = ttk.Button(self.system_options_window, text="Password update", command=self.passwordUpdate, style="SystemButton.TButton")
            password_update_button.pack(fill="x", padx=10, pady=5)
        except Exception as e:
            logging.error(f"An error occurred while displaying the {system_type} options: {e}")

    def setup_system_options_styles(self):
        try:
            self.system_options_window.option_add("*Button.Background", "#4d4d4d")
            self.system_options_window.option_add("*Button.Foreground", "white")
            self.system_options_window.option_add("*Button.activeBackground", "#808080")
            self.system_options_window.option_add("*Button.activeForeground", "white")
            self.system_options_window.option_add("*Button.highlightThickness", 0)
            self.system_options_window.option_add("*Label.Background", "#d9d9d9")
            self.system_options_window.option_add("*Label.Foreground", "#4d4d4d")
        except Exception as e:
            logging.error(f"An error occurred while setting up the {self.system_options_window.title()} window styles: {e}")

    def passwordUpdate(self):
        try:
            password_updater = PasswordUpdate(self.master, self.system_options_window)
            password_updater.create_window()
        except Exception as e:
            logging.error(f"An error occurred while displaying the password update window: {e}")

    def displaySystemSetupOptions(self, system_type, install_type):
        try:
            system_setup_options = SystemSetupOptions(self.master, self.system_options_window, system_type, install_type)
            system_setup_options.create_window()
        except Exception as e:
            logging.error(f"An error occurred while displaying the {system_type} {install_type} setup options: {e}")
