import os
import json
import logging
from tkinter import messagebox, filedialog


class CreateVariables:
    def __init__(self, system_type):
        self.system_type = system_type
        self.logger = logging.getLogger(__name__)

    def create(self):
        try:
            with open("constants.json", "r") as f:
                data = json.load(f)
                for item in data[self.system_type]["Variables"]:
                    self.create_variable(item)
                for item in data[self.system_type]["Files"]:
                    self.create_file(item)
                for item in data[self.system_type]["Directories"]:
                    self.create_directory(item)
                for item in data[self.system_type]["Connection_Details"]:
                    self.create_connection_detail(item)
        except Exception as e:
            self.logger.error(f"Error while reading constants.json: {str(e)}")
            raise e

    def create_variable(self, item):
        var_name = item["Name"]
        var_value = item["Value"]
        var_type = item.get("Type", "I")
        update_path = item.get("Path", "N")

        try:
            if update_path == "Y":
                if os.path.isabs(var_value):
                    if os.path.exists(var_value):
                        os.environ["PATH"] += os.pathsep + var_value
                    else:
                        self.show_error_message(item)
                        self.logger.error(f"Variable {var_name} could not be created. {var_value} is not a valid path.")
                else:
                    os.environ["PATH"] += os.pathsep + var_value

            if var_type == "E":
                if os.path.isabs(var_value):
                    if os.path.exists(var_value):
                        os.environ[var_name] = var_value
                        setattr(self, var_name, var_value)
                    else:
                        self.show_error_message(item)
                        self.logger.error(f"Variable {var_name} could not be created. {var_value} is not a valid path.")
                else:
                    os.environ[var_name] = var_value
                    setattr(self, var_name, var_value)

            elif var_type == "I":
                if os.path.isabs(var_value):
                    if os.path.exists(var_value):
                        setattr(self, var_name, var_value)
                    else:
                        self.show_error_message(item)
                        self.logger.error(f"Variable {var_name} could not be created. {var_value} is not a valid path.")
                else:
                    setattr(self, var_name, var_value)

        except Exception as e:
            self.logger.error(f"Error while creating variable {var_name}: {str(e)}")
            raise e

    def create_file(self, item):
        source = item.get("Source")
        target = item.get("Target")

        try:
            if os.path.exists(source):
                os.makedirs(os.path.dirname(target), exist_ok=True)
                os.replace(source, target)
            else:
                self.show_error_message(item)
                self.logger.error(f"File {source} could not be copied to {target}. {source} does not exist.")
        except Exception as e:
            self.logger.error(f"Error while copying file {source} to {target}: {str(e)}")
            raise e

    def create_directory(self, item):
        dir_path = item.get("Name")

        try:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            else:
                self.logger.warning(f"Directory {dir_path} already exists.")
        except Exception as e:
            self.logger.error(f"Error while creating directory {dir_path}: {str(e)}")
            raise e

    def create_connection_detail(self, item):
        name = item.get("Name")
        value = item.get("Value")
            try:
        # Your code to create the connection detail goes here
        pass
    except Exception as e:
        self.logger.error(f"Error while creating connection detail {name}: {str(e)}")
        raise e

def show_error_message(self, item):
    message = f"Could not create variable for {item['Name']} with value {item['Value']}. Please update the constants.json file with a valid path."
    result = messagebox.askyesno("Error", message)
    if result:
        file_path = filedialog.askopenfilename(initialdir=".", title="Select JSON file", filetypes=[("JSON files", "*.json")])
        os.startfile(file_path)
    else:
        raise Exception(message)




