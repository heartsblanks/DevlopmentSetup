import os
import shutil
import logging
from zipfile import ZipFile
from GenericFunctions import replace_strings_in_file

class ConfigureToolkit:
    def __init__(self, workspace_dir, toolkit_plugins_dir, toolkit_settings_dir, cvs_settings_file, jdt_settings_file):
        self.WORKSPACE_DIR = workspace_dir
        self.TOOLKIT_PLUGINS_DIR = toolkit_plugins_dir
        self.TOOLKIT_SETTINGS_DIR = toolkit_settings_dir
        self.CVS_SETTINGS_FILE = cvs_settings_file
        self.JDT_SETTINGS_FILE = jdt_settings_file
        self.logger = logging.getLogger(__name__)

    def configure(self, iib_basepath):
        try:
            # Update eclipse.ini to increase java heap size
            eclipse_ini_file = os.path.join(iib_basepath, "tools", "eclipse.ini")
            replace_strings_in_file(eclipse_ini_file, {"-Xmx1024m": "-Xmx4096m"})
            self.logger.info(f"Updated {eclipse_ini_file} to increase java heap size.")

            # Copy files from metadata and plugins directories
            metadata_dir = os.path.join(iib_basepath, "tools", "eclipse", "plugins", "com.ibm.etools.msgbroker.toolkit_")
            version_file = os.path.join(metadata_dir, "version.ini")
            lock_file = os.path.join(metadata_dir, ".lock")
            shutil.copy(version_file, os.path.join(self.WORKSPACE_DIR, ".metadata"))
            shutil.copy(lock_file, os.path.join(self.WORKSPACE_DIR, ".metadata"))
            self.logger.info(f"Copied {version_file} and {lock_file} to {self.WORKSPACE_DIR}/.metadata")
            
            plugins_dir = os.path.join(iib_basepath, "tools", "eclipse", "plugins")
            shutil.copytree(os.path.join(plugins_dir, "com.ibm.etools.msgbroker.toolkit_"), self.TOOLKIT_PLUGINS_DIR)
            self.logger.info(f"Copied files from {plugins_dir}/com.ibm.etools.msgbroker.toolkit_ to {self.TOOLKIT_PLUGINS_DIR}")
            
            settings_dir = os.path.join(iib_basepath, "tools", "eclipse", "configuration", "org.eclipse.core.runtime")
            shutil.copytree(settings_dir, self.TOOLKIT_SETTINGS_DIR)
            self.logger.info(f"Copied files from {settings_dir} to {self.TOOLKIT_SETTINGS_DIR}")
            
            # Update CVS and JDT settings files
            replace_strings_in_file(self.CVS_SETTINGS_FILE, {"RPL_USERID": os.environ["USERNAME"]})
            self.logger.info(f"Updated {self.CVS_SETTINGS_FILE} with USERNAME environment variable.")
            
            replace_strings_in_file(self.JDT_SETTINGS_FILE, {"RPL_VERSIONNO": os.environ["IIBTK_VERSION"]})
            self.logger.info(f"Updated {self.JDT_SETTINGS_FILE} with IIBTK_VERSION environment variable.")
            
            # Extract MS SQL driver
            driver_source = "MS_SQL_DRIVER_SOURCE.zip"
            driver_target = "MS_SQL_DRIVER_TARGET"
            with ZipFile(driver_source, 'r') as zipObj:
                zipObj.extractall(driver_target)
            self.logger.info(f"Extracted MS SQL driver from {driver_source} to {driver_target}.")
            
        except Exception as e:
            self.logger.exception(f"Error while configuring toolkit: {str(e)}")
            raise e
