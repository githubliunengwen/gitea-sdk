"""API client for Gitea issue stopwatches and tracked time."""

import logging
from typing import Dict, List, Optional, Union

from ..client import GiteaClient
from .models import TrackedTime

logger = logging.getLogger("gitea_issues_sdk")


class StopwatchAPI:
    """API client for working with Gitea issue stopwatches and tracked time."""

    def __init__(self, client: GiteaClient):
        """Initialize the stopwatch API client.

        Args:
            client: The Gitea API client
        """
        self.client = client

    def list_tracked_times(
        self,
        owner: str,
        repo: str,
        index: int,
        user: Optional[str] = None,
        since: Optional[str] = None,
        before: Optional[str] = None,
        page: int = 1,
        limit: Optional[int] = None,
    ) -> List[TrackedTime]:
        """List tracked times for an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            user: Filter by username
            since: Only show tracked times after this ISO 8601 timestamp
            before: Only show tracked times before this ISO 8601 timestamp
            page: Page number
            limit: Page size

        Returns:
            List of tracked times for the issue
        """
        params: Dict[str, Union[str, int]] = {"page": page}
        
        if limit:
            params["limit"] = limit
        if user:
            params["user"] = user
        if since:
            params["since"] = since
        if before:
            params["before"] = before
            
        logger.debug(f"Listing tracked times for issue {owner}/{repo}#{index} with params: {params}")
        response = self.client.get(f"repos/{owner}/{repo}/issues/{index}/times", params=params)
        
        tracked_times = []
        for time_data in response:
            try:
                tracked_times.append(TrackedTime(time_data))
            except Exception as e:
                logger.error(f"Error parsing tracked time data: {e}")
                
        return tracked_times

    def add_tracked_time(
        self,
        owner: str,
        repo: str,
        index: int,
        time: int,
    ) -> TrackedTime:
        """Add tracked time to an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            time: Time in seconds to add

        Returns:
            The added tracked time

        Raises:
            GiteaAPIError: If the tracked time couldn't be added
        """
        data = {"time": time}
        
        logger.debug(f"Adding {time} seconds of tracked time to issue {owner}/{repo}#{index}")
        response = self.client.post(
            f"repos/{owner}/{repo}/issues/{index}/times",
            json_data=data,
        )
        
        return TrackedTime(response)

    def delete_tracked_time(
        self,
        owner: str,
        repo: str,
        index: int,
        tracked_time_id: int,
    ) -> bool:
        """Delete tracked time from an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            tracked_time_id: Tracked time ID

        Returns:
            True if the tracked time was deleted successfully

        Raises:
            GiteaAPIError: If the tracked time doesn't exist or couldn't be deleted
        """
        logger.debug(f"Deleting tracked time {tracked_time_id} from issue {owner}/{repo}#{index}")
        self.client.delete(f"repos/{owner}/{repo}/issues/{index}/times/{tracked_time_id}")
        return True

    def reset_tracked_time(
        self,
        owner: str,
        repo: str,
        index: int,
    ) -> bool:
        """Reset all tracked time for an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number

        Returns:
            True if the tracked time was reset successfully

        Raises:
            GiteaAPIError: If the tracked time couldn't be reset
        """
        logger.debug(f"Resetting all tracked time for issue {owner}/{repo}#{index}")
        self.client.delete(f"repos/{owner}/{repo}/issues/{index}/times")
        return True

    def start_stopwatch(
        self,
        owner: str,
        repo: str,
        index: int,
    ) -> bool:
        """Start a stopwatch for an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number

        Returns:
            True if the stopwatch was started successfully

        Raises:
            GiteaAPIError: If the stopwatch couldn't be started
        """
        logger.debug(f"Starting stopwatch for issue {owner}/{repo}#{index}")
        self.client.post(f"repos/{owner}/{repo}/issues/{index}/stopwatch/start")
        return True

    def stop_stopwatch(
        self,
        owner: str,
        repo: str,
        index: int,
    ) -> bool:
        """Stop a stopwatch for an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number

        Returns:
            True if the stopwatch was stopped successfully

        Raises:
            GiteaAPIError: If the stopwatch couldn't be stopped
        """
        logger.debug(f"Stopping stopwatch for issue {owner}/{repo}#{index}")
        self.client.post(f"repos/{owner}/{repo}/issues/{index}/stopwatch/stop")
        return True

    def delete_stopwatch(
        self,
        owner: str,
        repo: str,
        index: int,
    ) -> bool:
        """Delete a stopwatch for an issue without adding time.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number

        Returns:
            True if the stopwatch was deleted successfully

        Raises:
            GiteaAPIError: If the stopwatch couldn't be deleted
        """
        logger.debug(f"Deleting stopwatch for issue {owner}/{repo}#{index}")
        self.client.delete(f"repos/{owner}/{repo}/issues/{index}/stopwatch/delete")
        return True
