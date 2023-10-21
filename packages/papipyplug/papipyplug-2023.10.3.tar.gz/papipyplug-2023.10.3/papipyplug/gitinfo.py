# from dataclasses import dataclass
# from git.repo import Repo
# import logging
# import json


# @dataclass
# class GitInfo:
#     repository: str
#     commit_hash: str
#     active_branch: str


# class UncommittedChangesError(Exception):
#     """
#     TODO: Add check and subsequent error for uncommitted changes in the repo
#     to ensure the commit hash pulled will accurately reflect state of code
#     """


# def version() -> GitInfo:
#     """
#     Returns relevant metadata for the git repository
#     as a mechanism to comply with FAIR practices.
#     """
#     logging.info("fetching metadata")
#     repo = Repo(search_parent_directories=True)
#     if repo.is_dirty():
#         logging.error("uncommitted files, script cannot be verified")
#         # raise UncommittedChangesError
#     info = GitInfo(
#         repo.remotes.origin.url.replace("git@github.com:", "https://github.com/").replace(".git", ""),
#         repo.active_branch.commit.hexsha,
#         repo.active_branch.name,
#     )
#     return info.__dict__


# def git_meta():
#     metadata_file = "git-metadata.json"
#     with open(metadata_file, "w") as f:
#         json.dump(version(), f)


# if __name__ == "__main__":
#     git_meta()
