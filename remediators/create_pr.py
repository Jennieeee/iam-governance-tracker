from github import Github
import os

def create_pr(repo_name, token, branch="auto-fix"):
    g = Github(token)
    repo = g.get_repo(repo_name)
    base = repo.get_branch("main")

    repo.create_git_ref(ref=f"refs/heads/{branch}", sha=base.commit.sha)

    file_path = "results/scan-logs.json"
    with open(file_path, "r") as f:
        content = f.read()

    repo.update_file(file_path, "Auto-fix: Update scan log", content, repo.get_contents(file_path, ref=branch).sha, branch=branch)

    repo.create_pull(
        title="🛠 Auto-Remediation PR",
        body="This PR includes findings from IAM scan and updates log files.",
        base="main",
        head=branch
    )
