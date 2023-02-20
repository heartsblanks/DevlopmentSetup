import os
import logging
import socket
import subprocess
from GenericFunctions import GenericFunctions
from createVariables import CreateVariables


class CheckConnections:
    def __init__(self, install_type):
        self.generic_functions = GenericFunctions()
        create_variables = CreateVariables(install_type)
        create_variables.create()
        create_variables = CreateVariables("GIT")
        create_variables.create()
        create_variables = CreateVariables("CVS")
        create_variables.create()

    def check_git_connection(self):
        try:
            os.system("git ls-remote")
            logging.info("Git connection successful")
        except:
            message = "Could not connect to Git. Please check your internet connection and Git configuration."
            logging.error(message)
            raise Exception(message)

    def check_cvs_connection(self):
        cvs_host = "cvs.example.com"
        cvs_port = 2401
        try:
            socket.create_connection((cvs_host, cvs_port), timeout=5)
            logging.info("CVS connection successful")
        except:
            message = "Could not connect to CVS. Please check your internet connection and CVS configuration."
            logging.error(message)
            raise Exception(message)

    def check_command(self, command):
        try:
            subprocess.run(command, check=True, shell=True)
            logging.info(f"Command '{command}' successful")
        except subprocess.CalledProcessError as e:
            message = f"Command '{command}' failed: {e}"
            logging.error(message)
            raise Exception(message)
