"""API client for Gitea issue timeline events."""

import logging
from typing import Dict, List, Optional, Union

from ..client import GiteaClient
from .models import TimelineEvent

logger = logging.getLogger("gitea_issues_sdk")


class TimelineAPI:
    """API client for working with Gitea issue timeline events."""

    def __init__(self, client: GiteaClient):
        """Initialize the timeline API client.

        Args:
            client: The Gitea API client
        """
        self.client = client

    def list_timeline_events(
        self,
        owner: str,
        repo: str,
        index: int,
        page: int = 1,
        limit: Optional[int] = None,
        since: Optional[str] = None,
        before: Optional[str] = None,
    ) -> List[TimelineEvent]:
        """List timeline events for an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            page: Page number
            limit: Page size
            since: Only show events after this ISO 8601 timestamp
            before: Only show events before this ISO 8601 timestamp

        Returns:
            List of timeline events for the issue
        """
        params: Dict[str, Union[str, int]] = {"page": page}
        
        if limit:
            params["limit"] = limit
        if since:
            params["since"] = since
        if before:
            params["before"] = before
            
        logger.debug(f"Listing timeline events for issue {owner}/{repo}#{index} with params: {params}")
        response = self.client.get(f"repos/{owner}/{repo}/issues/{index}/timeline", params=params)
        
        events = []
        for event_data in response:
            try:
                events.append(TimelineEvent(event_data))
            except Exception as e:
                logger.error(f"Error parsing timeline event data: {e}")
                
        return events
    
    def filter_events_by_type(
        self,
        events: List[TimelineEvent],
        event_type: str,
    ) -> List[TimelineEvent]:
        """Filter timeline events by type.

        Args:
            events: List of timeline events to filter
            event_type: Event type to filter by

        Returns:
            Filtered list of timeline events
        """
        logger.debug(f"Filtering timeline events by type: {event_type}")
        return [event for event in events if event.type == event_type]
    
    def filter_events_by_user(
        self,
        events: List[TimelineEvent],
        username: str,
    ) -> List[TimelineEvent]:
        """Filter timeline events by user.

        Args:
            events: List of timeline events to filter
            username: Username to filter by

        Returns:
            Filtered list of timeline events
        """
        logger.debug(f"Filtering ti meline events by user: {username}")
        return [
            event for event in events 
            if event.user and event.user.username == username
        ]
    
    def sort_events_by_date(
        self,
        events: List[TimelineEvent],
        ascending: bool = True,
    ) -> List[TimelineEvent]:
        """Sort timeline events by date.

        Args:
            events: List of timeline events to sort
            ascending: Sort in ascending order if True, descending if False

        Returns:
            Sorted list of timeline events
        """
        logger.debug(f"Sorting timeline events by date (ascending={ascending})")
        return sorted(events, key=lambda event: event.created_at, reverse=not ascending)
