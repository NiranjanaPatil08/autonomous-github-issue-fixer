import os
import tempfile
from git import Repo


def clone_repo(repo_url):
    """
    Clone a GitHub repository locally and return the path.
    """

    temp_dir = tempfile.mkdtemp()

    Repo.clone_from(repo_url, temp_dir)

    return temp_dir
