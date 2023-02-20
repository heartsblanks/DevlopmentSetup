import logging
import os

class GenericFunctions:
    @staticmethod
    def replace_strings_in_file(file_path, replacements):
        logger = logging.getLogger(__name__)
        if not os.path.isfile(file_path):
            logger.error(f"File {file_path} does not exist.")
            return
        try:
            with open(file_path, "r") as f:
                file_content = f.read()
            for old_string, new_string in replacements.items():
                file_content = file_content.replace(old_string, new_string)
                logger.info(f"Replaced '{old_string}' with '{new_string}' in file {file_path}.")
            with open(file_path, "w") as f:
                f.write(file_content)
        except Exception as e:
            logger.error(f"Error replacing strings in file {file_path}: {str(e)}")


            
#gf = GenericFunctions()
#replacements = {
 #   "<string1>": "value1",
  #  "<string2>": "value2",
  #  "<string3>": "value3"
#}
#gf.replace_strings_in_file("file_path", replacements)
