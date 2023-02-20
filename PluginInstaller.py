import os
import shutil
import logging
from GenericFunctions import GenericFunctions

class PluginInstaller:
    def __init__(self, iib_version, maven_version, maven_dir, ace_install_dir, m2_dir):
        self.iib_version = iib_version
        self.maven_version = maven_version
        self.maven_dir = maven_dir
        self.ace_install_dir = ace_install_dir
        self.m2_dir = m2_dir
        self.logger = logging.getLogger(__name__)

    def install_eclipse_plugin(self, repository, package, directory):
        command = f"{directory}\\eclipsec.exe -nosplash -application org.eclipse.equinox.p2.director -repository {repository} -installIU {package}"
        self.logger.info(f"Running command: {command}")
        try:
            os.system(command)
            self.logger.info(f"Finished installing Eclipse plugin {package}.")
        except Exception as e:
            self.logger.error(f"Error installing Eclipse plugin {package}: {str(e)}")
            raise e

    def install_maven_plugin(self):
        logger = logging.getLogger(__name__)
        directories = [
            self.maven_dir,
            self.m2_dir
        ]
        files = [
            (f"MavenCLI\\mvn.cmd", os.path.join(self.maven_dir, "bin", "mvn.cmd")),
            ("MavenCLI\\settings.xml", os.path.join(self.m2_dir, "settings.xml")),
            ("MavenCLI\\settings-security.xml", os.path.join(self.m2_dir, "settings-security.xml"))
        ]

        for directory in directories:
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                    logger.info(f"Created directory: {directory}")
                except Exception as e:
                    logger.error(f"Error creating directory {directory}: {str(e)}")
                    raise e

        for source, target in files:
            try:
                shutil.copy(source, target)
                logger.info(f"Copied {source} to {target}.")
            except Exception as e:
                logger.error(f"Error copying {source} to {target}: {str(e)}")
                raise e
        
        # Replace strings in files
        try:
            settings_xml_file = os.path.join(self.m2_dir, "settings.xml")
            settings_security_xml_file = os.path.join(self.m2_dir, "settings-security.xml")
            values_to_replace = {"<localRepository>${M2_REPO}</localRepository>": f"<localRepository>{os.environ['M2_REPO']}</localRepository>"}
            GenericFunctions.replace_strings_in_file(settings_xml_file, values_to_replace)
            logger.info(f"Replaced values in {settings_xml_file}: {values_to_replace}")

            values_to_replace = {"<master>{*AES*}REPLACEME{*AES*}</master>": f"<master>{os.environ['NEXUS_USER_PASS']}</master>"}
            GenericFunctions.replace_strings_in_file(settings_security_xml_file, values_to_replace)
            logger.info(f"Replaced values in {settings_security_xml_file}: {values_to_replace}")
        except Exception as e:
            logger.error("Failed to replace strings in settings.xml and settings-security.xml.")
            raise e
