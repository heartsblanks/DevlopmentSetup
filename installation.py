import logging
import os
import sys

from WorkspaceFunctions import WorkspaceUtils
from createVariables import CreateVariables
from checkConnections import CheckConnections
from PluginInstaller import PluginInstaller
from CheckOutProjects import CheckOutProjects
from configureToolkit import ToolkitConfigurator
from createProperties import CreateProperties
from progressBar import ProgressBar


class Installation:
    def __init__(self, install_type):
        self.install_type = install_type
        self.logger = logging.getLogger(__name__)
        self.progress_bar = ProgressBar(None, 7, "Installing")

    def run(self):
        try:
            self.progress_bar.top_level.deiconify()
            self.installation_steps()
            self.logger.info("Installation completed successfully!")
            self.progress_bar.destroy()
            sys.exit(0)
        except Exception as e:
            self.logger.error("Installation failed. See log for details.")
            self.logger.exception(str(e))
            self.progress_bar.destroy()
            sys.exit(1)

    def installation_steps(self):
        try:
            workspace = WorkspaceUtils(self.install_type)
            create_vars = CreateVariables(self.install_type)
            check_conns = CheckConnections(create_vars)
            plugin_installer = PluginInstaller(self.install_type, create_vars, check_conns)
            checkout_projects = CheckOutProjects(self.install_type, create_vars, check_conns)
            toolkit_config = ToolkitConfigurator(self.install_type, create_vars, check_conns)
            create_props = CreateProperties(self.install_type)

            workspace.check_workspace_directory()
            self.progress_bar.update(1)
            create_vars.create()
            self.progress_bar.update(2)
            check_conns.check_all_connections()
            self.progress_bar.update(3)
            plugin_installer.install_plugins()
            self.progress_bar.update(4)
            checkout_projects.checkout_all_projects()
            self.progress_bar.update(5)
            toolkit_config.configure_toolkit()
            self.progress_bar.update(6)
            create_props.create()
            self.progress_bar.update(7)
        except Exception as e:
            self.logger.exception("Error during installation steps")
            raise e
