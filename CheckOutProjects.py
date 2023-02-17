import os
import logging
import git


class CheckOutProjects:
    def __init__(self, git_url, destination_path):
        self.git_url = git_url
        self.destination_path = destination_path
        self.logger = logging.getLogger(__name__)

    def clone_repo(self):
        try:
            if not os.path.exists(self.destination_path):
                os.makedirs(self.destination_path, exist_ok=True)

            git.Repo.clone_from(self.git_url, self.destination_path)
            self.logger.info(f"Repository cloned from {self.git_url} to {self.destination_path}.")
        except git.exc.GitCommandError as e:
            self.logger.error(f"Error while cloning repository from {self.git_url} to {self.destination_path}: {str(e)}")
            raise e

    def pull_repo(self):
        try:
            repo = git.Repo(self.destination_path)
            repo.git.pull()
            self.logger.info(f"Repository at {self.destination_path} has been pulled successfully.")
        except git.exc.GitCommandError as e:
            self.logger.error(f"Error while pulling repository at {self.destination_path}: {str(e)}")
            raise e
