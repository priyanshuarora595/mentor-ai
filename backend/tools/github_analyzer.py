import git
import os


def clone_repo(repo_url):

    repo_path = "repos/temp_repo"

    if not os.path.exists(repo_path):
        git.Repo.clone_from(repo_url, repo_path)

    return repo_path
