
import os
import subprocess
import logging


class CheckOutProjects:
    def __init__(self, log_file="checkout.log"):
        self.log_file = log_file

    def checkout_projects(self, system_type):
        logging.basicConfig(filename=self.log_file, level=logging.DEBUG)

        try:
            logging.info(f"Starting checkout process for {system_type} projects")

            if system_type == "EAI":
                self.checkout_cvs_project("EAI")
            else:
                self.checkout_git_project("DS")

            logging.info(f"Finished checkout process for {system_type} projects")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error checking out projects: {e}")
            raise CheckoutError(str(e))

    def checkout_cvs_project(self, project_name):
        logging.info(f"Checking out {project_name} project from CVS")

        try:
            cmd = f"cvs checkout {project_name}"
            subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error checking out {project_name} project: {e}")
            raise CheckoutError(str(e))

    def checkout_git_project(self, project_name):
        logging.info(f"Checking out {project_name} project from GIT")

        try:
            cmd = f"git clone git@github.com:myorg/{project_name}.git"
            subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error checking out {project_name} project: {e}")
            raise CheckoutError(str(e))


class CheckoutError(Exception):
    pass
