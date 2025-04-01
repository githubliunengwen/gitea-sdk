"""Custom exceptions for the Gitea Issues SDK."""


class GiteaError(Exception):
    """Base exception for all Gitea API errors."""

    def __init__(self, message: str):
        """Initialize the exception.

        Args:
            message: Error message
        """
        self.message = message
        super().__init__(self.message)


class GiteaAPIError(GiteaError):
    """Exception raised for errors returned by the Gitea API."""

    def __init__(self, message: str, status_code: int = None, response_body: str = None):
        """Initialize the exception.

        Args:
            message: Error message
            status_code: HTTP status code
            response_body: Response body from the API
        """
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(f"API Error: {message} (Status: {status_code})")


class GiteaConnectionError(GiteaError):
    """Exception raised for connection errors when contacting the Gitea API."""

    def __init__(self, message: str, original_error: Exception = None):
        """Initialize the exception.

        Args:
            message: Error message
            original_error: Original exception that caused this error
        """
        self.original_error = original_error
        super().__init__(f"Connection Error: {message}")


class GiteaAuthenticationError(GiteaError):
    """Exception raised for authentication errors with the Gitea API."""

    def __init__(self, message: str = "Authentication failed"):
        """Initialize the exception.

        Args:
            message: Error message
        """
        super().__init__(f"Authentication Error: {message}")


class GiteaValidationError(GiteaError):
    """Exception raised for validation errors in the SDK."""

    def __init__(self, message: str, field: str = None):
        """Initialize the exception.

        Args:
            message: Error message
            field: Field that failed validation
        """
        self.field = field
        field_info = f" (Field: {field})" if field else ""
        super().__init__(f"Validation Error: {message}{field_info}")


class GiteaRateLimitError(GiteaError):
    """Exception raised when the API rate limit is exceeded."""

    def __init__(self, message: str = "API rate limit exceeded", reset_time: str = None):
        """Initialize the exception.

        Args:
            message: Error message
            reset_time: Time when the rate limit will reset
        """
        self.reset_time = reset_time
        reset_info = f", resets at {reset_time}" if reset_time else ""
        super().__init__(f"Rate Limit Error: {message}{reset_info}")


class GiteaTimeoutError(GiteaError):
    """Exception raised when an API request times out."""

    def __init__(self, message: str = "API request timed out", timeout: float = None):
        """Initialize the exception.

        Args:
            message: Error message
            timeout: Timeout value in seconds
        """
        self.timeout = timeout
        timeout_info = f" after {timeout} seconds" if timeout else ""
        super().__init__(f"Timeout Error: {message}{timeout_info}")


class GiteaNotFoundError(GiteaAPIError):
    """Exception raised when a resource is not found."""

    def __init__(self, message: str, resource_type: str = None, resource_id: str = None):
        """Initialize the exception.

        Args:
            message: Error message
            resource_type: Type of resource that was not found
            resource_id: ID of the resource that was not found
        """
        self.resource_type = resource_type
        self.resource_id = resource_id
        
        details = ""
        if resource_type:
            details += f" {resource_type}"
        if resource_id:
            details += f" '{resource_id}'"
            
        super().__init__(f"Not Found:{details} - {message}", status_code=404)
