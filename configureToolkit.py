import logging
import os
import shutil
from GenericFunctions import GenericFunctions

class ConfigureToolkit:
    def __init__(self, install_type, iib_base_path, workspace_dir, node, user_id, log_file="configure_toolkit.log"):
        self.install_type = install_type
        self.iib_base_path = iib_base_path
        self.workspace_dir = workspace_dir
        self.node = node
        self.user_id = user_id
        self.log_file = log_file
        self.logger = logging.getLogger(__name__)
        
        self.metadata_dir = os.path.join(workspace_dir, ".metadata")
        self.plugins_dir = os.path.join(self.metadata_dir, ".plugins", "com.ibm.etools.mft.broker.runtime")
        
        self.version_file = os.path.join(self.iib_base_path, "version.ini")
        self.lock_file = os.path.join(self.iib_base_path, ".lock")
        self.settings_dir = os.path.join(self.iib_base_path, "ToolkitSettings")
        self.plugins_source_dir = os.path.join(self.settings_dir, "plugins")
        self.settings_source_dir = os.path.join(self.settings_dir, "org.eclipse.core.runtime")
        self.cvs_settings_file = os.path.join(self.settings_dir, "cvs_settings.xml")
        self.jdt_settings_file = os.path.join(self.settings_dir, "org.eclipse.jdt.core.prefs")
        self.mssql_driver_source = os.path.join(self.settings_dir, "MS_SQL_DRIVER_SOURCE.zip")
        self.mssql_driver_target = os.path.join(self.iib_base_path, "jdbc", "drivers", "Microsoft_SQL_Server")
        self.dev_broker_file = os.path.join(self.iib_base_path, "IntegrationNodes", install_type, "DEV.broker")
        self.test_broker_file = os.path.join(self.iib_base_path, "IntegrationNodes", install_type, "TEST.broker")

    def configure_toolkit(self):
        logging.basicConfig(filename=self.log_file, level=logging.DEBUG)
        self.copy_files()
        self.replace_dev_broker()
        self.replace_test_broker()
        GenericFunctions.replace_strings_in_file(self.version_file, {"IIBTK_VERSION=": f"IIBTK_VERSION={self.get_iib_version()}"})
        self.logger.info("Finished configuring IIB Toolkit.")
    
    def copy_files(self):
        source_target_list = [
            (self.version_file, os.path.join(self.metadata_dir, "version.ini")),
            (self.lock_file, os.path.join(self.metadata_dir, ".lock")),
            (self.cvs_settings_file, self.cvs_settings_file),
            (self.jdt_settings_file, self.jdt_settings_file),
            (self.mssql_driver_source, self.mssql_driver_target),
        ]
        for source, target in source_target_list:
            shutil.copy(source, target)
            self.logger.info(f"Copied {source} to {target}.")
        
        for plugin_file in os.listdir(self.plugins_source_dir):
            source = os.path.join(self.plugins_source_dir, plugin_file)
            target = os.path.join(self.plugins_dir, plugin_file)
            shutil.copy(source, target)
            self.logger.info(f"Copied {source} to {target}.")
    
        for settings_file in os.listdir(self.settings_source_dir):
            source = os.path.join(self.settings_source_dir, settings_file)
            target = os.path.join(self.iib_base_path, "ToolkitSettings", "org.eclipse.core.runtime", settings_file)
            shutil.copy(source, target)
            self.logger.info(f"Copied {source} to {target}.")
    
        shutil.copy(self.dev_broker_file, self.plugins_dir)
        self.logger.info(f"Copied {self.dev_broker_file} to {self.plugins_dir}.")
        GenericFunctions.replace_strings_in_file(self.plugins_dir + "/DEV.broker", {
        "NODE": self.node,
        "LISTEN_PORT": str(self.WEBADMINPORT_SSL),
        "User": os.getenv("USER_ID")
        })
        self.logger.info("Replaced variables in DEV.broker.")

        shutil.copy(self.test_broker_file, self.plugins_dir)
        self.logger.info(f"Copied {self.test_broker_file} to {self.plugins_dir}.")
        GenericFunctions.replace_strings_in_file(self.plugins_dir + "/TEST.broker", {
        "User": os.getenv("USER_ID")
    })
    self.logger.info("Replaced variables in TEST.broker.")

