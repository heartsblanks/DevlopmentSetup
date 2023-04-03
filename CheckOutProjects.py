from original_file import CheckOutProjects, CheckoutError

update_type = "-q"  # Example value for update_type
workspace_dir = "/path/to/workspace"  # Example value for workspace_dir
log_file = "checkout.log"  # Example value for log_file

project1 = {"name": "project1", "tags": {"cvs": "tag1", "git": "tag2"}, "folder_name": "project1_folder"}
project2 = {"name": "project2", "tags": {"cvs": "tag3", "git": "tag4"}, "folder_name": "project2_folder"}
project3 = {"name": "project3", "tags": {"cvs": None, "git": "tag5"}, "folder_name": "project3_folder"}

checkout = CheckOutProjects(update_type, workspace_dir, log_file)
project_list = [project1, project2, project3]
checkout.checkout_projects(project_list)


import os
import subprocess
import logging


class CheckOutProjects:
    def __init__(self, update_type, workspace_dir, log_file="checkout.log"):
        self.update_type = update_type
        self.workspace_dir = workspace_dir
        self.log_file = log_file

    def checkout_projects(self, project_list):
        logging.basicConfig(filename=self.log_file, level=logging.DEBUG)

        try:
            logging.info(f"Starting checkout process for projects")

            for project in project_list:
                if "name" in project and "folder_name" in project:
                    project_name = project["name"]
                    folder_name = project["folder_name"]
                    
                    if "cvs" in project.get("tags", {}):
                        tag = project["tags"]["cvs"]
                        self.checkout_cvs_project(project_name, folder_name, tag)
                    elif "git" in project.get("tags", {}):
                        tag = project["tags"]["git"]
                        self.checkout_git_project(project_name, folder_name, tag)
                    else:
                        self.checkout_latest_project(project_name, folder_name)
                else:
                    raise ValueError("Invalid project parameters")

            logging.info("Finished checkout process for projects")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error checking out projects: {e}")
            raise CheckoutError(str(e))

    def checkout_cvs_project(self, project_name, folder_name, tag):
        logging.info(f"Checking out {project_name} project from CVS with tag {tag}")

        try:
            cmd = f"cvs {self.update_type} {tag} {project_name}"
            cwd = os.path.join(self.workspace_dir, folder_name)
            subprocess.check_output(cmd, shell=True, cwd=cwd)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error checking out {project_name} project: {e}")
            raise CheckoutError(str(e))

    def checkout_git_project(self, project_name, folder_name, tag):
        logging.info(f"Checking out {project_name} project from GIT with tag {tag}")

        try:
            cmd = f"git {self.update_type} && git checkout {tag}"
            cwd = os.path.join(self.workspace_dir, folder_name)
            subprocess.check_output(cmd, shell=True, cwd=cwd)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error checking out {project_name} project: {e}")
            raise CheckoutError(str(e))
    
    def checkout_latest_project(self, project_name, folder_name):
        logging.info(f"Checking out {project_name} project with the latest version")
        
        try:
            cmd = f"cvs {self.update_type} {project_name}"  # Assuming CVS, replace with Git command as needed
            cwd = os.path.join(self.workspace_dir, folder_name)
            subprocess.check_output(cmd, shell=True, cwd=cwd)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error checking out {project_name} project: {e}")
            raise CheckoutError(str(e))


class CheckoutError(Exception):
    pass
