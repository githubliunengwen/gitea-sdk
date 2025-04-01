import os
from gitea_issues_sdk.app.client import GiteaClient
from gitea_issues_sdk.app.issues import IssuesAPI, Issue, CreateIssueOption, EditIssueOption
# Initialize the client
client = GiteaClient(
    base_url="https://gitea.ailoveworld.cn/api/v1",
    token="d90121063caa66d5995647e02031abcaa4929bc4"
)


# Example: Create an attachment on an issue from a file
owner = "issues_api_test"
repo = "issues_api_test"
issue_number = 1
file_path = "D:\\Projects\\gitea-api-issnes-sdk\\gitea_issues_sdk\\examples\\attachments\\test.png"



# Initialize the issues API
issues_api = client.issues()


# Example: List all issues assigned to the authenticated user
my_issues = issues_api.search_issues(
    owner=owner
  
)
print(f"Found {len(my_issues)} issues assigned to me in {owner}")

# Example: List all issues in a repository
issues = issues_api.list_repo_issues(
    owner=owner,
    repo=repo,
  
)
print(f"Found {len(issues)} open issues in {owner}/{repo}")

# Example: Create a new issue
new_issue = issues_api.create_issue(
    owner=owner,
    repo=repo,
    title="Test issue from SDK",
    body="This is a test issue created using the Python SDK",
    assignees=["lnw"],
)
print(f"Created issue #{new_issue.number}: {new_issue.title}")

# Example: Get a specific issue
issue = issues_api.get_issue(
    owner=owner,
    repo=repo,
    index=new_issue.number
)
print(f"Issue #{issue.number}: {issue.title} ({issue.state})")

# Example: Edit an issue
updated_issue = issues_api.edit_issue(
    owner=owner,
    repo=repo,
    index=new_issue.number,
    title="Updated issue title",
    state="closed"
)
print(f"Updated issue #{updated_issue.number} to: {updated_issue.title}")



