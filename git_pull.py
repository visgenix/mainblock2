import os
import subprocess

def run_git_command(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return result.decode().strip()
    except subprocess.CalledProcessError as e:
        return e.output.decode().strip()

def check_and_pull_repo(repo_path):
    # Change to the repository directory
    os.chdir(repo_path)

    # Check the current status
    status = run_git_command("git status")
    print("Git Status:\n", status)

    # Update remote references
    run_git_command("git remote update")

    # Check if the local repo is behind
    status = run_git_command("git status -uno")
    if "Your branch is behind" in status:
        print("New commits available. Pulling changes...")
        pull_result = run_git_command("git pull")
        print(pull_result)
    else:
        print("Your repository is up-to-date.")

