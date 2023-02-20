import os
import shutil
import urllib.request
import zipfile
import logging

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
        try:
            urllib.request.urlretrieve(MAVEN_CLI_URL, "maven-frontend-plugin.jar")
            shutil.move("maven-frontend-plugin.jar", os.path.join(os.environ["MAVEN_HOME"], "lib", "ext"))
        except:
            logger.exception("Failed to install Maven plugin.")

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
