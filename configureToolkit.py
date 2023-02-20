import logging
import os
import shutil
from GenericFunctions import GenericFunctions

class ConfigureToolkit:
    PLUGINS_DIR = ".plugins/com.ibm.etools.mft.broker.runtime"
    SETTINGS_DIR = "ToolkitSettings/org.eclipse.core.runtime"
    CVS_SETTINGS_FILE = "cvs_settings.xml"
    JDT_SETTINGS_FILE = "org.eclipse.jdt.core.prefs"
    MSSQL_DRIVER_SOURCE = "MS_SQL_DRIVER_SOURCE.zip"
    DEV_BROKER_FILE = "IntegrationNodes/{install_type}/DEV.broker"
    TEST_BROKER_FILE = "IntegrationNodes/{install_type}/TEST.broker"

    def __init__(self, install_type, iib_base_path, workspace_dir, node, user_id, log_file="configure_toolkit.log"):
        self.install_type = install_type
        self.iib_base_path = iib_base_path
        self.workspace_dir = workspace_dir
        self.node = node
        self.user_id = user_id
        self.log_file = log_file
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.metadata_dir = os.path.join(workspace_dir, ".metadata")
        self.plugins_dir = os.path.join(self.metadata_dir, self.PLUGINS_DIR)

        self.version_file = os.path.join(self.iib_base_path, "version.ini")
        self.lock_file = os.path.join(self.iib_base_path, ".lock")
        self.settings_dir = os.path.join(self.iib_base_path, self.SETTINGS_DIR)
        self.plugins_source_dir = os.path.join(self.settings_dir, "plugins")
        self.settings_source_dir = os.path.join(self.settings_dir, "org.eclipse.core.runtime")
        self.cvs_settings_file = os.path.join(self.settings_dir, self.CVS_SETTINGS_FILE)
        self.jdt_settings_file = os.path.join(self.settings_dir, self.JDT_SETTINGS_FILE)
        self.mssql_driver_source = os.path.join(self.settings_dir, self.MSSQL_DRIVER_SOURCE)
        self.mssql_driver_target = os.path.join(self.iib_base_path, "jdbc", "drivers", "Microsoft_SQL_Server")
        self.dev_broker_file = os.path.join(self.iib_base_path, self.DEV_BROKER_FILE.format(install_type=install_type))
        self.test_broker_file = os.path.join(self.iib_base_path, self.TEST_BROKER_FILE.format(install_type=install_type))

    def configure_toolkit(self):
        logging.basicConfig(filename=self.log_file)
        try:
            self.copy_files()
            self.replace_dev_broker()
            self.replace_test_broker()
            version = {"IIBTK_VERSION=": f"IIBTK_VERSION={self.get_iib_version()}"}
            GenericFunctions.replace_strings_in_file(self.version_file, version)
            self.logger.info("Finished configuring IIB Toolkit.")
        except Exception as e:
            self.logger.exception(f"Error configuring IIB Toolkit: {str(e)}")
            raise e
    def copy_files(self):
    try:
        source_target_list = [
            (self.version_file, f"{self.metadata_dir}/version.ini"),
            (self.lock_file, f"{self.metadata_dir}/.lock"),
            (self.cvs_settings_file, self.cvs_settings_file),
            (self.jdt_settings_file, self.jdt_settings_file),
            (self.mssql_driver_source, f"{self.mssql_driver_target}/MS_SQL_SERVER.zip"),
        ]
        for source, target in source_target_list:
            shutil.copy(source, target)
            self.logger.info(f"Copied {source} to {target}.")
        
        plugin_files = [f for f in os.listdir(self.plugins_source_dir) if os.path.isfile(os.path.join(self.plugins_source_dir, f))]
        for plugin_file in plugin_files:
            source = os.path.join(self.plugins_source_dir, plugin_file)
            target = os.path.join(self.plugins_dir, plugin_file)
            shutil.copy(source, target)
            self.logger.info(f"Copied {source} to {target}.")

        settings_files = [f for f in os.listdir(self.settings_source_dir) if os.path.isfile(os.path.join(self.settings_source_dir, f))]
        for settings_file in settings_files:
            source = os.path.join(self.settings_source_dir, settings_file)
            target = os.path.join(self.iib_base_path, "ToolkitSettings", "org.eclipse.core.runtime", settings_file)
            shutil.copy(source, target)
            self.logger.info(f"Copied {source} to {target}.")

        shutil.copy(self.dev_broker_file, self.plugins_dir)
        self.logger.info(f"Copied {self.dev_broker_file} to {self.plugins_dir}.")
        GenericFunctions.replace_strings_in_file(f"{self.plugins_dir}/DEV.broker", {
            "NODE": self.node,
            "LISTEN_PORT": str(self.WEBADMINPORT_SSL),
            "User": os.getenv("USER_ID")
        })
        self.logger.info("Replaced variables in DEV.broker.")

        shutil.copy(self.test_broker_file, self.plugins_dir)
        self.logger.info(f"Copied {self.test_broker_file} to {self.plugins_dir}.")
        GenericFunctions.replace_strings_in_file(f"{self.plugins_dir}/TEST.broker", {
            "User": os.getenv("USER_ID")
        })
        self.logger.info("Replaced variables in TEST.broker.")
    except Exception as e:
        self.logger.error(f"Failed to copy or replace files: {str(e)}")
        raise e
