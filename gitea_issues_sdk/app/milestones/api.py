"""API client for Gitea issue milestones."""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Union

from ..client import GiteaClient
from .models import Milestone, CreateMilestoneOption, EditMilestoneOption

logger = logging.getLogger("gitea_issues_sdk")


class MilestonesAPI:
    """API client for working with Gitea issue milestones."""

    def __init__(self, client: GiteaClient):
        """Initialize the milestones API client.

        Args:
            client: The Gitea API client
        """
        self.client = client

    def list_milestones(
        self,
        owner: str,
        repo: str,
        state: Optional[str] = None,
        page: int = 1,
        limit: Optional[int] = None,
    ) -> List[Milestone]:
        """List milestones in a repository.

        Args:
            owner: Repository owner
            repo: Repository name
            state: Milestone state (open, closed, all)
            page: Page number
            limit: Page size

        Returns:
            List of milestones in the repository
        """
        params: Dict[str, Union[str, int]] = {"page": page}
        
        if state:
            params["state"] = state
        if limit:
            params["limit"] = limit
            
        logger.debug(f"Listing milestones for {owner}/{repo} with params: {params}")
        response = self.client.get(f"repos/{owner}/{repo}/milestones", params=params)
        
        milestones = []
        for milestone_data in response:
            try:
                milestones.append(Milestone(milestone_data))
            except Exception as e:
                logger.error(f"Error parsing milestone data: {e}")
                
        return milestones

    def get_milestone(self, owner: str, repo: str, id: int) -> Milestone:
        """Get a specific milestone.

        Args:
            owner: Repository owner
            repo: Repository name
            id: Milestone ID

        Returns:
            The milestone

        Raises:
            GiteaAPIError: If the milestone doesn't exist
        """
        logger.debug(f"Getting milestone {owner}/{repo}#{id}")
        response = self.client.get(f"repos/{owner}/{repo}/milestones/{id}")
        return Milestone(response)

    def create_milestone(
        self,
        owner: str,
        repo: str,
        title: str,
        description: Optional[str] = None,
        state: Optional[str] = None,
        due_on: Optional[datetime] = None,
    ) -> Milestone:
        """Create a new milestone.

        Args:
            owner: Repository owner
            repo: Repository name
            title: Milestone title
            description: Milestone description
            state: Milestone state (open, closed)
            due_on: Milestone due date

        Returns:
            The created milestone

        Raises:
            GiteaAPIError: If the milestone couldn't be created
        """
        milestone_data = CreateMilestoneOption(
            title=title,
            description=description,
            state=state,
            due_on=due_on,
        )
        
        logger.debug(f"Creating milestone in {owner}/{repo}: {title}")
        response = self.client.post(
            f"repos/{owner}/{repo}/milestones",
            json_data=milestone_data.to_dict(),
        )
        
        return Milestone(response)

    def edit_milestone(
        self,
        owner: str,
        repo: str,
        id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        state: Optional[str] = None,
        due_on: Optional[datetime] = None,
    ) -> Milestone:
        """Edit an existing milestone.

        Args:
            owner: Repository owner
            repo: Repository name
            id: Milestone ID
            title: New milestone title
            description: New milestone description
            state: New milestone state (open, closed)
            due_on: New milestone due date

        Returns:
            The updated milestone

        Raises:
            GiteaAPIError: If the milestone doesn't exist or couldn't be updated
        """
        milestone_data = EditMilestoneOption(
            title=title,
            description=description,
            state=state,
            due_on=due_on,
        )
        
        logger.debug(f"Editing milestone {owner}/{repo}#{id}")
        response = self.client.patch(
            f"repos/{owner}/{repo}/milestones/{id}",
            json_data=milestone_data.to_dict(),
        )
        
        return Milestone(response)

    def delete_milestone(self, owner: str, repo: str, id: int) -> bool:
        """Delete a milestone.

        Args:
            owner: Repository owner
            repo: Repository name
            id: Milestone ID

        Returns:
            True if the milestone was deleted successfully

        Raises:
            GiteaAPIError: If the milestone doesn't exist or couldn't be deleted
        """
        logger.debug(f"Deleting milestone {owner}/{repo}#{id}")
        self.client.delete(f"repos/{owner}/{repo}/milestones/{id}")
        return True

    def get_milestone_issues(
        self,
        owner: str,
        repo: str,
        milestone: int,
        state: Optional[str] = None,
        page: int = 1,
        limit: Optional[int] = None,
    ) -> List[dict]:
        """Get issues for a milestone.

        Args:
            owner: Repository owner
            repo: Repository name
            milestone: Milestone ID
            state: Issue state (open, closed, all)
            page: Page number
            limit: Page size

        Returns:
            List of issues for the milestone

        Raises:
            GiteaAPIError: If the milestone doesn't exist
        """
        params: Dict[str, Union[str, int]] = {
            "milestone": milestone,
            "page": page,
        }
        
        if state:
            params["state"] = state
        if limit:
            params["limit"] = limit
            
        logger.debug(f"Getting issues for milestone {owner}/{repo}#{milestone} with params: {params}")
        return self.client.get(f"repos/{owner}/{repo}/issues", params=params)
