import os
import shutil
import urllib.request
import zipfile
import logging
from GenericFunctions import replace_strings_in_file


# Local file paths for plugin installation
IIB_TOOLKIT_PLUGIN_PATH = r"C:\temp\iib_toolkit_plugin.zip"
ACE_TOOLKIT_PLUGIN_PATH = r"C:\temp\ace_toolkit_plugin.zip"
MAVEN_CLI_URL = r"https://repo1.maven.org/maven2/com/github/eirslett/maven-frontend-plugin/1.10.0/maven-frontend-plugin-1.10.0.jar"
MAVEN_CLI_PATH = r"C:\apache-maven-3.8.1-bin.zip"
ECLIPSE_PLUGIN_URL = "https://download.eclipse.org/releases/latest"

logger = logging.getLogger(__name__)

class PluginInstaller:
    def __init__(self, system_type):
        self.system_type = system_type

    def install_iib_toolkit_plugin(self):
        if self.system_type == "EAI":
            self.install_plugin_from_zip(IIB_TOOLKIT_PLUGIN_PATH, "IIB Toolkit")

    def install_ace_toolkit_plugin(self):
        if self.system_type == "EAI":
            self.install_plugin_from_zip(ACE_TOOLKIT_PLUGIN_PATH, "ACE Toolkit")

    def install_eclipse_plugin(self):
        eclipse_path = os.environ.get("ECLIPSE_HOME")
        if not eclipse_path:
            logger.error("ECLIPSE_HOME environment variable not set.")
            return
        try:
            urllib.request.urlretrieve(ECLIPSE_PLUGIN_URL, os.path.join(eclipse_path, "eclipse", "plugins", "latest"))
        except:
            logger.exception("Failed to install Eclipse plugin.")

    def install_maven_cli(self):
        try:
            urllib.request.urlretrieve(MAVEN_CLI_URL, MAVEN_CLI_PATH)
            with zipfile.ZipFile(MAVEN_CLI_PATH, "r") as zip_ref:
                zip_ref.extractall("C:\\")
            os.environ["MAVEN_HOME"] = "C:\\apache-maven-3.8.1"
            os.environ["PATH"] = f"{os.environ['MAVEN_HOME']}\\bin;{os.environ['PATH']}"
        except:
            logger.exception("Failed to install Maven CLI.")

    def install_jre(self):
        java_home = os.environ.get("JAVA_HOME")
        if not java_home:
            logger.error("JAVA_HOME environment variable not set.")
            return
        try:
            subprocess.run([os.path.join(java_home, "bin", "java"), "-version"])
        except:
            logger.exception("Failed to install JRE.")

    def install_maven_plugin(self):
        # Create directories for M2_DIR and M2_USERDIR
        try:
            m2_dir = os.environ["M2_DIR"]
            m2_user_dir = os.environ["M2_USERDIR"]
            os.makedirs(m2_dir, exist_ok=True)
            os.makedirs(m2_user_dir, exist_ok=True)
        except Exception as e:
            logger.exception("Failed to create directories for M2_DIR and M2_USERDIR.")
            raise e

        # Copy files to M2_DIR and M2_USERDIR
        try:
            # Copy settings.xml and settings-security.xml from Maven Plugin directory to M2_DIR
            src_dir = os.path.join(os.getcwd(), "MavenPlugin")
            dst_dir = m2_dir
            shutil.copy(os.path.join(src_dir, "settings.xml"), dst_dir)
            shutil.copy(os.path.join(src_dir, "settings-security.xml"), dst_dir)

            # Copy settings-security.xml from Maven Plugin/Security Relocation directory to M2_USERDIR
            src_dir = os.path.join(src_dir, "Security Relocation")
            dst_dir = m2_user_dir
            shutil.copy(os.path.join(src_dir, "settings-security.xml"), dst_dir)
        except Exception as e:
            logger.exception("Failed to copy files to M2_DIR and M2_USERDIR.")
            raise e

        # Replace strings in files
        try:
            settings_xml_file = os.path.join(m2_dir, "settings.xml")
            settings_security_xml_file = os.path.join(m2_dir, "settings-security.xml")
            values_to_replace = {"<localRepository>${M2_REPO}</localRepository>": f"<localRepository>{os.environ['M2_REPO']}</localRepository>"}
            replace_strings_in_file(settings_xml_file, values_to_replace)
            logger.info(f"Replaced values in {settings_xml_file}: {values_to_replace}")

            values_to_replace = {"<master>{*AES*}REPLACEME{*AES*}</master>": f"<master>{os.environ['NEXUS_USER_PASS']}</master>"}
            replace_strings_in_file(settings_security_xml_file, values_to_replace)
            logger.info(f"Replaced values in {settings_security_xml_file}: {values_to_replace}")
        except Exception as e:
            logger.exception("Failed to replace strings in settings.xml and settings-security.xml.")
            raise e


    def install_plugin_from_zip(self, plugin_path, plugin_name):
        plugin_dir = os.environ.get("ECLIPSE_HOME")
        if not plugin_dir:
            logger.error("ECLIPSE_HOME environment variable not set.")
            return
        try:
            with zipfile.ZipFile(plugin_path, "r") as zip_ref:
                zip_ref.extractall(plugin_dir)
        except:
            logger.exception(f"Failed to install {plugin_name} plugin from zip.")
