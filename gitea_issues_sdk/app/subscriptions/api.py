"""API client for Gitea issue subscriptions."""

import logging
from typing import Dict, List, Optional, Union

from ..client import GiteaClient

logger = logging.getLogger("gitea_issues_sdk")


class SubscriptionsAPI:
    """API client for working with Gitea issue subscriptions."""

    def __init__(self, client: GiteaClient):
        """Initialize the subscriptions API client.

        Args:
            client: The Gitea API client
        """
        self.client = client

    def list_subscribers(
        self,
        owner: str,
        repo: str,
        index: int,
        page: int = 1,
        limit: Optional[int] = None,
    ) -> List[Dict]:
        """List users who are subscribed to an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            page: Page number
            limit: Page size

        Returns:
            List of users subscribed to the issue
        """
        params: Dict[str, Union[str, int]] = {"page": page}
        
        if limit:
            params["limit"] = limit
            
        logger.debug(f"Listing subscribers for issue {owner}/{repo}#{index} with params: {params}")
        return self.client.get(f"repos/{owner}/{repo}/issues/{index}/subscriptions", params=params)

    def check_subscription(
        self,
        owner: str,
        repo: str,
        index: int,
        user: str,
    ) -> bool:
        """Check if a user is subscribed to an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            user: Username to check

        Returns:
            True if the user is subscribed, False otherwise

        Raises:
            GiteaAPIError: If the user doesn't exist
        """
        logger.debug(f"Checking if {user} is subscribed to issue {owner}/{repo}#{index}")
        try:
            self.client.get(f"repos/{owner}/{repo}/issues/{index}/subscriptions/{user}")
            return True
        except Exception as e:
            if "404" in str(e):
                return False
            raise

    def add_subscription(
        self,
        owner: str,
        repo: str,
        index: int,
        user: str,
    ) -> bool:
        """Subscribe a user to an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            user: Username to subscribe

        Returns:
            True if the subscription was added successfully

        Raises:
            GiteaAPIError: If the subscription couldn't be added
        """
        logger.debug(f"Adding subscription for {user} to issue {owner}/{repo}#{index}")
        self.client.put(f"repos/{owner}/{repo}/issues/{index}/subscriptions/{user}")
        return True

    def remove_subscription(
        self,
        owner: str,
        repo: str,
        index: int,
        user: str,
    ) -> bool:
        """Unsubscribe a user from an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            user: Username to unsubscribe

        Returns:
            True if the subscription was removed successfully

        Raises:
            GiteaAPIError: If the subscription couldn't be removed
        """
        logger.debug(f"Removing subscription for {user} from issue {owner}/{repo}#{index}")
        self.client.delete(f"repos/{owner}/{repo}/issues/{index}/subscriptions/{user}")
        return True
