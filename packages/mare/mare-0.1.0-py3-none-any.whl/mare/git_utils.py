import subprocess
from pathlib import Path

GET_REPO_NAME_CMD = "git rev-parse --show-toplevel".split()
GET_BRANCH_NAME_CMD = "git rev-parse --abbrev-ref HEAD".split()
GET_ALL_BRANCH_NAME_CMD = "git branch -a"

def get_repo_path() -> Path:
  repo_path = subprocess.run(
    GET_REPO_NAME_CMD,
    capture_output=True,
    text=True
  ).stdout.strip()
  return Path(repo_path)

def get_repo_name() -> str:
  repo_path = subprocess.run(
    GET_REPO_NAME_CMD,
    capture_output=True,
    text=True
  ).stdout.strip()

  repo_name = Path(repo_path).name

  return repo_name

def get_branch_name() -> str:
  branch_name = subprocess.run(
    GET_BRANCH_NAME_CMD,
    capture_output=True,
    text=True
  ).stdout
  return branch_name.strip()

def get_all_git_branch_name() -> list:
  all_branches = subprocess.run(
    GET_BRANCH_NAME_CMD,
    capture_output=True,
    text=True
  ).stdout.strip()
  return [all_branches]

def main():
  print(get_repo_name())
  print(type(get_repo_name()))
  print(get_repo_path())
if __name__ == "__main__":
  main()
