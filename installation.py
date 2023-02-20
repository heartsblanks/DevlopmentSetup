import logging
from tkinter import messagebox
from CheckOutProjects import CheckOutProjects
from PluginInstaller import PluginInstaller
from CheckConnections import CheckConnections
from CreateVariables import CreateVariables


class Installation:
    def __init__(self, system_type, install_type):
        self.system_type = system_type
        self.install_type = install_type
        self.logger = logging.getLogger(__name__)
        self.checkout_projects = CheckOutProjects(self.install_type, self.logger)
        self.plugin_installer = PluginInstaller(self.install_type, self.logger)
        self.check_connections = CheckConnections(self.logger)
        self.create_variables = CreateVariables(self.system_type)
        self.orchestrate_installation()

    def orchestrate_installation(self):
        try:
            self.checkout_projects.run()
            self.plugin_installer.run()
            self.check_connections.run()
            self.create_variables.create()
            messagebox.showinfo("Installation Complete", f"{self.install_type} installation complete.")
            self.logger.info(f"{self.install_type} installation complete.")
        except Exception as e:
            self.logger.exception("An error occurred during installation")
            messagebox.showerror("Installation Error", f"An error occurred during {self.install_type} installation. Error message: {str(e)}")
