class GenericFunctions:
    def replace_strings_in_file(self, file_path, replacements):
        try:
            with open(file_path, 'r') as file:
                file_data = file.read()

            # Replace the target strings with their corresponding values
            for target, value in replacements.items():
                file_data = file_data.replace(target, value)

            with open(file_path, 'w') as file:
                file.write(file_data)

        except Exception as e:
            logger.error(f"Error while replacing strings in file {file_path}: {str(e)}")
            raise e

            
#gf = GenericFunctions()
#replacements = {
 #   "<string1>": "value1",
  #  "<string2>": "value2",
  #  "<string3>": "value3"
#}
#gf.replace_strings_in_file("file_path", replacements)
