"""API client for Gitea issues."""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Union

from ..client import GiteaClient
from .models import CreateIssueOption, EditIssueOption, Issue

logger = logging.getLogger("gitea_issues_sdk")


class IssuesAPI:
    """API client for working with Gitea issues."""

    def __init__(self, client: GiteaClient):
        """Initialize the issues API client.

        Args:
            client: The Gitea API client
        """
        self.client = client

    def search_issues(
        self,
        q: Optional[str] = None,
        priority_repo_id: Optional[int] = None,
        owner: Optional[str] = None,
        state: Optional[str] = "open",
        labels: Optional[List[str]] = None,
        milestones: Optional[List[str]] = None,
        type_: Optional[str] = None,
        since: Optional[datetime] = None,
        before: Optional[datetime] = None,
        assigned: bool = False,
        created: bool = False,
        mentioned: bool = False,
        review_requested: bool = False,
        reviewed: bool = False,
        team: Optional[str] = None,
        page: int = 1,
        limit: Optional[int] = None,
    ) -> List[Issue]:
        """Search for issues across repositories.

        Args:
            q: Search string
            priority_repo_id: Repository ID to prioritize in results
            owner: Filter by repository owner
            state: State of issues (open, closed, all)
            labels: Filter by labels
            milestones: Filter by milestones
            type_: Filter by issue type (issues, pulls)
            since: Only show issues updated after this time
            before: Only show issues updated before this time
            assigned: Filter issues assigned to the authenticated user
            created: Filter issues created by the authenticated user
            mentioned: Filter issues mentioning the authenticated user
            review_requested: Filter PRs where user's review was requested
            reviewed: Filter PRs reviewed by the authenticated user
            team: Filter by team (requires organization owner parameter)
            page: Page number
            limit: Page size

        Returns:
            List of issues matching the search criteria
        """
        params: Dict[str, Union[str, int, bool]] = {"page": page}
        
        if q:
            params["q"] = q
        if priority_repo_id:
            params["priority_repo_id"] = priority_repo_id
        if owner:
            params["owner"] = owner
        if state:
            params["state"] = state
        if labels:
            params["labels"] = ",".join(labels)
        if milestones:
            params["milestones"] = ",".join(milestones)
        if type_:
            params["type"] = type_
        if since:
            params["since"] = since.isoformat()
        if before:
            params["before"] = before.isoformat()
        if assigned:
            params["assigned"] = assigned
        if created:
            params["created"] = created
        if mentioned:
            params["mentioned"] = mentioned
        if review_requested:
            params["review_requested"] = review_requested
        if reviewed:
            params["reviewed"] = reviewed
        if team:
            params["team"] = team
        if limit:
            params["limit"] = limit
            
        logger.debug(f"Searching issues with params: {params}")
        response = self.client.get("repos/issues/search", params=params)
        
        issues = []
        for issue_data in response:
            try:
                issues.append(Issue(issue_data))
            except Exception as e:
                logger.error(f"Error parsing issue data: {e}")
                
        return issues

    def list_repo_issues(
        self,
        owner: str,
        repo: str,
        state: Optional[str] = None,
        labels: Optional[List[str]] = None,
        q: Optional[str] = None,
        type_: Optional[str] = None,
        milestones: Optional[List[str]] = None,
        since: Optional[datetime] = None,
        before: Optional[datetime] = None,
        created_by: Optional[str] = None,
        assigned_by: Optional[str] = None,
        mentioned_by: Optional[str] = None,
        page: int = 1,
        limit: Optional[int] = None,
    ) -> List[Issue]:
        """List issues in a repository.

        Args:
            owner: Repository owner
            repo: Repository name
            state: Issue state (open, closed, all)
            labels: Filter by labels
            q: Search string
            type_: Filter by type (issues, pulls)
            milestones: Filter by milestones
            since: Only show issues updated after this time
            before: Only show issues updated before this time
            created_by: Filter by creator
            assigned_by: Filter by assignee
            mentioned_by: Filter by mentioned user
            page: Page number
            limit: Page size

        Returns:
            List of issues in the repository
        """
        params: Dict[str, Union[str, int]] = {"page": page}
        
        if state:
            params["state"] = state
        if labels:
            params["labels"] = ",".join(labels)
        if q:
            params["q"] = q
        if type_:
            params["type"] = type_
        if milestones:
            params["milestones"] = ",".join(milestones)
        if since:
            params["since"] = since.isoformat()
        if before:
            params["before"] = before.isoformat()
        if created_by:
            params["created_by"] = created_by
        if assigned_by:
            params["assigned_by"] = assigned_by
        if mentioned_by:
            params["mentioned_by"] = mentioned_by
        if limit:
            params["limit"] = limit
            
        logger.debug(f"Listing issues for {owner}/{repo} with params: {params}")
        response = self.client.get(f"repos/{owner}/{repo}/issues", params=params)
        
        issues = []
        for issue_data in response:
            try:
                issues.append(Issue(issue_data))
            except Exception as e:
                logger.error(f"Error parsing issue data: {e}")
                
        return issues

    def get_issue(self, owner: str, repo: str, index: int) -> Issue:
        """Get a specific issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number

        Returns:
            The issue

        Raises:
            GiteaAPIError: If the issue doesn't exist
        """
        logger.debug(f"Getting issue {owner}/{repo}#{index}")
        response = self.client.get(f"repos/{owner}/{repo}/issues/{index}")
        return Issue(response)

    def create_issue(
        self,
        owner: str,
        repo: str,
        title: str,
        body: Optional[str] = None,
        assignee: Optional[str] = None,
        assignees: Optional[List[str]] = None,
        milestone: Optional[int] = None,
        labels: Optional[List[str]] = None,
        deadline: Optional[datetime] = None,
        ref: Optional[str] = None,
    ) -> Issue:
        """Create a new issue.

        Args:
            owner: Repository owner
            repo: Repository name
            title: Issue title
            body: Issue body
            assignee: Username of assignee
            assignees: Usernames of assignees
            milestone: Milestone ID
            labels: Label names
            deadline: Due date
            ref: Git reference

        Returns:
            The created issue

        Raises:
            GiteaAPIError: If the issue couldn't be created
        """
        issue_data = CreateIssueOption(
            title=title,
            body=body,
            assignee=assignee,
            assignees=assignees,
            milestone=milestone,
            labels=labels,
            deadline=deadline,
            ref=ref,
        )
        
        logger.debug(f"Creating issue in {owner}/{repo}: {title}")
        response = self.client.post(
            f"repos/{owner}/{repo}/issues",
            json_data=issue_data.to_dict(),
        )
        
        return Issue(response)

    def edit_issue(
        self,
        owner: str,
        repo: str,
        index: int,
        title: Optional[str] = None,
        body: Optional[str] = None,
        assignee: Optional[str] = None,
        assignees: Optional[List[str]] = None,
        milestone: Optional[int] = None,
        state: Optional[str] = None,
        labels: Optional[List[str]] = None,
        deadline: Optional[datetime] = None,
        ref: Optional[str] = None,
    ) -> Issue:
        """Edit an existing issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            title: New title
            body: New body
            assignee: New assignee
            assignees: New assignees
            milestone: New milestone ID
            state: New state
            labels: New labels
            deadline: New due date
            ref: New Git reference

        Returns:
            The updated issue

        Raises:
            GiteaAPIError: If the issue doesn't exist or couldn't be updated
        """
        issue_data = EditIssueOption(
            title=title,
            body=body,
            assignee=assignee,
            assignees=assignees,
            milestone=milestone,
            state=state,
            labels=labels,
            deadline=deadline,
            ref=ref,
        )
        
        logger.debug(f"Editing issue {owner}/{repo}#{index}")
        response = self.client.patch(
            f"repos/{owner}/{repo}/issues/{index}",
            json_data=issue_data.to_dict(),
        )
        
        return Issue(response)
