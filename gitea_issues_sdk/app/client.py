"""Base client for interacting with the Gitea API."""

import logging
from typing import Any, Dict, Optional, Union

import requests
from requests.exceptions import RequestException

class GiteaAPIError(Exception):
    """Base exception for all Gitea API errors."""
    pass

class GiteaClient:
    """Client for interacting with the Gitea API."""

    def __init__(
        self,
        base_url: str,
        token: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        timeout: int = 30,
    ):
        """Initialize the Gitea API client.

        Args:
            base_url: Base URL of the Gitea API (e.g., 'https://gitea.example.com/api/v1')
            token: Personal access token for authentication
            username: Username for basic authentication (alternative to token)
            password: Password for basic authentication (alternative to token)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.logger = logging.getLogger("gitea_issues_sdk")
        
        # Set up authentication
        if token:
            self.session.headers.update({"Authorization": f"token {token}"})
        elif username and password:
            self.session.auth = (username, password)
        
        # Set common headers
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
        })
        
        self.logger.debug(f"Initialized Gitea client for {base_url}")

    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Union[Dict[str, Any], list, bytes]:
        """Make a request to the Gitea API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API endpoint path
            params: Query parameters
            data: Form data
            json_data: JSON data
            files: File data

        Returns:
            Response data as dictionary or list

        Raises:
            GiteaAPIError: If the API returns an error
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        self.logger.debug(f"{method} {url}")
        
        try:
            if files:
                self.session.headers.pop("Content-Type", None)
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json_data,
                files=files,
                timeout=self.timeout,
            )
            
            # Log request details at debug level
            self.logger.debug(f"Response status: {response.status_code}")
            
            # Handle different response status codes
            if response.status_code == 204:  # No content
                return {}
                
            if 200 <= response.status_code < 300:
                return response.json() if response.content else response.content
                
            # Handle error responses
            error_message = "Unknown error"
            try:
                error_data = response.json()
                if isinstance(error_data, dict) and "message" in error_data:
                    error_message = error_data["message"]
            except ValueError:
                error_message = response.text or f"HTTP {response.status_code}"

            self.logger.error(f"API error: {response.status_code} - {error_message}")
            raise GiteaAPIError(f"API error ({response.status_code}): {error_message}")
            
        except RequestException as e:
            self.logger.error(f"Connection error: {str(e)}")
            raise GiteaAPIError(f"Failed to connect to Gitea API: {str(e)}")

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Union[Dict[str, Any], list]:
        """Make a GET request to the API.

        Args:
            path: API endpoint path
            params: Query parameters

        Returns:
            Response data
        """
        return self.request("GET", path, params=params)

    def post(self, path: str, params: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None, files: Optional[Dict[str, Any]] = None) -> Union[Dict[str, Any], list]:
        """Make a POST request to the API.

        Args:
            path: API endpoint path
            params: Query parameters
            json_data: JSON data
            files: File data
        Returns:
            Response data
        """
        return self.request("POST", path, params=params, json_data=json_data, files=files)

    def put(self, path: str, params: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None) -> Union[Dict[str, Any], list]:
        """Make a PUT request to the API.

        Args:
            path: API endpoint path
            params: Query parameters
            json_data: JSON data

        Returns:
            Response data
        """
        return self.request("PUT", path, params=params, json_data=json_data)

    def delete(self, path: str, params: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None) -> Union[Dict[str, Any], list]:
        """Make a DELETE request to the API.

        Args:
            path: API endpoint path
            params: Query parameters
            json_data: JSON data for DELETE requests with a body

        Returns:
            Response data
        """
        return self.request("DELETE", path, params=params, json_data=json_data)
        
    def patch(self, path: str, params: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None) -> Union[Dict[str, Any], list]:
        """Make a PATCH request to the API.

        Args:
            path: API endpoint path
            params: Query parameters
            json_data: JSON data

        Returns:
            Response data
        """
        return self.request("PATCH", path, params=params, json_data=json_data)
        
    def issues(self):
        """Get the issues API client.

        Returns:
            IssuesAPI client
        """
        from .issues import IssuesAPI
        return IssuesAPI(self)
        
    def comments(self):
        """Get the comments API client.

        Returns:
            CommentsAPI client
        """
        from .comments import CommentsAPI
        return CommentsAPI(self)
        
    def labels(self):
        """Get the labels API client.

        Returns:
            LabelsAPI client
        """
        from .labels import LabelsAPI
        return LabelsAPI(self)
        
    def milestones(self):
        """Get the milestones API client.

        Returns:
            MilestonesAPI client
        """
        from .milestones import MilestonesAPI
        return MilestonesAPI(self)
        
    def reactions(self):
        """Get the reactions API client.

        Returns:
            ReactionsAPI client
        """
        from .reactions import ReactionsAPI
        return ReactionsAPI(self)
        
    def attachments(self):
        """Get the attachments API client.

        Returns:
            AttachmentsAPI client
        """
        from .attachments import AttachmentsAPI
        return AttachmentsAPI(self)
        
    def blocks(self):
        """Get the blocks API client.

        Returns:
            BlocksAPI client
        """
        from .blocks import BlocksAPI
        return BlocksAPI(self)
        
    def subscriptions(self):
        """Get the subscriptions API client.

        Returns:
            SubscriptionsAPI client
        """
        from .subscriptions import SubscriptionsAPI
        return SubscriptionsAPI(self)
        
    def timeline(self):
        """Get the timeline API client.

        Returns:
            TimelineAPI client
        """
        from .timeline import TimelineAPI
        return TimelineAPI(self)
        
    def stopwatch(self):
        """Get the stopwatch API client.

        Returns:
            StopwatchAPI client
        """
        from .stopwatch import StopwatchAPI
        return StopwatchAPI(self)
        
    def pinned(self):
        """Get the pinned issues API client.

        Returns:
            PinnedAPI client
        """
        from .pinned import PinnedAPI
        return PinnedAPI(self)
