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

    def get_developer_ports(self, ssh_host, ssh_port, ssh_username, ssh_password):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ssh_host, port=ssh_port, username=ssh_username, password=ssh_password)

        try:
            stdin, stdout, stderr = ssh.exec_command("mqsilist -v")
            output = stdout.read().decode("utf-8")
            self.HTTP_CONNECTOR = self.HTTPS_CONNECTOR = self.WEBADMINPORT_SSL = self.WEBADMINPORT = self.MQ_LISTENER_PORT = self.DEBUG_PORT = "Not Found"
            for line in output.splitlines():
                if "HTTPConnector:" in line:
                    self.HTTP_CONNECTOR = line.split(":")[1].strip()
                elif "HTTPSConnector:" in line:
                    self.HTTPS_CONNECTOR = line.split(":")[1].strip()
                elif "Webadminport (SSL):" in line:
                    self.WEBADMINPORT_SSL = line.split(":")[1].strip()
                elif "Webadminport:" in line:
                    self.WEBADMINPORT = line.split(":")[1].strip()
                elif "MQ-Listener Port:" in line:
                    self.MQ_LISTENER_PORT = line.split(":")[1].strip()
                elif "Debug Port:" in line:
                    self.DEBUG_PORT = line.split(":")[1].strip()
        except Exception as e:
            self.logger.error(f"Error getting developer ports via SSH: {str(e)}")
            raise e
        finally:
            ssh.close()
            
#gf = GenericFunctions()
#replacements = {
 #   "<string1>": "value1",
  #  "<string2>": "value2",
  #  "<string3>": "value3"
#}
#gf.replace_strings_in_file("file_path", replacements)
