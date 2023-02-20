import os
import logging
from GenericFunctions import replace_strings_in_file


class CreateProperties:
    def __init__(self, install_type):
        self.install_type = install_type
        self.logger = logging.getLogger(__name__)

    def create(self):
        source_file = f"template_broker.local_{self.install_type}.properties"
        target_file = f"Z:\\local_{self.install_type}.properties"

        try:
            if os.path.exists(source_file):
                with open(source_file, "r") as f:
                    source_data = f.read()
            else:
                raise Exception(f"Source file {source_file} does not exist.")

            with open(target_file, "w") as f:
                f.write(source_data)

            replace_strings_in_file(target_file, {
                "{{INSTALL_TYPE}}": self.install_type,
            })

            self.logger.info(f"Created {target_file} file with replaced strings.")
        except Exception as e:
            self.logger.error(f"Error while creating {target_file} file: {str(e)}")
            raise e
