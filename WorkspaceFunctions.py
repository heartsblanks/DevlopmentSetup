import os
import tkinter as tk
import logging
from tkinter import messagebox


class WorkspaceUtils:
    LOG_FILE = "install_orchestration.log"

    def __init__(self, install_type):
        self.install_type = install_type
        self.workspace_path = None
        self.logger = logging.getLogger(__name__)

    def check_workspace_directory(self):
        try:
            logging.basicConfig(filename=self.LOG_FILE, filemode='a', level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
            version_file_path = f"C:/Workspaces/{self.install_type}/.metadata/version.ini"
            if not os.path.exists(version_file_path):
                self.workspace_options_window = tk.Toplevel()
                self.workspace_options_window.title(f"{self.install_type} Workspace")

                # Create label
                label = tk.Label(self.workspace_options_window, text="Workspace has not been detected. Do you want to create a new workspace within the standard directory?")
                label.pack(pady=5)

                # Create yes button
                yes_button = tk.Button(self.workspace_options_window, text="Yes", command=lambda: self.create_new_workspace())
                yes_button.pack(pady=10)

                # Create no button
                no_button = tk.Button(self.workspace_options_window, text="No", command=lambda: self.get_custom_workspace())
                no_button.pack(pady=10)
            else:
                self.logger.info(f"{self.install_type} workspace has been detected.")
        except Exception as e:
            self.logger.exception(f"Error checking workspace directory: {e}")
            raise e

    def create_new_workspace(self):
        try:
            workspace_path = f"C:/Workspaces/{self.install_type}"
            os.makedirs(workspace_path, exist_ok=True)
            version_file_path = f"{workspace_path}/.metadata/version.ini"
            if not os.path.exists(version_file_path):
                messagebox.showerror("Error", f"Failed to create new workspace for {self.install_type}")
                self.logger.error(f"Failed to create new workspace for {self.install_type}")
                return

            self.workspace_options_window.destroy()
            self.workspace_path = workspace_path
            self.logger.info(f"{self.install_type} workspace has been created at {self.workspace_path}.")
        except Exception as e:
            self.logger.exception(f"Error creating new workspace: {e}")
            raise e

    def get_custom_workspace(self):
        try:
            # Create new top level window
            custom_workspace_window = tk.Toplevel()
            custom_workspace_window.title("Custom Workspace Location")

            # Create label and entry
            label = tk.Label(custom_workspace_window, text=f"Enter the location of the {self.install_type} workspace:")
            label.pack(pady=5)
            entry = tk.Entry(custom_workspace_window)
            entry.pack()

            # Create submit button
            submit_button = tk.Button(custom_workspace_window, text="Submit", command=lambda: self.check_custom_workspace(custom_workspace_window, entry.get()))
            submit_button.pack(pady=10)

            # Create quit button
            quit_button = tk.Button(custom_workspace_window, text="Quit", command=custom_workspace_window.destroy)
            quit_button.pack(pady=10)
        except Exception as e:
            self.logger.exception(f"Error getting custom workspace: {e}")
            raise e
    def check_custom_workspace(self, custom_workspace_window, workspace_path):
        try:
            if os.path.exists(os.path.join(workspace_path, self.install_type, ".metadata", "version.ini")):
                self.workspace_path = workspace_path
                custom_workspace_window.destroy()
                self.logger.info(f"{self.install_type} workspace has been set to {self.workspace_path}.")
            else:
                messagebox.showerror("Error", f"{self.install_type} workspace not found at the provided location.")
                self.logger.error(f"{self.install_type} workspace not found at {workspace_path}.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while setting {self.install_type} workspace: {str(e)}")
            self.logger.exception(f"An error occurred while setting {self.install_type} workspace: {str(e)}")
            raise e
