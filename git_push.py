import subprocess
import os

def run_git_command(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return result.decode().strip()
    except subprocess.CalledProcessError as e:
        return e.output.decode().strip()

def git_add_commit_push(repo_path, commit_message):
    # Change to the repository directory
    os.chdir(repo_path)

    # Add changes
    add_result = run_git_command("git add .")
    print("Git Add Result:\n", add_result)

    # Commit changes
    commit_result = run_git_command(f"git commit -m \"{commit_message}\"")
    print("Git Commit Result:\n", commit_result)

    # Push changes
    push_result = run_git_command("git push")
    print("Git Push Result:\n", push_result)


