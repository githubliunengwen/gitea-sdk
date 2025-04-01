import os
from gitea_issues_sdk.app.attachments import AttachmentsAPI, Attachment, EditAttachmentOption
from gitea_issues_sdk.app.client import GiteaClient

# Initialize the client
client = GiteaClient(
    base_url="https://gitea.ailoveworld.cn/api/v1",
    token="25ad59263c1d35a2b17b1af99b94a577dc76f815"
)

# Initialize the attachments API
attachments_api = AttachmentsAPI(client)

# Example: Create an attachment on an issue from a file
owner = "issues_api_test"
repo = "issues_api_test"
issue_number = 1
file_path = "D:\\Projects\\gitea-api-issnes-sdk\\gitea_issues_sdk\\examples\\attachments\\test.png"
attachment_id = 41

# Upload the attachment
attachment = attachments_api.create_issue_attachment(
    owner=owner,
    repo=repo,
    index=issue_number,
    file_path=file_path
)
print(f"Created attachment: {attachment.name} (ID: {attachment.id})")

# Example: Create an attachment from bytes
with open(file_path, 'rb') as f:
    file_content = f.read()

attachment_from_bytes = attachments_api.create_issue_attachment_from_bytes(
    owner=owner,
    repo=repo,
    index=issue_number,
    file_content=file_content,
    file_name="custom_name.png"
)
print(f"Created attachment from bytes: {attachment_from_bytes.name}")

# Example: Edit an attachment
updated_attachment = attachments_api.edit_issue_attachment(
    owner=owner,
    repo=repo,
    index=issue_number,
    attachment_id=attachment_id,
    name="renamed_file.png"
)
print(f"Updated attachment name: {updated_attachment.name}")

# Example: Get and download an attachment
retrieved_attachment = attachments_api.get_issue_attachment(
    owner=owner,
    repo=repo,
    index=issue_number,
    attachment_id=attachment_id,
)
print(f"Retrieved attachment: {retrieved_attachment.name}, size: {retrieved_attachment.size} bytes")

# Example: Delete an attachment
attachments_api.delete_issue_attachment(
    owner=owner,
    repo=repo,
    index=issue_number,
    attachment_id=attachment_id
)
print(f"Deleted attachment with ID: {attachment_id}")

# Example: List all attachments on an issue
attachments = attachments_api.list_issue_attachments(
    owner=owner,
    repo=repo,
    index=issue_number,
    page=1,
    limit=10
)
print(f"Found {len(attachments)} attachments on issue #{issue_number}")

# Example: Comment attachment operations
comment_id = 123  # Replace with an actual comment ID

# Get a comment attachment
comment_attachment = attachments_api.get_comment_attachment(
    owner=owner,
    repo=repo,
    id=comment_id,
    attachment_id=attachment_from_bytes.id,
)
print(f"Retrieved comment attachment: {comment_attachment.name}")

# Edit a comment attachment
updated_comment_attachment = attachments_api.edit_comment_attachment(
    owner=owner,
    repo=repo,
    id=comment_id,
    attachment_id=attachment_from_bytes.id,
    name="updated_comment_file.png"
)
print(f"Updated comment attachment name: {updated_comment_attachment.name}")

# Delete a comment attachment
attachments_api.delete_comment_attachment(
    owner=owner,
    repo=repo,
    id=comment_id,
    attachment_id=attachment_from_bytes.id,
)
print(f"Deleted comment attachment with ID: {attachment_from_bytes.id}")

# Example: List comment attachments
comment_attachments = attachments_api.list_comment_attachments(
    owner=owner,
    repo=repo,
    id=comment_id,
    page=1,
    limit=10
)
print(f"Found {len(comment_attachments)} attachments on comment #{comment_id}")
